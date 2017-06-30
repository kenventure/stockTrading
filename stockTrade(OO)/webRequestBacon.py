import requests

url = 'http://baconipsum.com/api/?type=meat-and-filler'
data = '{  "type": "meat-and-filler"}'

headers = {"Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json; charset=UTF-8",
            "VERSION": "2",
            "X-IG-API-KEY": "2816010fc8a0d7c446393955d5b3e9"
}

response = requests.post(url, data=data)
print(response)

#string = response.read()

print(response.text)
