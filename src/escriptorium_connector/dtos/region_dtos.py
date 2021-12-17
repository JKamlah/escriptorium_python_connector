from escriptorium_connector.utils.pydantic_dataclass_fix import dataclass
from typing import List


@dataclass(init=True, frozen=True)
class GetRegionType:
    pk: int
    name: str


@dataclass(init=True, frozen=True)
class GetRegion:
    pk: int
    document_part: int
    external_id: str
    order: int
    box: List[List[int]]
    typology: int
