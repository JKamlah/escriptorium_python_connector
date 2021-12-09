from dataclasses import dataclass
from datetime import datetime
from typing import List, Union, Any

from .super_dtos import PagenatedResponse
from .utils import iso_string_date_to_datetime


@dataclass
class PostProject:
    name: str
    slug: str
    owner: int
    shared_with_users: List[int]
    shared_with_groups: List[int]


@dataclass
class PutProject:
    name: str
    slug: str
    owner: int
    shared_with_users: List[int]
    shared_with_groups: List[int]


@dataclass
class GetProject:
    id: int
    name: str
    slug: str
    created_at: datetime
    updated_at: datetime
    owner: int
    shared_with_users: List[int]
    shared_with_groups: List[int]

    def __init__(
        self,
        id: int,
        name: str,
        slug: str,
        created_at: str,
        updated_at: str,
        owner: int,
        shared_with_users: List[int],
        shared_with_groups: List[int],
    ):
        self.id = id
        self.name = name
        self.slug = slug
        self.created_at = iso_string_date_to_datetime(created_at)
        self.updated_at = iso_string_date_to_datetime(updated_at)
        self.owner = owner
        self.shared_with_users = shared_with_users
        self.shared_with_groups = shared_with_groups


@dataclass
class GetProjects(PagenatedResponse):
    results: List[GetProject]

    def __init__(
        self,
        count: int,
        next: Union[str, None],
        previous: Union[str, None],
        results: List[Any] = [],
    ):
        super(GetProjects, self).__init__(count, next, previous)
        self.results = [GetProject(**x) for x in results]
