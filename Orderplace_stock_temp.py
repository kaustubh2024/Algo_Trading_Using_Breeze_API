import http.client
import json
from datetime import datetime
import hashlib
import login as l

# App related key and token
app_key = l.api_key
secret_key = l.api_secret
session_token = l.session_key

#request-body generation
# 'body' is the request-body of your current request
body = {"exchange_code": "NSE","from_date": "2023-03-12T04:00:00.000Z","to_date": "2023-03-12T04:00:00.000Z","underlying": "IDECEL","portfolio_type": ""} # Example

payload_for_checksum = json.dumps(body, separators=(',', ':'))

#request-headers generation
current_date = datetime.utcnow().isoformat()[:19] + '.000Z'
checksum = hashlib.sha256((current_date+payload_for_checksum+secret_key).encode("utf-8")).hexdigest()
headers = {
    "Content-Type": "application/json",
    'X-Checksum': "token "+checksum,
    'X-Timestamp': current_date,
    'X-AppKey': app_key,
    'X-SessionToken': session_token
}

payload = json.dumps(body)
#request-url generation
conn = http.client.HTTPSConnection("api.icicidirect.com")
conn.request("GET", "/breezeapi/api/v1/portfolioholdings", payload, headers)

# request call
res = conn.getresponse()

data = res.read()

#print response 
print(data.decode("utf-8"))