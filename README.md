# JARVIS CLI Tool

## Prerequisite

- [Github Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- Python Virtualenv setup
- Python3
- Good Internet Connection

## Installation

The below commands were tested in Arch Linux

```jsx
pip install virtualenv
```

if it’s not working properly try it with sudo.

```jsx
git clone https://github.com/dyte-submissions/dyte-vit-2022-Avinash-Ashokar.git
```

```jsx
cd dyte-vit-2022-Avinash-Ashokar-main
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

![Untitled](JARVIS%20CLI%20Tool%20b9d3df401ce749768b02867019def7c8/Untitled.png)

```jsx
jarvis check -i input.csv axios@0.23.0 cors@2.8.5
```

The above command is to check versions. We could even check for multiple versions.

![Untitled](JARVIS%20CLI%20Tool%20b9d3df401ce749768b02867019def7c8/Untitled%201.png)

```jsx
jarvis update -i input.csv axios@0.23.0 cors@2.8.6
```

The above command will create a pull request. We can create pull request for multiple files simultaneously.

![Untitled](JARVIS%20CLI%20Tool%20b9d3df401ce749768b02867019def7c8/Untitled%202.png)

Commands which can be used when we are stuck

![Untitled](JARVIS%20CLI%20Tool%20b9d3df401ce749768b02867019def7c8/Untitled%203.png)

![Untitled](JARVIS%20CLI%20Tool%20b9d3df401ce749768b02867019def7c8/Untitled%204.png)

![Untitled](JARVIS%20CLI%20Tool%20b9d3df401ce749768b02867019def7c8/Untitled%205.png)

![Untitled](JARVIS%20CLI%20Tool%20b9d3df401ce749768b02867019def7c8/Untitled%206.png)

## Hidden Features

- You could run `jarvis configure ACCESS_TOKEN` command as many time as you want.
- `jarvis update` command knows when there is an existing Pull request.

![Untitled](JARVIS%20CLI%20Tool%20b9d3df401ce749768b02867019def7c8/Untitled%207.png)

- If we are stuck somewhere, then we can execute `jarvis —help` to know the available list of commands.
- Both `jarvis check` and `jarvis update` command generate a packgeName.csv file, which can be used for later reference.
- Jarvis get’s a bit annoyed when someone tests it with a package which is not present in the given repository links.

![Untitled](JARVIS%20CLI%20Tool%20b9d3df401ce749768b02867019def7c8/Untitled%208.png)

## Future works

- Need to make it more interactive.
- Encrypt the access token file.
- Releasing it as a Pypi project.

## Credits

- Thanks for this activity. It was fun.
- And Hats off to the person who wrote that notion instruction. It was really creative. Please give them a hike.
- I must finally thank stackoverflow, for helping me when I am stuck.
