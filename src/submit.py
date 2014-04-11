from datetime import datetime

import json
import pymongo
import requests
import time
import traceback

db = pymongo.Connection().novena
username = 'lunixbochs'

def get_difficulty():
    try:
        response = requests.get('http://novena-puzzle.crowdsupply.com/difficulty')
        return response.json().get('difficulty')
    except Exception:
        traceback.print_exc()

def submit(contents):
    try:
        response = requests.post('http://novena-puzzle.crowdsupply.com/submit', data=json.dumps({
            'username': username, 'contents': contents,
        }))
        if response.status_code == 502:
            return False
        return response.json()
    except Exception:
        traceback.print_exc()

difficulty = get_difficulty()
print 'difficulty:', difficulty
while True:
    for i in xrange(30):
        hashes = list(db.hashes.find({'bits': {'$gte': difficulty}, 'submitted': {'$exists': False}}))
        for h in hashes:
            print 'submitting: "%s":' % h['contents'],
            try:
                response = submit(h['contents'])
                db.hashes.update({'_id': h['_id']}, {'$set': {'response': response, 'submitted': True}})
                print response
            except Exception:
                traceback.print_exc()
        time.sleep(1)
    new_diff = get_difficulty()
    if new_diff != difficulty:
        print 'difficulty changed:', new_diff
        difficulty = new_diff
        db.hashes.difficulty.insert({'time': datetime.now(), 'difficulty': difficulty})
