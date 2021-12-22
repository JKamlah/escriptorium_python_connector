# region global setup

from escriptorium_connector.dtos.document_dtos import PutDocument
from .helpers import PrepForDocumentTest
from escriptorium_connector.dtos import ReadDirection, LineOffset
from deepdiff import DeepDiff

# endregion

# Try CRUD operations on the documents endpoint
def test_documents():
    with PrepForDocumentTest() as (escr, new_document):
        # Get the document list to see if the new document is there
        documents = escr.get_documents()

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

        # Attempt a put request
        updated_name = "updated-test-name"
        updated_main_script = "Arabic"
        updated_read_direction = ReadDirection.RTL
        updated_line_offset = LineOffset.CENTERED
        updated_tags = []
        # TODO: test changing the project and adding a tag
        updated_data = PutDocument(
            name=updated_name,
            project=new_document.project,
            main_script=updated_main_script,
            read_direction=updated_read_direction,
            line_offset=updated_line_offset,
            tags=updated_tags,
        )
        updated_doc = escr.update_document(new_document.pk, updated_data)

        assert DeepDiff(new_document, updated_doc)
        assert updated_name == updated_doc.name
        assert updated_main_script == updated_doc.main_script
        assert updated_read_direction == updated_doc.read_direction
        assert updated_line_offset == updated_doc.line_offset
        assert len(updated_tags) == len(updated_doc.tags)
        for tag in updated_tags:
            assert tag in updated_doc.tags
        assert new_document.pk == updated_doc.pk

        # Make sure that the document deletion was successfull
        escr.delete_document(new_document.pk)
        documents = escr.get_documents()
        matched_documents = [x for x in documents.results if x.pk == new_document.pk]
        assert len(matched_documents) == 0
