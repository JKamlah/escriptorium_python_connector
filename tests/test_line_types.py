# TODO: the line typology support in the REST API
# is not currently working properly. Come back to this
# when the API is fixed.

# region global setup

from tests.helpers import get_connector
from escriptorium_connector.dtos import PostLineType
from deepdiff import DeepDiff

# endregion

# # Try CRUD operations on the parts endpoint
# def test_line_types():
#     # Create a new line type
#     escr = get_connector()
#     new_line_type_data = PostLineType(name="test-line-type")
#     new_line_type = escr.create_line_type(new_line_type_data)

#     assert new_line_type.name == new_line_type_data.name
#     assert new_line_type.pk >= 0

#     # Get line types and make sure new one is included
#     retrieved_line_types = escr.get_line_type(new_line_type.pk)
#     assert not DeepDiff(new_line_type, retrieved_line_types)

#     # Update the line type
#     updated_line_type_data = PostLineType(name="updated-line-type")
#     updated_line_type = escr.update_line_type(new_line_type.pk, updated_line_type_data)
#     assert updated_line_type_data.name == updated_line_type.name
#     assert new_line_type.pk == updated_line_type.pk

#     # Delete the line type
#     escr.delete_line_type(new_line_type.pk)
#     error = None
#     try:
#         retrieved_line_types = escr.get_line_type(new_line_type.pk)
#     except Exception as e:
#         error = e
#     assert error is not None
