from typing import List, Optional
from pydantic import BaseModel, Field


class PostSearchRequest(BaseModel):
    query: str = Field(description="変換したい文章。")


class Correspondence(BaseModel):
    id: str = Field(description="ID")
    word: str = Field(description="変換前の一般的な表現の単語。")
    correspond_to: str = Field(description="変換後の単語。")
    use_case: Optional[str] = Field(description="変換後の単語の用例。")


class PostSearchResponse(BaseModel):
    correspondences: List[Correspondence] = Field(description="単語変換表。")
