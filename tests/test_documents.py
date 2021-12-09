# region global setup

from escriptorium_connector.connector import EscriptoriumConnector
from escriptorium_connector.dtos import (
    GetProject,
    PostProject,
    GetDocument,
    PostDocument,
    ReadDirection,
    LineOffset,
)
from .helpers import get_connector

# endregion


def get_user_id(escr: EscriptoriumConnector) -> int:
    user_details = escr.get_user()
    return user_details.count


def create_project(escr: EscriptoriumConnector, project_name: str) -> int:
    all_projects = (escr.get_projects()).results
    requested_project = [x for x in all_projects if x.name == project_name]
    if requested_project:
        return requested_project[0].id

    new_project_data = PostProject(
        project_name, project_name, get_user_id(escr), [], []
    )
    new_project = escr.create_project(new_project_data)
    if new_project.slug != ["project with this slug already exists."]:
        return new_project.id

    return -1


def create_document(escr: EscriptoriumConnector, document_name: str) -> GetDocument:
    project_name = "pytest-suite-2"
    _ = create_project(escr, project_name)
    new_document = PostDocument(
        document_name, project_name, "Latin", ReadDirection.LTR, LineOffset.BASELINE, []
    )
    new_doc = escr.create_document(new_document)
    return new_doc


def test_get_documents():
    escr = get_connector()
    # Create the document
    new_document = create_document(escr, "my document")

    # Get the document list to see if the new document is there
    documents = escr.get_documents()

    # Immediately delete the new doc before running checks
    escr.delete_document(new_document.pk)
    assert len(documents.results) > 0

    # Check to see if the new doc is in the document list
    matched_documents = [x for x in documents.results if x.pk == new_document.pk]
    assert len(matched_documents) == 1

    # Make sure the new document was returned with the correct data
    matched_document = matched_documents[0]
    assert matched_document.parts_count == new_document.parts_count
    assert matched_document.created_at == new_document.created_at
    assert matched_document.line_offset == new_document.line_offset
    assert matched_document.main_script == new_document.main_script
    assert matched_document.project == new_document.project
    assert matched_document.read_direction == new_document.read_direction

    # Make sure that the document deletion was successfull
    documents = escr.get_documents()
    matched_documents = [x for x in documents.results if x.pk == new_document.pk]
    assert len(matched_documents) == 0
