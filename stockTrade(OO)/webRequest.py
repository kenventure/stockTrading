import requests

url = 'https://demo-api.ig.com/gateway/deal/session'

#url = 'https://demo-api.ig.com/gateway/deal'
#data = { 'encryptedPassword': 'False', 'identifier': 'lthams', 'password': '1q2w3e4rT',}
data = '{ "identifier": "lthams", "password": "1q2w3e4rT", "encryptedPassword": "False"}'
#data = '{ "encryptedPassword": False, "identifier": "lthams1", "password": "1q2w3e4rT"}'

headers = {'Content-Type': 'application/json; charset=UTF-8', 'Accept': 'application/json; charset=UTF-8', 'VERSION': '2', 'X-IG-API-KEY': '2816010fc8a0d7c446393955d5b3e922c1b1b955'}

response = requests.post(url, data=data,headers=headers)
print(response)

print(response.text)