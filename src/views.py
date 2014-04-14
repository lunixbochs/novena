from flask import (
    render_template,
    request,
)
import json

from app import app, mongo

@app.before_first_request
def init():
    mongo.db.hashes.ensure_index([('bits', 1)])
    mongo.db.hashes.ensure_index([('contents', 1)])
    mongo.db.hashes.ensure_index([('ip', 1), ('bits', 1)])

@app.route('/')
def index():
    ip = request.args.get('ip', request.remote_addr)
    counts = {}
    bits = mongo.db.hashes.find({'ip': ip}).distinct('bits')
    for i in bits:
        hashcount = mongo.db.hashes.find({'ip': ip, 'bits': i}).count()
        if hashcount:
            counts[i] = hashcount
    return render_template('index.html', counts=counts)

@app.route('/submit', methods=['POST'])
def submit():
    data = json.loads(request.environ['body_copy'])
    if not mongo.db.hashes.find_one({'contents': data['contents']}):
        doc = {
            'contents': data['contents'],
            'bits': data['bits'],
            'ip': request.remote_addr,
        }
        mongo.db.hashes.insert(doc)
    return ''
