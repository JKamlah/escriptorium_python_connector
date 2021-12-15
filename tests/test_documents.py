# region global setup

from .helpers import get_connector, create_document

# endregion


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
