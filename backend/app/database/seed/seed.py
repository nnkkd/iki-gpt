import csv
from typing import List
from dotenv import load_dotenv
import numpy as np
from openai import embeddings
from app.crud.goroku import GorokuCollection
from app.inference.embed import embed_queries

load_dotenv(".env")

seed_csv = "dataset/goroku.csv"


with open(seed_csv, "r", encoding="utf-8") as f:
    dict_reader = csv.DictReader(f)
    push_list = []

    for row in dict_reader:
        if row["embed_document"] and row["natural"] and row["meme"]:
            push_list.append(row)

    print(push_list)
    collection = GorokuCollection()
    data = embed_queries([row["embed_document"] for row in push_list])
    collection.collection.add(
        ids=[row["id"] for row in push_list],
        embeddings=data,
        documents=[row["embed_document"] for row in push_list],
        metadatas=[
            {
                "meme": row["meme"],
                "natural": row["natural"],
                "description": row["description"],
                "use_case": row["use_case"],
                "hit_count": 0 if row["hit_count"] == "" else int(row["hit_count"]),
                "unlike_count": 0
                if row["unlike_count"] == ""
                else int(row["unlike_count"]),
            }
            for row in push_list
        ],
    )
