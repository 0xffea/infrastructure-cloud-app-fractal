import sys
import json

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueClient
from azure.core.exceptions import ServiceRequestError
from azure.core.exceptions import ResourceNotFoundError

keyVaultName = "xffed-key-vault"
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

messages = queue_client.receive_messages()

for message in messages:
    payload = message.content
    print(f"Dequeueing message: {payload}")
    payload = json.loads(payload)
    print(payload["request_id"])
    queue_client.delete_message(message.id, message.pop_receipt)
