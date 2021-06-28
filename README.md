[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]

# Escriptorium Connector

This simple python package makes it easy to connect to escriptorium and work with the data stored there.

## Installation

And the obligatory: `pip install escriptorium-connector`
## Usage

If you are working on a public repository, you will probably want to store your user token in a hidden `.env` file that does not get distributed with your code. This is pretty easy to accomplish with [python-dotenv](https://pypi.org/project/python-dotenv/). You can get your user token by going to your eScriptorium instance (perhaps https://escriptorium.fr/), logging in, clicking on your username then "profile", and selecting "Api key". The token is a fairly long string of random letters and numbers.

The `EscriptoriumConnector` class provides (or will provide) all the methods needed to interact programmatically with the eScriptorium platform.

Example usage:

```python
from escriptorium_connector import EscriptoriumConnector
import os
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv()
    url = os.getenv('ESCRIPTORIUM_URL')
    api = f'{url}api/'
    token = os.getenv('ESCRIPTORIUM_TOKEN')
    escr = EscriptoriumConnector(url, api, token)
    print(escr.get_documents())

```

And your `.env` file should have:

```txt
ESCRIPTORIUM_URL=https://www.escriptorium.fr/
ESCRIPTORIUM_TOKEN='your secret user token here'
```