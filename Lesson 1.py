import requests
import json

url = 'https://api.github.com/users/R-u-z-a/repos'

response = requests.get(url)
# print(response.headers.get('Content-Type'))
j_data = response.json()
# pprint(j_data)
for i in j_data:
    print(i["name"])

with open('data.json', 'w') as f:
    json.dump(response.json(), f)

# for i in response.json():
# print(i['name'])
