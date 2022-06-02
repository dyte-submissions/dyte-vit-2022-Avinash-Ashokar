import requests
import json

# Create Pull Requests
def createPullRequests(url, authToken, title, body, head, base):
    payload = json.dumps({
        "title": title,
        "body": body,
        "head": head,
        "base": base
    })
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': authToken,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        if (response.json()["errors"][0]["message"].__contains__("A pull request already exists")):
            return "A pull request already exists!"
    except KeyError:
        return response.json()["url"]