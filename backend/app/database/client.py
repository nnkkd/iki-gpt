import os
from typing import Optional
import chromadb
from chromadb.api import ClientAPI
from chromadb.config import Settings


class SingletonChromaClient:
    _instance: Optional["SingletonChromaClient"] = None
    chroma_client: ClientAPI

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonChromaClient, cls).__new__(cls)
            cls._instance.chroma_client = chromadb.HttpClient(
                host=os.environ["DB_HOST"],
                port=os.environ["DB_PORT"],
                ssl=False,
                settings=Settings(
                    anonymized_telemetry=False,
                ),
            )

        return cls._instance


def get_chroma_client():
    return SingletonChromaClient()
