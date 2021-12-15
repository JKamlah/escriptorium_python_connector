# region global setup

from dotenv import load_dotenv
import os
import sys

sys.path.append("../src")
from escriptorium_connector import EscriptoriumConnector
from escriptorium_connector.dtos import (
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

# endregion


def get_connector() -> EscriptoriumConnector:
    return EscriptoriumConnector(url, username, password)


def get_user_id(escr: EscriptoriumConnector) -> int:
    user_details = escr.get_user()
    return user_details.count


def create_project(escr: EscriptoriumConnector, project_name: str) -> int:
    all_projects = (escr.get_projects()).results
    requested_project = [x for x in all_projects if x.name == project_name]
    if requested_project:
        return requested_project[0].id

    new_project_data = PostProject(
        name=project_name,
        slug=project_name,
        owner=get_user_id(escr),
        shared_with_groups=[],
        shared_with_users=[],
    )
    new_project = escr.create_project(new_project_data)
    if new_project.slug != ["project with this slug already exists."]:
        return new_project.id

    return -1


def create_document(escr: EscriptoriumConnector, document_name: str) -> GetDocument:
    project_name = "pytest-suite-2"
    _ = create_project(escr, project_name)
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
