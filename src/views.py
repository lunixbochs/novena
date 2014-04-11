from bs4 import BeautifulSoup
from datetime import timedelta
from flask import (
    render_template,
    request,
    Response,
)
import json

from app import app, mongo

@app.before_first_request
def init():
    mongo.db.hashes.ensure_index([('bits', 1)])
    mongo.db.hashes.ensure_index([('contents', 1)])

@app.route('/submit', methods=['POST'])
def submit():
    data = json.loads(request.environ['body_copy'])
    if not mongo.db.hashes.findOne({'contents': data['contents']}):
        mongo.db.hashes.insert({'contents': data['contents'], 'bits': data['bits']})
    return ''
