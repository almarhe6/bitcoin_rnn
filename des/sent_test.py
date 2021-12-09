import requests

r = requests.get('http://api.senticrypt.com/v1/history/bitcoin-2020-02-13_20.json')
print(r.json()[0]['sum'])
