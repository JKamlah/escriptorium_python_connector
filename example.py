from src.escriptorium_connector import EscriptoriumConnector
import os
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv()
    url = os.getenv('ESCRIPTORIUM_URL')
    api = f'{url}api/'
    token = os.getenv('ESCRIPTORIUM_TOKEN')
    escr = EscriptoriumConnector(url, api, token)
    print(escr.get_documents())