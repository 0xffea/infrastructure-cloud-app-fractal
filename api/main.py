import environ
import uuid

from typing import Optional

from azure.storage.queue import QueueClient

from fastapi import FastAPI

env = environ.Env(
    DEBUG=(bool, False)
)

# Read .env file for local dev
environ.Env.read_env()

DEBUG = env("DEBUG")
AZURE_STORAGE_CONNECTION_STRING = env("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_QUEUE_NAME = env("AZURE_STORAGE_QUEUE_NAME")

queue_client = QueueClient.from_connection_string(
                        conn_str=AZURE_STORAGE_CONNECTION_STRING,
                        queue_name=AZURE_STORAGE_QUEUE_NAME
                    )
app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/health")
async def get_health():
    return {}

@app.get("/random")
async def get_random_fractal():
    request_uuid = str(uuid.uuid4())
    print("Adding message: " + request_uuid)
    msg = { "uuid": request_uuid }
    queue_client.send_message(msg)
    return {"request-uuid": request_uuid}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
