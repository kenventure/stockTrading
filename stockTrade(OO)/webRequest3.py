import requests
import base64
import json 
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5 
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