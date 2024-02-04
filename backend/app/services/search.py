import logging
import random
from typing import Dict, List, Sequence

from app.crud.goroku import GorokuCollection
from app.schemas.search import Correspondence, PostSearchResponse
from app.inference.embed import embed_queries


logger = logging.getLogger(__name__)


def evaluate_dislike(hit_count: int, unlike_count: int) -> float:
    if hit_count == 0:
        return 0
    return unlike_count / (hit_count + 1)


async def search(query: str, collection: GorokuCollection):
    # 15文字ごとに分割
    query_texts = [query[i : i + 30] for i in range(0, len(query), 30)]
    data: List[Sequence[float]] = embed_queries(query_texts)

    res = collection.collection.query(
        query_embeddings=data, include=["metadatas", "documents"]
    )
    logger.info(res["metadatas"])
    id_to_information: Dict[str, dict] = {}

    ids = res["ids"]
    documents = res["documents"] or []
    metadatas = res["metadatas"] or []
    for id, doc, meta in zip(ids, documents, metadatas):
        for i, d, m in zip(id, doc, meta):
            id_to_information[i] = {"document": d, "metadata": m}

    # dislikeに応じてフィルタリング
    id_to_information = {
        k: v
        for k, v in id_to_information.items()
        if evaluate_dislike(v["metadata"]["hit_count"], v["metadata"]["unlike_count"])
        < random.random()
    }

    # 一致したものを更新
    collection.collection.update(
        ids=list(id_to_information.keys()),
        metadatas=[
            {
                "hit_count": v["metadata"]["hit_count"] + 1,
            }
            for v in id_to_information.values()
        ],
    )

    return PostSearchResponse(
        correspondences=[
            Correspondence(
                id=k,
                word=v["metadata"]["natural"],
                correspond_to=v["metadata"]["meme"],
                use_case=v["metadata"]["use_case"],
            )
            for k, v in id_to_information.items()
        ]
    )
