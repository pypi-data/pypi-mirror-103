import requests

def getGoogle():
    print(requests.get("https://www.google.com").text)
