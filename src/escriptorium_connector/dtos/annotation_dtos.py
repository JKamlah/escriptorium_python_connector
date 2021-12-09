from enum import Enum
from typing import List
from dataclasses import field
from escriptorium_connector.utils.pydantic_dataclass_fix import dataclass

from escriptorium_connector.dtos.super_dtos import PagenatedResponse


class TextMarkerType(str, Enum):
    BACKGROUNDCOLOR = "Background Color"
    TEXTCOLOR = "Text Color"
    BOLD = "Bold"
    ITALIC = "Italic"


@dataclass(init=True, frozen=True)
class PostTypology:
    name: str


@dataclass(init=True, frozen=True)
class GetTypology:
    pk: int
    name: str


@dataclass(init=True, frozen=True)
class PostComponent:
    name: str
    allowed_values: List[str]


@dataclass(init=True, frozen=True)
class GetComponent:
    pk: int
    name: str
    allowed_values: List[str]


@dataclass(init=True, frozen=True)
class PostAnnotationTaxonomy:
    document: int
    name: str
    marker_type: TextMarkerType
    marker_detail: str
    has_comments: bool
    typology: PostTypology
    components: List[PostComponent] = field(default_factory=list)


@dataclass(init=True, frozen=True)
class GetAnnotationTaxonomy:
    pk: int
    document: int
    name: str
    marker_type: TextMarkerType
    marker_detail: str
    has_comments: bool
    typology: GetTypology
    components: List[GetComponent] = field(default_factory=list)


@dataclass
class GetAnnotationTaxonomies(PagenatedResponse):
    results: List[GetAnnotationTaxonomy] = field(default_factory=list)
