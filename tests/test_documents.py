# region global setup

from dotenv import load_dotenv
import os
import sys

sys.path.append("../src")
from escriptorium_connector import (
    EscriptoriumConnector,
    PostDocument,
    ReadDirection,
    LineOffset,
)
from escriptorium_connector.models.document_models import GetDocument

load_dotenv()
url = os.getenv("ESCRIPTORIUM_URL")
api = f"""{url}api"""
username = os.getenv("ESCRIPTORIUM_USERNAME")
password = os.getenv("ESCRIPTORIUM_PASSWORD")

if url is None or username is None or password is None:
    sys.exit()


def get_connector() -> EscriptoriumConnector:
    return EscriptoriumConnector(url, api, username, password)


# endregion


def create_document() -> GetDocument:
    escr = get_connector()
    new_document = PostDocument(
        "test-doc", "test-1", "Latin", ReadDirection.LTR, LineOffset.BASELINE, []
    )
    # import requests
    # try:
    #     r = requests.post(
    #         f"{api}/documents/", json=new_document.__dict__, headers=escr.http.headers
    #     )
    #     r.raise_for_status()
    # except requests.HTTPError as err:
    #     error_msg = r.text
    #     print(error_msg)
    new_doc = escr.create_document(new_document)
    return new_doc


create_document()


def test_get_documents():
    escr = get_connector()
    documents = escr.get_documents()
    assert len(documents.results) == 0
