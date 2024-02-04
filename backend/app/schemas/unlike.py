from typing import Literal
from pydantic import BaseModel


class PostUnlikeRequest(BaseModel):
    id: str


class PostUnlikeResponse(BaseModel):
    status: Literal["ok", "failed"]
