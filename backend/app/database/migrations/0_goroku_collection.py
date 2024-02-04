import os
from dotenv import load_dotenv
from app.database.client import SingletonChromaClient

load_dotenv(".env")
print(os.environ["DB_PORT"])


def up():
    client = SingletonChromaClient()
    client.chroma_client.create_collection("goroku", metadata={"hnsw:space": "cosine"})


def down():
    client = SingletonChromaClient()
    client.chroma_client.delete_collection("goroku")
    client.chroma_client.delete_collection("goroku_unchecked")


up()
