#!/usr/bin/python

#  Copyright 2015 Weswit s.r.l.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import sys
import traceback
import logging
from trading_ig.lightstreamer import LSClient, Subscription

import requests
import base64
import json 
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5 


# A simple function acting as a Subscription listener
def on_item_update(item_update):
    print("{stock_name:<19}: Last{last_price:>6} - Time {time:<8} - "
          "Bid {bid:>5} - Ask {ask:>5}".format(**item_update["values"]))


# In[] 
url = "https://demo-api.ig.com/gateway/deal"
identifier = "lthams"
password = "1q2w3e4rT"
m_apiKey = "2816010fc8a0d7c446393955d5b3e922c1b1b955"
session = "/session/encryptionKey"
m_url = url + session
headers = { "Content-Type": "application/json; charset=utf-8",
"Accept": "application/json; charset=utf-8",
"X-IG-API-KEY": m_apiKey
} 
# In[]
r = requests.get(m_url, headers=headers)
# In[] 
m_data = r.json() 
decoded = base64.b64decode(m_data['encryptionKey'])
rsakey = RSA.importKey(decoded)
message = password + '|' + str(int(m_data['timeStamp']))
input = base64.b64encode(message.encode())
encryptedPassword = base64.b64encode(PKCS1_v1_5.new(rsakey).encrypt(input))
session = "/session"
m_url = url + session
headers = { "Content-Type": "application/json; charset=utf-8",
"Accept": "application/json; charset=utf-8",
"X-IG-API-KEY": m_apiKey,
"Version": "2"
} 
payload = json.dumps({ "identifier": identifier,
"password": encryptedPassword.decode('utf-8'),
"encryptedPassword": True
}) 
# In[]
r = requests.post(m_url, data=payload, headers=headers)
r.status_code
print (r.status_code)
print (r.text)
print (r.headers)
data = json.loads(r.text)
#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

# Establishing a new connection to Lightstreamer Server
print("Starting connection")
#lightstreamer_client = LSClient("http://localhost:8080", "DEMO")
#lightstreamer_client = LSClient("http://push.lightstreamer.com", "DEMO")
passwordSet = "CST-" + r.headers['CST'] + "|XST-" + r.headers['X-SECURITY-TOKEN']
lightstreamer_client = LSClient(data['lightstreamerEndpoint'], "DEMO", user=identifier, password=passwordSet)


try:
    lightstreamer_client.connect()
except Exception as e:
    print("Unable to connect to Lightstreamer Server")
    print(traceback.format_exc())
    sys.exit(1)


# Making a new Subscription in MERGE mode
subscription = Subscription(
    mode="MERGE",
    items=["item1", "item2", "item3", "item4",
           "item5", "item6", "item7", "item8",
           "item9", "item10", "item11", "item12"],
    fields=["stock_name", "last_price", "time", "bid", "ask"],
    adapter="QUOTE_ADAPTER")


# Adding the "on_item_update" function to Subscription
subscription.addlistener(on_item_update)

# Registering the Subscription
sub_key = lightstreamer_client.subscribe(subscription)

#input("{0:-^80}\n".format("HIT CR TO UNSUBSCRIBE AND DISCONNECT FROM LIGHTSTREAMER"))

# Unsubscribing from Lightstreamer by using the subscription key
#lightstreamer_client.unsubscribe(sub_key)


lightstreamer_client.unsubscribe(sub_key)

# Disconnecting
lightstreamer_client.disconnect()

#if __name__ == '__main__':

