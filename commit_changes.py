import requests
import json

# Commit Changes
def commitChanges(url, authToken, commitMessage, contentValue, sha):
    payload = json.dumps({
        "message": commitMessage,
        "content": contentValue,
        "sha": sha
    })
    headers = {
        'Authorization': authToken,
        'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data=payload)