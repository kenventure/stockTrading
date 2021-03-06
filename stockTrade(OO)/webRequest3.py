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
print (r.headers)

urlMarket = "https://demo-api.ig.com/gateway/deal/markets/CS.D.EURUSD.MINI.IP"

headers = { "Content-Type": "application/json; charset=utf-8",
"Accept": "application/json; charset=utf-8",
"X-IG-API-KEY": m_apiKey,
"Version": "3",
"X-SECURITY-TOKEN": r.headers['X-SECURITY-TOKEN'],
"CST": r.headers['CST']
}

r1 = requests.get(urlMarket, headers = headers)

print(r1.status_code)
print (r1.text) 



#urlMarket = "https://demo-api.ig.com/gateway/deal/prices/CS.D.EURUSD.MINI.IP?resolution=MINUTE_5&from=2017-06-21T00%3A00%3A00&to=2017-06-21T23%3A59%3A59&max=100&pageSize=100&pageNumber=1"
urlMarket = "https://demo-api.ig.com/gateway/deal/prices/IX.D.DOW.IFG.IP?resolution=MINUTE_5&from=2017-06-21T00%3A00%3A00&to=2017-06-21T23%3A59%3A59&max=100&pageSize=100&pageNumber=1"

headers = { "Content-Type": "application/json; charset=utf-8",
"Accept": "application/json; charset=utf-8",
"X-IG-API-KEY": m_apiKey,
"Version": "3",
"X-SECURITY-TOKEN": r.headers['X-SECURITY-TOKEN'],
"CST": r.headers['CST']
}

r1 = requests.get(urlMarket, headers = headers)

print(r1.status_code)
print (r1.text) 