from typing import TypedDict
from app.database.client import SingletonChromaClient


class GorokuCollection:
    client: SingletonChromaClient

    def __init__(self) -> None:
        self.client = SingletonChromaClient()
        self.collection = self.client.chroma_client.get_collection("goroku")


class GorokuCollectionMetaData(TypedDict):
    meme: str
    natural: str
    description: str
    use_case: str
    hit_count: int
    unlike_count: int
