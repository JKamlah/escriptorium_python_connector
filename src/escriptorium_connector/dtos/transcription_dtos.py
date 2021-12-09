from escriptorium_connector.utils.pydantic_dataclass_fix import dataclass


@dataclass(init=True, frozen=True)
class GetTranscription:
    pk: int
    name: str
