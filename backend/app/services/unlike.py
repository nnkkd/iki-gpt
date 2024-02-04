import logging

from app.crud.goroku import GorokuCollection
from app.schemas.search import Correspondence, PostSearchResponse
from app.inference.embed import embed_queries
from app.schemas.unlike import PostUnlikeResponse


logger = logging.getLogger(__name__)


async def unlike(query: str, collection: GorokuCollection):
    res = collection.collection.get(
        ids=[query],
    )

    metadata = res["metadatas"] or []
    if len(metadata) == 0:
        return PostUnlikeResponse(status="failed")
    unlike = int(metadata[0]["unlike_count"])

    collection.collection.update(ids=[query], metadatas=[{"unlike_count": unlike + 1}])
    return PostUnlikeResponse(status="ok")
