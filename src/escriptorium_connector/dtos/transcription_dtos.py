from escriptorium_connector.utils.pydantic_dataclass_fix import dataclass
from typing import Union, List
from datetime import datetime


@dataclass(init=True, frozen=True)
class GetAbbreviatedTranscription:
    pk: int
    name: str


@dataclass(init=True, frozen=True)
class GetTranscription:
    pk: int
    line: int
    transcription: int
    content: str
    versions: List[str]  # TODO: Check that this is correct
    version_author: str
    version_source: str
    version_updated_at: datetime
    graphs: Union[str, None] = None
