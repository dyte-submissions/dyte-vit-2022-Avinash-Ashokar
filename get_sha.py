import requests
import json

# Get SHA value
def getSHA(url, authToken):
    payload = ""
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': authToken
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(json.dumps(response.json(), indent = 1))
    return response.json()["sha"]