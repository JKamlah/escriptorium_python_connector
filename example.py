from src.escriptorium_connector import EscriptoriumConnector
import os
from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()
    source_url = str(os.getenv("ESCRIPTORIUM_URL"))
    source_api = f"{source_url}api/"
    username = str(os.getenv("ESCRIPTORIUM_USERNAME"))
    password = str(os.getenv("ESCRIPTORIUM_PASSWORD"))
    project = str(os.getenv("ESCRIPTORIUM_PROJECT"))
    source = EscriptoriumConnector(source_url, source_api, username, password, project)
    print(source.get_documents())
    print(source.http.headers)
