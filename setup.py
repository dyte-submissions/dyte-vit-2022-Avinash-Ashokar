from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
    
setup(
    name = 'jarvis',
    version = '0.0.1',
    author = 'Avinash A',
    author_email = 'mail_avinashashokar@pm.me',
    license = 'GNU General Public License v3.0>',
    description = 'A tool made to solve Deprecated libraries',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/Avinash-Ashokar/Avinash-Ashokar',
    py_modules = ['jarvis', 'app'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points = '''
        [console_scripts]
        jarvis=jarvis:cli
    '''
)