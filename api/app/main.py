import uuid
import sys
import json

from dataclasses import dataclass
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

@dataclass
class Frame:
    x: int = None
    y: int = None
    x1: int = None
    y1: int = None

@dataclass
class Resolution:
    x: int = None
    y: int = None

@dataclass
class Fractal:
    iterations: Optional[int]= None
    resolution: Optional[Resolution] = None
    frame: Optional[Frame] = None


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

@app.post("/api/v1/fractal/")
async def generate_fractal(fractal: Fractal):
    request_id = str(uuid.uuid4())
    msg = {"request_id": request_id}
    if iterations := fractal.iterations:
        msg.update({"iterations": iterations})
    if resolution := fractal.resolution:
        msg.update({"resolution": {"x": resolution.x, "y": resolution.y}})
    if frame := fractal.frame:
        msg.update({
            "frame": {
                "x": frame.x,
                "y": frame.y,
                "x1": frame.x1,
                "y1": frame.y1
            }
        })
    msg = json.dumps(msg)
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
        raise HTTPException(status_code=404, detail="Image not found")

    return StreamingResponse(stream.chunks(), media_type="image/png")

