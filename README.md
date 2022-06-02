# JARVIS CLI Tool

## Prerequisite

- [Github Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- Python Virtualenv setup
- Python3
- Good Internet Connection

## Installation

```jsx
pip install virtualenv
```

if it’s not working properly try it with sudo.

```jsx
git clone https://github.com/dyte-submissions/dyte-vit-2022-Avinash-Ashokar.git
```

```jsx
cd dyte-vit-2022-Avinash-Ashokar/
```

```jsx
virtualenv testing
```

```jsx
source testing/bin/activate
```

```jsx
python setup.py develop
```

```jsx
jarvis configure ACCESS_TOKEN
```

In my case it is “jarvis configure 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”

My access token will be deleted by the time you are reading this 😅.

```jsx
jarvis check -i input.csv axios@0.23.0
```

The above command is to check versions

```jsx
jarvis update -i input.csv axios@0.23.0
```

The above command will create a pull request. 

## Hidden Features

- You could run `jarvis configure ACCESS_TOKEN` command as many time as you want.
- `jarvis check` command can be used even without configuring jarvis cli tool.
- `jarvis update` command knows when there is a existing Pull request.
- If we are stuck somewhere, then we can execute `jarvis —help` to know the available list of commands
- Both `jarvis check` and `jarvis update` command generate a output.csv file, which can be used to for later reference.

## Future works

- Need to make it more interactive.
- Encrypt the access token file.
- Modifying commands to check multiple package version at the same time.
- Releasing it as a Pypi project.

## Credits

- Thanks for this activity. It was fun.
- And Hats off to the person who wrote that notion instruction. It was really creative. Please give them a raise.
- I must finally thank stackoverflow, for helping me when I am stuck.
