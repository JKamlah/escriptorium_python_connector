[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]

# Escriptorium Connector

This simple python package makes it easy to connect to escriptorium and work with the data stored there.

## Installation

And the obligatory: `pip install escriptorium-connector`
## Usage

If you are working on a public repository, you will probably want to store your user credentials in a hidden `.env` file that does not get distributed with your code. This is pretty easy to accomplish with [python-dotenv](https://pypi.org/project/python-dotenv/). You will need to provide the connector with an eScriptorium instance URL, the API URL, your username, and your password (see below).

The `EscriptoriumConnector` class provides (or will provide) all the methods needed to interact programmatically with the eScriptorium platform.

Example usage:

```python
from escriptorium_connector import EscriptoriumConnector
import os
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv()
    url = str(os.getenv('ESCRIPTORIUM_URL'))
    api = f'{url}api/'
    username = str(os.getenv('ESCRIPTORIUM_USERNAME'))
    password = str(os.getenv('ESCRIPTORIUM_PASSWORD'))
    escr = EscriptoriumConnector(url, api, username, password)
    print(escr.get_documents())

```

And your `.env` file should have:

```txt
ESCRIPTORIUM_URL=https://www.escriptorium.fr/
ESCRIPTORIUM_USERNAME=your escriptorium username
ESCRIPTORIUM_PASSWORD=your escriptorium password
```

See [this Jupyter notebook](./example.ipynb) for a longer introduction to the connector.