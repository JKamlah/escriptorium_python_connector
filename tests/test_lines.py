# region global setup

from tests.helpers import PrepForPartTest
from escriptorium_connector.dtos import PostLine, PutLine
from deepdiff import DeepDiff

# endregion

# Try CRUD operations on the parts endpoint
def test_lines():
    with PrepForPartTest() as (escr, new_document, new_part):
        new_line_id = "test-line-id"
        new_line_data = PostLine(
            document_part=new_part.pk,
            external_id=new_line_id,
            baseline=[[10, 10], [30, 10]],
            mask=[[0, 0], [0, 30], [40, 30], [40, 0], [0, 0]],
        )
        new_line = escr.create_document_part_line(
            new_document.pk, new_part.pk, new_line_data
        )

        assert new_line_id == new_line.external_id
        assert new_part.pk == new_line.document_part
        assert not DeepDiff(new_line_data.baseline, new_line.baseline)
        assert not DeepDiff(new_line_data.mask, new_line.mask)

        # Ensure that the line is accessible in get lines
        all_lines = (escr.get_document_part_lines(new_document.pk, new_part.pk)).results
        matching_lines = [x for x in all_lines if x.pk == new_line.pk]
        assert len(matching_lines) > 0
        assert not DeepDiff(new_line, matching_lines[0])

        # Check updating
        updated_line_id = "updated-line-id"
        updated_line_data = PutLine(
            document_part=new_part.pk,
            external_id=updated_line_id,
            baseline=[[100, 100], [300, 100]],
            mask=[[0, 0], [0, 300], [400, 300], [400, 0], [0, 0]],
        )
        updated_line = escr.update_document_part_line(
            new_document.pk, new_part.pk, new_line.pk, updated_line_data
        )

        assert updated_line_id == updated_line.external_id
        assert new_part.pk == updated_line.document_part
        assert not DeepDiff(updated_line_data.baseline, updated_line.baseline)
        assert not DeepDiff(updated_line_data.mask, updated_line.mask)

        # Check deletion
        escr.delete_document_part_line(new_document.pk, new_part.pk, new_line.pk)
        all_lines2 = (
            escr.get_document_part_lines(new_document.pk, new_part.pk)
        ).results
        matching_lines = [x for x in all_lines2 if x.pk == new_line.pk]
        assert len(matching_lines) == 0
