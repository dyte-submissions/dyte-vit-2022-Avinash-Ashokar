import requests
import json

# Get User Name
def getUserName(authToken):
    url = "https://api.github.com/user"

    payload = ""
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': authToken
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()["login"]