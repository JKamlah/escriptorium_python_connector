from dataclasses import field
from escriptorium_connector.utils.pydantic_dataclass_fix import dataclass
from enum import Enum
from typing import List, Union
from datetime import datetime

from escriptorium_connector.dtos.super_dtos import PagenatedResponse
from escriptorium_connector.dtos.transcription_dtos import GetAbbreviatedTranscription
from escriptorium_connector.dtos.region_dtos import GetRegionType
from escriptorium_connector.dtos.line_dtos import GetLineType, GetPartType
from dateutil.parser import isoparse

class ReadDirection(str, Enum):
    LTR = "ltr"
    RTL = "rtl"


class LineOffset(int, Enum):
    BASELINE = 0
    TOPLINE = 1
    CENTERED = 2


@dataclass(init=True, frozen=True)
class PostDocument:
    name: str
    project: str
    main_script: Union[str, None]
    read_direction: ReadDirection
    line_offset: LineOffset
    tags: List[str] = field(default_factory=list)


@dataclass(init=True, frozen=True)
class PutDocument:
    name: str
    project: str
    main_script: Union[str, None]
    read_direction: ReadDirection
    line_offset: LineOffset
    tags: List[str] = field(default_factory=list)


from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass(init=True, frozen=True)
class GetAbbreviatedTranscription:
    pk: int
    name: str
    archived: bool
    avg_confidence: Optional[float]


@dataclass(init=True, frozen=True)
class GetRegionType:
    pk: int
    name: str


@dataclass(init=True, frozen=True)
class GetLineType:
    pk: int
    name: str


@dataclass(init=True, frozen=True)
class GetPartType:
    pk: int
    name: str


@dataclass(init=True, frozen=True)
class GetDocument:
    pk: int
    name: str
    project: str
    main_script: Optional[str]
    read_direction: ReadDirection
    line_offset: LineOffset
    parts_count: int
    created_at: datetime
    updated_at: datetime
    transcriptions: List[GetAbbreviatedTranscription] = field(default_factory=list)
    valid_block_types: List[GetRegionType] = field(default_factory=list)
    valid_line_types: List[GetLineType] = field(default_factory=list)
    valid_part_types: List[GetPartType] = field(default_factory=list)
    tags: List[int] = field(default_factory=list)
    show_confidence_viz: bool = False

@dataclass
class GetDocuments(PagenatedResponse):
    results: List[GetDocument] = field(default_factory=list)

# --- Parser-Funktionen ---
def parse_document(data: dict) -> GetDocument:
    return GetDocument(
        pk=data["pk"],
        name=data["name"],
        project=data["project"],
        main_script=data.get("main_script"),
        read_direction=ReadDirection(data["read_direction"]),
        line_offset=LineOffset(data["line_offset"]),
        parts_count=data["parts_count"],
        created_at=isoparse(data["created_at"]),
        updated_at=isoparse(data["updated_at"]),
        transcriptions=[GetAbbreviatedTranscription(**t) for t in data.get("transcriptions", [])],
        valid_block_types=[GetRegionType(**b) for b in data.get("valid_block_types", [])],
        valid_line_types=[GetLineType(**l) for l in data.get("valid_line_types", [])],
        valid_part_types=[GetPartType(**p) for p in data.get("valid_part_types", [])],
        tags=data.get("tags", []),
        show_confidence_viz=data.get("show_confidence_viz", False)
    )


def parse_documents(data: dict) -> GetDocuments:
    return GetDocuments(
        count=data["count"],
        next=data.get("next"),
        previous=data.get("previous"),
        results=[parse_document(d) for d in data.get("results", [])],
    )
