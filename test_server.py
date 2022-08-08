# predict the emoji probabilities given arbitrary sentences
# usage: python2 test_server.py "Congrats"

import requests
import sys
import json

# curl -X POST \
#   http://127.0.0.1:12340 \
#   -H 'Cache-Control: no-cache' \
#   -H 'Content-Type: application/json' \
#   -H 'Postman-Token: 748a5055-d93a-4c2a-91ef-1b3bd1135845' \
#   -d '{
#       "sentences": ["hello"]
# }'

query = sys.argv[1]

headers = {
    'Cache-Control': 'no-cache',
    # Already added when you pass json= but not when you pass data=
    # 'Content-Type': 'application/json',
    'Postman-Token': '748a5055-d93a-4c2a-91ef-1b3bd1135845',
}

json_data = {
    'sentences': [query,],
}

# response = requests.post('http://127.0.0.1:12345', headers=headers, json=json_data)
response = requests.post('http://caixingyu.c.googlers.com:12345', headers=headers, json=json_data)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{\n        "sentences": ["hello"]\n}'
#response = requests.post('http://127.0.0.1:12340', headers=headers, data=data)

r = response.json()['emoji'][0]
r = sorted(r, key=lambda e: e['prob'])[::-1]
for i in range(5):
    print(r[i]['emoji'].encode('utf-8') + ' prob: ' + str(r[i]['prob']))
