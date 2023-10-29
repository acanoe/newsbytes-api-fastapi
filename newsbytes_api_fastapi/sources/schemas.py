from pydantic import BaseModel


class GetSourcesResponse(BaseModel):
    sources: list[str]


class SetSourcesRequest(BaseModel):
    sources: list[str]


class SetSourcesResponse(BaseModel):
    message: str
