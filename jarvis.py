import click
import csv
import os
from write_csv_file import writeCSVFiles
from read_csv_file import readCSVFile
from merge_request import mergeRequest

# Storing home directory path and creating a hidden directory to store access token value
homeDir = os.path.expanduser('~')
cooltoolDir = homeDir + "/.cooltool/"

if not os.path.exists(cooltoolDir):
    os.makedirs(cooltoolDir)
    tokenFile = open(homeDir+"/.cooltool/access_token.txt", 'w')
    tokenFile.close()

@click.group()
def cli():
    pass

#This command is to only check whether there are any deprecated packages in the repository
@cli.command()
@click.option('-i', '--input', type=str, help='CSV File Location')
@click.argument('ver', nargs=1)
def check(input, ver):
    readCSVFile(input, ver)

#This command is to configure the cooltool
@cli.command()
@click.argument('token', nargs=1)
def configure(token):
    file = open(cooltoolDir+"/access_token.txt", "w") 
    file.write(token)
    file.close()


#This command is to create a PR request
@cli.command()
@click.option('-i', '--input', type=str, help='CSV File Location')
@click.argument('ver', nargs=1)
def update(input, ver):
    tokenData = open(cooltoolDir+"/access_token.txt", "r")
    token = tokenData.read()
    bearToken = "Bearer " + token
    tokenData.close()

    if (token == ""):
        print("\nConfigure Cooltool before using update command")
        print("To configure type \"jarvis configure ACCESS_TOKEN\" ")
    else:
        mergeRequest(input, ver, bearToken)
