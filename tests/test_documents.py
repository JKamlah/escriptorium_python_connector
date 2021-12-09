# region global setup

from dotenv import load_dotenv
import os
import sys

sys.path.append("../src")
from escriptorium_connector import EscriptoriumConnector
from escriptorium_connector.dtos import (
    GetProject,
    PostProject,
    GetDocument,
    PostDocument,
    ReadDirection,
    LineOffset,
)

load_dotenv()
url = os.getenv("ESCRIPTORIUM_URL")
username = os.getenv("ESCRIPTORIUM_USERNAME")
password = os.getenv("ESCRIPTORIUM_PASSWORD")

if url is None or username is None or password is None:
    sys.exit()


def get_connector() -> EscriptoriumConnector:
    return EscriptoriumConnector(url, username, password)


escr = get_connector()
# endregion


def get_user_id() -> int:
    user_details = escr.get_user()
    return user_details.count


def create_project(project_name: str) -> int:
    all_projects = (escr.get_projects()).results
    requested_project = [x for x in all_projects if x.name == project_name]
    if requested_project:
        return requested_project[0].id

    new_project_data = PostProject(project_name, project_name, get_user_id(), [], [])
    new_project = escr.create_project(new_project_data)
    if new_project.slug != ["project with this slug already exists."]:
        return new_project.id

    return -1


def create_document(document_name) -> GetDocument:
    project_name = "pytest-suite-2"
    _ = create_project(project_name)
    new_document = PostDocument(
        document_name, project_name, "Latin", ReadDirection.LTR, LineOffset.BASELINE, []
    )
    new_doc = escr.create_document(new_document)
    return new_doc


def test_get_documents():
    new_document = create_document("my document")
    documents = escr.get_documents()
    assert len(documents.results) > 0

    matched_documents = [x for x in documents.results if x.pk == new_document.pk]
    assert len(matched_documents) == 1

    matched_document = matched_documents[0]
    assert matched_document.parts_count == new_document.parts_count
    assert matched_document.created_at == new_document.created_at
    assert matched_document.line_offset == new_document.line_offset
    assert matched_document.main_script == new_document.main_script
    assert matched_document.project == new_document.project
    assert matched_document.read_direction == new_document.read_direction


test_get_documents()
