import sys
import json
import logging

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueClient
from azure.core.exceptions import ServiceRequestError
from azure.core.exceptions import ResourceNotFoundError

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

from compute import Fractal

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

DEFAULT_ITERATIONS = 100

keyVaultName = "xffee-key-vault"
KVUri = f"https://{keyVaultName}.vault.azure.net"
secretName = "0xffeasaprod-connection-string"

credential = DefaultAzureCredential()

client = SecretClient(vault_url=KVUri, credential=credential)

storage_connection_string = None

try:
    storage_connection_string = client.get_secret(secretName)
except ServiceRequestError:
    # log existing
    sys.exit(1)
else:
    storage_connection_string = storage_connection_string.value


try:
    queue_client = QueueClient.from_connection_string(
        storage_connection_string,
        "0xffea-storage-queue-prod-westeurope"
    )
except ResourceNotFoundError:
    sys.exit(1)
except ValueError:
    sys.exit(1)

try:
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
    container_client = blob_service_client.get_container_client("0xffea-storage-container-prod-westeurope")
except ResourceNotFoundError:
    sys.exit(1)

messages = queue_client.receive_messages()

for message in messages:
    payload = message.content
    print(f"Dequeueing message: {payload}")
    payload = json.loads(payload)
    request_id = payload["request_id"]
    iterations = payload.get("iterations", DEFAULT_ITERATIONS)
    print(request_id)
    queue_client.delete_message(message.id, message.pop_receipt)
    fractal = Fractal(iterations=iterations)
    logger.debug("Generating image...")
    data = fractal.generate()
    logger.debug("Uploading image to blob storage")
    blob_client = container_client.get_blob_client(request_id)
    blob_client.upload_blob(data, blob_type="BlockBlob")
