from typing import Literal, Optional
from pydantic import BaseModel, Field


class PostAddRequest(BaseModel):
    word: str = Field(description="変換前の一般的な表現の単語。")
    correspond_to: str = Field(description="変換後の単語。語録やミーム。")
    use_case: str = Field(description="変換後の単語の用例。")
    description: str = Field(description="変換後の単語の説明。")


class PostAddResponse(BaseModel):
    status: Literal["success", "failed"] = Field(description="追加の成否。")
    message: Optional[str] = Field(description="追加のメッセージ。")
