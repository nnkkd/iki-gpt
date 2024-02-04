import os
import sys
from typing import List
from mangum import Mangum
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import logging

from app.routers import routers

logging.basicConfig(level=logging.INFO)


load_dotenv(".env")


server = os.environ.get("SERVER", "")
app: FastAPI = FastAPI(servers=[{"url": server}])
app.openapi_version = "3.0.0"
origins: List[str] = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.router, prefix="/api/v1")

handler = Mangum(app)
