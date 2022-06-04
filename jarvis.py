import click
import requests
import json
import os

from check_deprecated_packages import check_deprecated_packages
from update_deprecated_packages import update_deprecated_packages

# Storing home directory path and creating a hidden directory to store access token value
home_dir = os.path.expanduser('~')
jarvis_dir = home_dir + "/.jarvis/"

# Creating a directory for jarvis, in case if it is not present. Then creating his secret file.
if not os.path.exists(jarvis_dir):
    os.makedirs(jarvis_dir)
    access_token_file = open(home_dir+"/.jarvis/access_token.txt", 'w')
    access_token_file.close()

# The below function just reads the token from the file
def get_token():
    access_token_file = open(jarvis_dir+"access_token.txt", "r")
    access_token = access_token_file.read()

    # I chose bearer token because it sounds cool. But if you found anything that sounds better than this,
    # please let me know.
    bear_token = "Bearer " + access_token
    access_token_file.close()

    return bear_token

# This function if used to get the user name, which will be used to know the head value of the target branch
def get_user_name(access_token):
    bear_token = "Bearer " + access_token
    url = "https://api.github.com/user"

    payload = ""
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': bear_token
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if ("message" in response.json()):
        click.echo(response.json()["message"])
        return ":("
    else:
        return response.json()["login"]

@click.group()
def cli():
    pass

#This command is to configure the jarvis cli tool
@cli.command()
@click.argument('access_token', nargs=1)
def configure(access_token):
    """
    This command is used to configure jarvis cli tool
    Sample command:
    jarvis configure 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
    """

    file = open(jarvis_dir+"/access_token.txt", "w") 
    if (get_user_name(access_token) == ":("):
        file.write("")
    else:
        file.write(access_token)
        click.echo("Jarvis configured successfully :)")

    file.close()

#This command is to only check whether there are any deprecated packages in the repository
@cli.command()
@click.option('-i', '--file_name', type=str, help='CSV File Location')
@click.argument('packages_name_with_version', nargs=-1)
def check(file_name, packages_name_with_version):
    """
    This command helps you by checking the repositories for any deprecated packages.
    Sample command:
    jarvis check -i input.csv axios@0.25.0 cors@2.8.5
    """

    bear_token = get_token()
    
    # The below check is being implemented for people who want to mess with jarvis, by entering command in
    # different order
    if (bear_token == "Bearer "):
        click.echo("\nConfigure jarvis before using check command")
        click.echo("To configure type \"jarvis configure ACCESS_TOKEN\" ")
    else:
        # Jarvis is so capabale he even defeated ultron. But in my case he is only capable of checking
        # versions for multiple packages
        for package_name_with_version in packages_name_with_version:
            check_deprecated_packages(file_name, package_name_with_version, bear_token)

#This command is to create a PR request
@cli.command()
@click.option('-i', '--file_name', type=str, help='CSV File Location')
@click.argument('packages_name_with_version', nargs=-1)
def update(file_name, packages_name_with_version):
    """
    This command helps you in generating a PR.
    Sample command:
    jarvis update -i input.csv axios@0.25.0 cors@2.8.5
    """

    bear_token = get_token()

    # The below check is being implemented for people who want to mess with jarvis, by entering command in
    # different order
    if (bear_token == "Bearer "):
        click.echo("\nConfigure jarvis before using update command")
        click.echo("To configure type \"jarvis configure ACCESS_TOKEN\" ")
    else:
        for package_name_with_version in packages_name_with_version:
            update_deprecated_packages(file_name, package_name_with_version, bear_token)