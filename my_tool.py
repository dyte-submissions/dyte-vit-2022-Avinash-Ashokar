import click
import csv
import requests
import json
import re
import base64

# Pull Request Parameters
title = "Updating old libraries"
body = "Please accept these awesome changes and secure our codebase from vulnerabilities"
base = "main"

# Create Fork
def createFork(url, authToken):
    payload={}
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': authToken
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()["url"]

# Get SHA value
def getSHA(url, authToken):
    payload = ""
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': authToken
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()["sha"]

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
    return response.json()["url"]

@click.group()
def cli():
    pass

@cli.command()
@click.option('-i', '--input', type=str, help='CSV File Location')
@click.argument('ver', nargs=1)
def check(input, ver):
    word = ver.split("@")
    packageName = word[0];
    versionNo = word[1];
    
    # opening the CSV file
    with open(input, mode ='r')as file:
    
        # reading the CSV file
        csvFile = csv.reader(file)
        
        newCSVFile = []
        # displaying the contents of the CSV file
        for lines in csvFile:
            givenUrl = lines[1]+'main/package.json';
            rawJSON = givenUrl.replace("github.com", "raw.githubusercontent.com")
            response = json.loads(requests.get(rawJSON).text)

            dependencies = response["dependencies"]

            if packageName in dependencies:
                eachRow = []
                eachRow.append(lines[0])
                eachRow.append(lines[1])

                text = dependencies[packageName]
                new_text = re.sub(r"[^0-9\.]", "", text)

                eachRow.append(new_text)
                if (new_text < versionNo):
                    eachRow.append("false")
                    newCSVFile.append(eachRow)
                    print("All details are being stored in output.csv file")
                else:
                    eachRow.append("true")
                    newCSVFile.append(eachRow)
            
        # print(newCSVFile)
        fields = ["name", "repo", "version", "version_satisfied"]

        with open("output.csv", 'w') as csvfile: 
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
                
            # writing the fields 
            csvwriter.writerow(fields) 
                
            # writing the data rows 
            csvwriter.writerows(newCSVFile)

@cli.command()
@click.option('-i', '--input', type=str, help='CSV File Location')
@click.argument('ver', nargs=1)
@click.argument('token', nargs=1)
def update(input, ver, token):
    word = ver.split("@")
    packageName = word[0];
    versionNo = word[1];
    bearToken = "Bearer " + token
    
    # opening the CSV file
    with open(input, mode ='r')as file:
    
        # reading the CSV file
        csvFile = csv.reader(file)
        
        newCSVFile = []
        # displaying the contents of the CSV file
        for lines in csvFile:
            givenUrl = lines[1]+'main/package.json';
            rawJSON = givenUrl.replace("github.com", "raw.githubusercontent.com")
            response = json.loads(requests.get(rawJSON).text)

            dependencies = response["dependencies"]

            if packageName in dependencies:
                eachRow = []
                eachRow.append(lines[0])
                eachRow.append(lines[1])

                text = dependencies[packageName]
                new_text = re.sub(r"[^0-9\.]", "", text)

                eachRow.append(new_text)
                if (new_text < versionNo):
                    eachRow.append("false")
                    response["dependencies"][packageName] = "^"+versionNo
                    response = json.dumps(response, indent = 1)
                    contentValue = base64.b64encode(response.encode('utf-8'))
                    contentValue = contentValue.decode("utf-8")
                    forkURL = lines[1].replace("github.com", "api.github.com/repos") + "forks"
                    pullURL = forkURL.replace("forks", "pulls")
                    shaURL = createFork(forkURL, bearToken)
                    shaURL = shaURL + "/contents/package.json"
                    shaValue = getSHA(shaURL, bearToken)
                    commitMessage = "Changing " + packageName + " version from " + new_text + " to "+ versionNo
                    commitChanges(shaURL, bearToken, commitMessage, contentValue, shaValue)
                    head = getUserName(bearToken)
                    head = head+":main"
                    requestURL = createPullRequests(pullURL, bearToken, title, body, head, base)
                    requestURL = requestURL.replace("api.github.com", "github.com")
                    requestURL = requestURL.replace("repos/", "")
                    requestURL = requestURL.replace("pulls", "pull")
                    eachRow.append(requestURL)
                    newCSVFile.append(eachRow)
                    print("All details are being stored in output.csv file")
                else:
                    eachRow.append("true")
                    eachRow.append("")
                    newCSVFile.append(eachRow)
            
        # print(newCSVFile)
        fields = ["name", "repo", "version", "version_satisfied", "update_pr"]

        with open("output.csv", 'w') as csvfile: 
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
                
            # writing the fields 
            csvwriter.writerow(fields) 
                
            # writing the data rows 
            csvwriter.writerows(newCSVFile)