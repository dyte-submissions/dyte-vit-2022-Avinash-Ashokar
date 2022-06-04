import requests
import json
import base64

# This function creates fork of the target repository
def create_fork(base_url, bear_token):
    fork_url = base_url.replace("github.com", "api.github.com/repos") + "forks"

    payload={}
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': bear_token
    }

    response = requests.request("POST", fork_url, headers=headers, data=payload)

    return response.json()["url"], response.json()["source"]["default_branch"]

# This function create sha value which will be used for sending commit request
def generate_sha(base_sha_url, bear_token):
    # sha url for package.json
    sha_url = base_sha_url + "/contents/package.json"
    # sha url for package-lock.json
    sha_url_lock = sha_url.replace("package", "package-lock")

    payload = ""
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': bear_token
    }

    # response for package.json
    response = requests.request("GET", sha_url, headers=headers, data=payload)
    # response for package-lock.json
    response_lock = requests.request("GET", sha_url_lock, headers=headers, data=payload)

    return response.json()["sha"], response_lock.json()["sha"], sha_url, sha_url_lock

# This function will be called after c=making changes to the target file
def send_commit_request(sha_url, bear_token, commit_message, content_value, sha_value):
    payload = json.dumps({
        "message": commit_message,
        "content": content_value,
        "sha": sha_value
    })
    headers = {
        'Authorization': bear_token,
        'Content-Type': 'application/json'
    }

    response = requests.request("PUT", sha_url, headers=headers, data=payload)

# This function make changes to the target file and pushes the changes to out fork repository
def commit_changes(package_name, existing_version, package_version, package_json, package_lock_json, sha_value, sha_value_lock, sha_url, sha_url_lock, bear_token):
    commit_message = "Changing " + package_name + " version from " + existing_version + " to "+ package_version

    package_json["dependencies"][package_name] = "^"+package_version
    package_lock_json["packages"][""]["dependencies"][package_name] = "^"+package_version
    package_json = json.dumps(package_json, indent = 1)
    package_lock_json = json.dumps(package_lock_json, indent = 1)

    encoded_package_json = base64.b64encode(package_json.encode('utf-8'))
    decoded_package_json = encoded_package_json.decode("utf-8")

    encoded_package_lock_json = base64.b64encode(package_lock_json.encode('utf-8'))
    decoded_package_lock_json = encoded_package_lock_json.decode('utf-8')

    send_commit_request(sha_url, bear_token, commit_message, decoded_package_json, sha_value)
    send_commit_request(sha_url_lock, bear_token, commit_message, decoded_package_lock_json, sha_value_lock)

# This function if used to get the user name, which will be used to know the head value of the target branch
def get_user_name(bear_token):
    url = "https://api.github.com/user"

    payload = ""
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': bear_token
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()["login"]

# Creates a pull request in the target repository and returns a pull request url
def create_pull_request(base_url, bear_token, package_name, package_version, existing_version, base_branch):
    title = "Changing " + package_name + " version from " + existing_version + " to "+ package_version
    head = get_user_name(bear_token) + ":" + base_branch
    body = "Please accept these awesome changes and secure our codebase from vulnerabilities"
    base = base_branch

    pull_url = base_url.replace("github.com", "api.github.com/repos") + "pulls"

    payload = json.dumps({
        "title": title,
        "body": body,
        "head": head,
        "base": base
    })
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': bear_token,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", pull_url, headers=headers, data=payload)
    try:
        if (response.json()["errors"][0]["message"].__contains__("A pull request already exists")):
            return "A pull request already exists!"
    except KeyError:
        return response.json()["url"]

def generate_pull_requests(package_json, package_lock_json, package_name, package_version, existing_version, base_url, bear_token):
    base_sha_url, base_branch = create_fork(base_url, bear_token)

    sha_value, sha_value_lock, sha_url, sha_url_lock = generate_sha(base_sha_url, bear_token)
    
    commit_changes(package_name, existing_version, package_version, package_json, package_lock_json, sha_value, sha_value_lock, sha_url, sha_url_lock, bear_token)

    pull_request_url = create_pull_request(base_url, bear_token, package_name, package_version, existing_version, base_branch)
    pull_request_url = pull_request_url.replace("api.github.com", "github.com")
    pull_request_url = pull_request_url.replace("repos/", "")
    pull_request_url = pull_request_url.replace("pulls", "pull")

    return pull_request_url