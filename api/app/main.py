import uuid
import sys
import json

from typing import Optional

from azure.storage.queue import QueueClient
from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import StreamingResponse

from config import settings


queue_client = None
blob_service_client = None

app = FastAPI()


@app.on_event("startup")
async def startup():
    global queue_client
    global blob_service_client

    try:
        queue_client = QueueClient.from_connection_string(
            conn_str=settings.azure_storage_connection_string,
            queue_name=settings.azure_storage_queue_name,
        )

        blob_service_client = BlobServiceClient.from_connection_string(
            settings.azure_storage_connection_string
        )
    except (ResourceNotFoundError, ValueError):
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

@app.get("/api/v1/fractal/{request_id}")
async def get_fractal_image(request_id):
    blob_client = blob_service_client.get_blob_client(
        container="0xffea-storage-container-prod-westeurope",
        blob=request_id
    )
    try:
        stream = blob_client.download_blob()
    except ResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Item not found")

    return StreamingResponse(stream.chunks(), media_type="image/png")


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
