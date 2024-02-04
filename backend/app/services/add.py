import logging
from typing import Dict, List
import numpy as np

from app.crud.goroku import GorokuCollection
from app.inference.embed import embed_queries, embed_query
from app.schemas.add import PostAddRequest, PostAddResponse


logger = logging.getLogger(__name__)


async def add(
    req_body: PostAddRequest, collection: GorokuCollection
) -> PostAddResponse:
    # すでに近い文章があるかどうかを確認
    print("add request", req_body)
    embed_meme = embed_query(req_body.correspond_to)
    res = collection.collection.query(
        query_embeddings=[embed_meme], include=["documents", "distances"]
    )
    distances = res["distances"]
    if distances:
        if len(distances[0]) > 0 and distances[0][0] < 0.01:
            documents = res["documents"] or []
            memes = [doc for doc in documents[0]][0]
            logger.info(f"すでに近い文章が存在します。:{memes}")
            return PostAddResponse(message=f"すでに近い文章が存在します。:{memes}", status="failed")

    # 追加
    embed_document = embed_query(req_body.word)
    new_id = collection.collection.count() + 1
    new_id_word = new_id + 1
    collection.collection.add(
        ids=[str(new_id), str(new_id_word)],
        embeddings=[embed_meme, embed_document],
        documents=[req_body.correspond_to, req_body.word],
        metadatas=[
            {
                "meme": req_body.correspond_to,
                "natural": req_body.word,
                "description": req_body.description,
                "use_case": req_body.use_case,
                "hit_count": 0,
                "unlike_count": 0,
            }
        ]
        * 2,
    )
    print(
        f"add: {new_id}, {req_body.correspond_to}, {req_body.correspond_to}, {req_body.word}, {req_body.description}, {req_body.use_case}"
    )
    print(
        f"add: {new_id_word}, {req_body.word}, {req_body.correspond_to}, {req_body.word}, {req_body.description}, {req_body.use_case}"
    )

    return PostAddResponse(
        message=f"追加しました。: {req_body.correspond_to}", status="success"
    )
