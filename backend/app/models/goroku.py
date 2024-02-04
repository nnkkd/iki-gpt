from pydantic import BaseModel


class GorokuMetadata(BaseModel):
    word: str
    description: str
    use_case: str
