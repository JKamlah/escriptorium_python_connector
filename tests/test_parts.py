# region global setup

from tests.helpers import PrepForDocumentTest
from escriptorium_connector.dtos import PostPart, PutPart
from deepdiff import DeepDiff
import pkg_resources
from pathlib import Path

# endregion

# Try CRUD operations on the parts endpoint
def test_parts():
    with PrepForDocumentTest() as (escr, new_document):
        image_filename = "Cod._Sangallensis_63_(277).jpg"
        image_file = Path(
            pkg_resources.resource_filename("tests.resources", image_filename)
        )
        image_filesize = image_file.stat().st_size
        new_part_info = PostPart(
            name="test-part",
            typology=None,
            source="https://en.wikipedia.org/wiki/Vulgate#/media/File:Cod._Sangallensis_63_(277).jpg",
        )

        # Create the new part
        new_part = escr.create_document_part(
            new_document.pk, new_part_info, image_filename, image_file.read_bytes()
        )

        assert new_part.pk >= 0
        assert new_part_info.name == new_part.name
        assert new_part_info.typology == new_part.typology
        assert new_part_info.source == new_part.source
        assert image_filename == new_part.filename
        assert 0 == new_part.order
        assert image_filesize == new_part.image_file_size

        # Make sure we can get the image and it hasn't been changed
        downloaded_image = escr.get_document_part_image(new_document.pk, new_part.pk)
        assert downloaded_image == image_file.read_bytes()

        small_thumbnail = escr.get_document_part_thumbnail(
            new_document.pk, new_part.pk, False
        )
        assert len(small_thumbnail) > 2
        # Verify JPG magic number at beginning
        assert small_thumbnail[:2] == b"\xff\xd8"
        # Verify JPG magic number at end
        assert small_thumbnail[-2:] == b"\xff\xd9"

        large_thumbnail = escr.get_document_part_thumbnail(
            new_document.pk, new_part.pk, True
        )
        assert len(large_thumbnail) > 2
        # Verify JPG magic number at beginning
        assert large_thumbnail[:2] == b"\xff\xd8"
        # Verify JPG magic number at end
        assert large_thumbnail[-2:] == b"\xff\xd9"

        # Perform update
        # TODO: test the typology
        updated_part_name = "my-updated-part"
        updated_source = "blank-source"
        updated_part_info = PutPart(
            name=updated_part_name, typology=None, source=updated_source
        )
        updated_part = escr.update_document_part(
            new_document.pk, new_part.pk, updated_part_info
        )

        assert DeepDiff(new_part, updated_part)
        assert new_part.pk == updated_part.pk
        assert new_part.filename == updated_part.filename
        assert new_part.bw_image == updated_part.bw_image
        assert new_part.image.size == updated_part.image.size
        assert new_part.image.uri == updated_part.image.uri
        # I test downloaded the thumbnails above, no need to test here
        assert new_part.image_file_size == updated_part.image_file_size
        assert new_part.recoverable == updated_part.recoverable
        assert not DeepDiff(new_part.regions, updated_part.regions)

        assert updated_part_name == updated_part.name
        assert updated_source == updated_part.source
        assert updated_part.typology is None

        # Delete it (use the "by index" method for more complete testing)
        # Test some illegal deletes first
        escr.delete_document_parts_by_index(new_document.pk, 20, 3)
        all_parts = (escr.get_document_parts(new_document.pk)).results
        matching_parts = [x for x in all_parts if x.pk == new_part.pk]
        assert len(matching_parts) == 1

        escr.delete_document_parts_by_index(new_document.pk, 19, 20)
        all_parts = (escr.get_document_parts(new_document.pk)).results
        matching_parts = [x for x in all_parts if x.pk == new_part.pk]
        assert len(matching_parts) == 1

        escr.delete_document_parts_by_index(
            new_document.pk, new_part.order, new_part.order + 1
        )
        all_parts = (escr.get_document_parts(new_document.pk)).results
        matching_parts = [x for x in all_parts if x.pk == new_part.pk]
        assert len(matching_parts) == 0
