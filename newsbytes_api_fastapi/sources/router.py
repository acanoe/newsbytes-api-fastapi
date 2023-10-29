from typing import Annotated

from fastapi import APIRouter, Path

from ..schemas import News
from .schemas import GetSourcesResponse, SetSourcesRequest, SetSourcesResponse

sources_router = APIRouter(prefix="/sources")


@sources_router.get("/", response_model=GetSourcesResponse)
def get_sources():
    return GetSourcesResponse(sources=["progscrape", "rss"])


@sources_router.post("/", response_model=SetSourcesResponse)
def set_sources(sources: SetSourcesRequest):
    return SetSourcesResponse(message="Sources set")


@sources_router.get("/{source}", response_model=News)
def get_source_items(
    source: Annotated[str, Path(title="The source to get items from")]
):
    return News(stories=[], tags=[])
