import requests

x = requests.get("http://192.168.1.61/api/echo?message=test1")
print(x.text)