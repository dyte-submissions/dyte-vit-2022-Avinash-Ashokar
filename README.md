# Github CLI Tool

## Prerequisite

- Github Access Token

[Creating a personal access token - GitHub Docs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

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

## Credits

- Thanks for this activity. It was fun.
- And Hats off to the person who wrote that notion instruction. It was really creative. Please give them a hike.
- I must finally thank stackoverflow, for helping me when I am stuck.
