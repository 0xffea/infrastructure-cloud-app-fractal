import os
import uuid

from typing import Optional

from azure.storage.queue import QueueClient
from azure.storage.queue import BinaryBase64EncodePolicy
from azure.storage.queue import BinaryBase64DecodePolicy

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
