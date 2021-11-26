# coding: utf-8

# --------------------------------------------------------------------------
# 2021
# --------------------------------------------------------------------------
"""
Classes and functions used in Fractal app.
"""

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueClient
from azure.core.exceptions import ServiceRequestError
from azure.core.exceptions import ResourceNotFoundError
from azure.core.exceptions import HttpResponseError
from azure.data.tables import TableClient

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

DEFAULT_ITERATIONS = 100
DEFAULT_RESOLUTION = (7168, 7168)

keyVaultName = "xffee-key-vault"
KVUri = f"https://{keyVaultName}.vault.azure.net"
secretName = "storage-account-connection-string"

credential = DefaultAzureCredential()

client = SecretClient(vault_url=KVUri, credential=credential)

storage_connection_string = None
storage_queue_name = None
storage_container_name = None

try:
    storage_connection_string = client.get_secret(secretName)
except ServiceRequestError:
    sys.exit(1)
else:
    storage_connection_string = storage_connection_string.value


try:
    table_client = TableClient.from_connection_string(
        storage_connection_string,
        "configuration")
except (ResourceNotFoundError, ValueError):
    sys.exit(1)

query_filter = "PartitionKey eq @pk_filter or RowKey eq @rk_filter"
parameters = {
    "pk_filter": "global",
    "rk_filter": "prod",
}


try:
    queried_entities = table_client.query_entities(
        query_filter, parameters=parameters)
except HttpResponseError:
    sys.exit(1)

for entity in queried_entities:
    storage_queue_name = entity["StorageQueueName"]
    storage_container_name = entity["StorageContainerName"]

try:
    queue_client = QueueClient.from_connection_string(
        storage_connection_string,
        storage_queue_name
    )
except (ResourceNotFoundError, ValueError):
    sys.exit(1)

try:
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
    container_client = blob_service_client.get_container_client(
        storage_container_name)
except ResourceNotFoundError:
    sys.exit(1)