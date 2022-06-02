import re
import csv
import json
import requests

from write_csv_file import writeCSVFiles

def readCSVFile(input, ver):
    word = ver.split("@")
    packageName = word[0];
    versionNo = word[1];

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
                else:
                    eachRow.append("true")
                    newCSVFile.append(eachRow)
            
        fields = ["name", "repo", "version", "version_satisfied"]

        writeCSVFiles(fields, newCSVFile)