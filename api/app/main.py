import uuid
import sys
import json

from typing import Optional

from azure.storage.queue import QueueClient
from azure.core.exceptions import ResourceNotFoundError

from fastapi import FastAPI

from config import settings


queue_client = None

app = FastAPI()


@app.on_event("startup")
async def startup():
    global queue_client
    try:
        queue_client = QueueClient.from_connection_string(
            conn_str=settings.azure_storage_connection_string,
            queue_name=settings.azure_storage_queue_name,
        )
    except ResourceNotFoundError:
        sys.exit(1)
    except ValueError:
        sys.exit(1)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


# query vms with grpc
@app.get("/health")
async def get_health():
    return {}


@app.get("/random")
async def get_random_fractal():
    request_id = str(uuid.uuid4())
    msg = json.dumps({"request_id": request_id})
    queue_client.send_message(msg)
    return {"request-id": request_id}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
