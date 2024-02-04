from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPBasicCredentials

from app.schemas.search import PostSearchRequest, PostSearchResponse
from app.crud.goroku import GorokuCollection
from app.services.add import add
from app.auth.auth import get_current_username
from app.services.search import search
import logging

from app.schemas.add import PostAddRequest, PostAddResponse
from app.services.unlike import unlike
from app.schemas.unlike import PostUnlikeRequest, PostUnlikeResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/search", response_model=PostSearchResponse, description="文章に関連するミームの検索を行います。"
)
async def search_router(
    query: str,
    username: Annotated[str, Depends(get_current_username)],
    collection: GorokuCollection = Depends(GorokuCollection),
):
    res = await search(query, collection)
    return res


@router.post("/add", response_model=PostAddResponse, description="文章に関連するミームの追加を行います。")
async def add_router(
    body: PostAddRequest,
    username: Annotated[str, Depends(get_current_username)],
    collection: GorokuCollection = Depends(GorokuCollection),
):
    return await add(body, collection)


@router.post(
    "/unlike",
    response_model=PostUnlikeResponse,
    description="idを指定することで、検索時にヒットする可能性を減らすことができます。",
)
async def unlike_router(
    body: PostUnlikeRequest,
    username: Annotated[str, Depends(get_current_username)],
    collection: GorokuCollection = Depends(GorokuCollection),
):
    return await unlike(body.id, collection)
