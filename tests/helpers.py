# region global setup

from dotenv import load_dotenv
import os
import sys
import random
import string
from typing import Tuple, Union
import pkg_resources
from pathlib import Path

sys.path.append("../src")
from escriptorium_connector import EscriptoriumConnector
from escriptorium_connector.dtos import (
    PostProject,
    GetDocument,
    PostDocument,
    GetPart,
    PostPart,
    ReadDirection,
    LineOffset,
)

load_dotenv()
url = os.getenv("ESCRIPTORIUM_URL")
username = os.getenv("ESCRIPTORIUM_USERNAME")
password = os.getenv("ESCRIPTORIUM_PASSWORD")

if url is None or username is None or password is None:
    sys.exit()

# endregion


def get_random_string(length: int) -> str:
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def get_connector() -> EscriptoriumConnector:
    return EscriptoriumConnector(url, username, password)


def get_user_id(escr: EscriptoriumConnector) -> int:
    user_details = escr.get_user()
    return user_details.count


def create_project(escr: EscriptoriumConnector, project_name: str) -> Union[int, None]:
    all_projects = (escr.get_projects()).results
    requested_project = [x for x in all_projects if x.name == project_name]
    if requested_project:
        return requested_project[0].id

    new_project_data = PostProject(
        name=project_name,
        shared_with_groups=[],
        shared_with_users=[],
    )
    new_project = escr.create_project(new_project_data)
    if new_project.slug != ["project with this slug already exists."]:
        return new_project.id

    return -1


def create_document(escr: EscriptoriumConnector, document_name: str) -> GetDocument:
    project_name = "pytest-suite-2"
    proj_id = create_project(escr, project_name)
    assert proj_id is not None

    new_document = PostDocument(
        name=document_name,
        project=project_name,
        main_script="Latin",
        read_direction=ReadDirection.LTR,
        line_offset=LineOffset.BASELINE,
        tags=[],
    )
    new_doc = escr.create_document(new_document)
    return new_doc


class PrepForDocumentTest(object):
    def __init__(self, doc_name: Union[str, None] = None):
        # auto-create the connector and the document
        self.connector = get_connector()
        doc_name = doc_name if doc_name is not None else "test-" + get_random_string(6)
        self.new_doc = create_document(self.connector, doc_name)

    def __enter__(self) -> Tuple[EscriptoriumConnector, GetDocument]:
        return (self.connector, self.new_doc)

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            # if document still exists, delete it
            if self.new_doc is not None:
                current_doc = self.connector.get_document(self.new_doc.pk)
                self.connector.delete_document(current_doc.pk)
        except:
            # if it is gone, do nothing
            pass


class PrepForPartTest(object):
    def __init__(
        self,
        doc_name: Union[str, None] = None,
        part_name: Union[str, None] = None,
        part_source: Union[str, None] = None,
        image_name: Union[str, None] = None,
        filedata: Union[bytes, None] = None,
    ):
        # auto-create the connector and the document
        self.connector = get_connector()
        doc_name = (
            doc_name if doc_name is not None else "test-doc-" + get_random_string(6)
        )
        part_name = (
            part_name if part_name is not None else "test-part-" + get_random_string(6)
        )
        part_source = (
            part_source
            if part_source is not None
            else "test-source-" + get_random_string(6)
        )
        image_name = (
            image_name if image_name is not None else "Cod._Sangallensis_63_(277).jpg"
        )
        filedata = (
            filedata
            if filedata is not None
            else Path(
                pkg_resources.resource_filename("tests.resources", image_name)
            ).read_bytes()
        )
        self.new_doc = create_document(self.connector, doc_name)
        new_part_info = PostPart(name=part_name, typology=None, source=part_source)
        self.new_part = self.connector.create_document_part(
            self.new_doc.pk, new_part_info, image_name, filedata
        )

    def __enter__(self) -> Tuple[EscriptoriumConnector, GetDocument, GetPart]:
        return (self.connector, self.new_doc, self.new_part)

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            # if document still exists, delete it
            if self.new_doc is not None:
                current_doc = self.connector.get_document(self.new_doc.pk)
                self.connector.delete_document(current_doc.pk)
        except:
            # if it is gone, do nothing
            pass
