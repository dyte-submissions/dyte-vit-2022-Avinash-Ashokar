from create_fork import createFork
from get_sha import getSHA
from get_username import getUserName
from commit_changes import commitChanges
from create_pull_requests import createPullRequests
from write_csv_file import writeCSVFiles
import os
import csv
import json
import requests
import re
import base64

# Pull Request Parameters
# title = "Updating old libraries"
body = "Please accept these awesome changes and secure our codebase from vulnerabilities"
base = "main"

def mergeRequest(input, ver, bearToken):
    word = ver.split("@")
    packageName = word[0];
    versionNo = word[1];
    
    with open(input, mode ='r')as file:
        csvFile = csv.reader(file)
        newCSVFile = []
        
        for lines in csvFile:
            givenUrl = lines[1]+'main/package.json'
            givenUrlLock = lines[1]+'main/package-lock.json'
            rawJSON = givenUrl.replace("github.com", "raw.githubusercontent.com")
            rawJSONLock = givenUrlLock.replace("github.com", "raw.githubusercontent.com")
            response = json.loads(requests.get(rawJSON).text)
            responseLock = json.loads(requests.get(rawJSONLock).text)

            dependencies = response["dependencies"]
            dependenciesLock = responseLock["packages"][""]["dependencies"]

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
                    responseLock["packages"][""]["dependencies"][packageName] = "^"+versionNo
                    # print(json.dumps(responseLock, indent=1))
                    response = json.dumps(response, indent = 1)
                    responseLock = json.dumps(responseLock, indent = 1)

                    # print(response)
                    # print(responseLock)

                    contentValue = base64.b64encode(response.encode('utf-8'))
                    contentValue = contentValue.decode("utf-8")

                    contentValueLock = base64.b64encode(responseLock.encode('utf-8'))
                    contentValueLock = contentValueLock.decode('utf-8')

                    forkURL = lines[1].replace("github.com", "api.github.com/repos") + "forks"
                    pullURL = forkURL.replace("forks", "pulls")
                    shaURL = createFork(forkURL, bearToken)
                    shaURL = shaURL + "/contents/package.json"
                    shaURLLock = shaURL.replace("package", "package-lock")

                    shaValue = getSHA(shaURL, bearToken)
                    shaValueLock = getSHA(shaURLLock, bearToken)
                    commitMessage = "Changing " + packageName + " version from " + new_text + " to "+ versionNo
                    title = commitMessage
                    commitChanges(shaURL, bearToken, commitMessage, contentValue, shaValue)
                    commitChanges(shaURLLock, bearToken, commitMessage, contentValueLock, shaValueLock)
                    head = getUserName(bearToken)
                    head = head+":main"
                    requestURL = createPullRequests(pullURL, bearToken, title, body, head, base)
                    requestURL = requestURL.replace("api.github.com", "github.com")
                    requestURL = requestURL.replace("repos/", "")
                    requestURL = requestURL.replace("pulls", "pull")
                    eachRow.append(requestURL)
                    newCSVFile.append(eachRow)
                else:
                    eachRow.append("true")
                    eachRow.append("")
                    newCSVFile.append(eachRow)
            
        fields = ["name", "repo", "version", "version_satisfied", "update_pr"]

        writeCSVFiles(fields, newCSVFile)