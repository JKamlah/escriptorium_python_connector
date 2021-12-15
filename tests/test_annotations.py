# region global setup

from escriptorium_connector.dtos import (
    PostComponent,
    TextMarkerType,
    PostTypology,
    PostAnnotationTaxonomy,
)
from .helpers import get_connector, create_document

# endregion


# TODO: update is not yet supported
def test_crud_component():
    escr = get_connector()
    new_document = create_document(escr, "component test document")
    new_component_name = "test_component"
    allowed_values = []
    doc_pk = new_document.pk

    # create the component
    new_component_data = PostComponent(
        document=doc_pk, name=new_component_name, allowed_values=allowed_values
    )
    new_component = escr.create_document_component(doc_pk, new_component_data)
    current_components = (escr.get_document_components(doc_pk)).results
    returned_new_component_matches = [
        x for x in current_components if x.pk == new_component.pk
    ]

    assert len(returned_new_component_matches) > 0

    returned_new_component = returned_new_component_matches[0]

    assert (
        new_component_name
        == returned_new_component.name
        == new_component.name
        == new_component_data.name
    )
    assert (
        returned_new_component.allowed_values
        == new_component.allowed_values
        == allowed_values
    )

    # delete the component
    escr.delete_document_component(doc_pk, new_component.pk)
    current_components = (escr.get_document_components(doc_pk)).results
    returned_new_component_matches = [
        x for x in current_components if x.pk == new_component.pk
    ]

    assert len(returned_new_component_matches) == 0

    escr.delete_document(doc_pk)


# TODO: add update test
def test_create_and_delete_annotation_types():
    escr = get_connector()
    new_document = create_document(escr, "annotation test document")
    new_component_name = "test_component"
    allowed_values = []
    doc_pk = new_document.pk
    new_component_data = PostComponent(
        document=doc_pk, name=new_component_name, allowed_values=allowed_values
    )
    new_component = escr.create_document_component(doc_pk, new_component_data)

    annotation_name = "test annotation"
    annotation_marker_type = TextMarkerType.TEXTCOLOR
    has_comments = False
    typology = PostTypology(name="test typology")
    new_annotation_type_data = PostAnnotationTaxonomy(
        document=doc_pk,
        name=annotation_name,
        marker_type=annotation_marker_type,
        marker_detail="",
        has_comments=has_comments,
        typology=typology,
        components=[new_component.pk],
    )
    new_annotation_type = escr.create_document_annotation(
        doc_pk, new_annotation_type_data
    )
    current_annotation_types = (escr.get_document_annotations(doc_pk)).results
    returned_new_annotation_matches = [
        x for x in current_annotation_types if x.pk == new_annotation_type.pk
    ]

    assert len(returned_new_annotation_matches) > 0

    returned_annotation_type = returned_new_annotation_matches[0]

    assert (
        returned_annotation_type.name
        == new_annotation_type.name
        == new_annotation_type_data.name
        == annotation_name
    )
    assert (
        returned_annotation_type.has_comments
        == new_annotation_type.has_comments
        == new_annotation_type_data.has_comments
    )
    assert (
        returned_annotation_type.marker_detail
        == new_annotation_type.marker_detail
        == new_annotation_type_data.marker_detail
    )
    assert (
        returned_annotation_type.marker_type
        == new_annotation_type.marker_type
        == new_annotation_type_data.marker_type
    )
    assert (
        returned_annotation_type.typology.name
        == new_annotation_type.typology.name
        == new_annotation_type_data.typology.name
    )
    assert (
        returned_annotation_type.components[0]
        == new_annotation_type.components[0]
        == new_annotation_type_data.components[0]
    )

    # delete the component
    escr.delete_document_annotation(doc_pk, new_annotation_type.pk)
    current_annotation_types = (escr.get_document_annotations(doc_pk)).results
    returned_new_annotation_matches = [
        x for x in current_annotation_types if x.pk == new_annotation_type.pk
    ]

    assert len(returned_new_annotation_matches) == 0

    escr.delete_document(doc_pk)
