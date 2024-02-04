from typing import List, Sequence, Union
import openai


def retry_on_error(func):
    def wrapper(*args, **kwargs):
        retry = 0
        while True:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if retry > 3:
                    raise e
                retry += 1

    return wrapper


@retry_on_error
def embed_query(query: str) -> Sequence[float]:
    client = openai.Client(timeout=5)
    response = client.embeddings.create(
        model="text-embedding-ada-002", input=query, encoding_format="float"
    )
    return response.data[0].embedding


@retry_on_error
def embed_queries(query: Union[str, List[str]]) -> List[Sequence[float]]:
    client = openai.Client(timeout=5)
    response = client.embeddings.create(
        model="text-embedding-ada-002", input=query, encoding_format="float"
    )
    return [data.embedding for data in response.data]
