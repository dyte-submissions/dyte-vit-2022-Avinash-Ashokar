import requests
import json

# Create Fork
def createFork(url, authToken):
    payload={}
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': authToken
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()["url"]