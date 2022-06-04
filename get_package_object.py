import requests
import json

# Function to get the raw file url. Raw file is easier to handle.
def get_raw_url(url, auth_token):
    payload={}
    headers = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': auth_token
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    for obj in response.json():
        if obj["name"] == "package.json":
            raw_package_json_url = obj["download_url"]

        if obj["name"] == "package-lock.json":
            raw_package_lock_json_url = obj["download_url"]

    return raw_package_json_url, raw_package_lock_json_url

# I need to find a better name for this function
def get_package_object(url, auth_token):
    url = url.replace("github.com", "api.github.com/repos")
    url = url + "contents/"

    raw_package_json_url, raw_package_lock_json_url = get_raw_url(url, auth_token)

    # Storing json data
    package_json = json.loads(requests.get(raw_package_json_url).text)
    package_lock_json = json.loads(requests.get(raw_package_lock_json_url).text)

    # Storing dependency data in an object
    package_json_dependencies = package_json["dependencies"]
    package_lock_json_dependencies = package_lock_json["packages"][""]["dependencies"]

    return package_json, package_lock_json, package_json_dependencies