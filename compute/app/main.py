import sys

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ServiceRequestError

keyVaultName = "xffed-key-vault"
KVUri = f"https://{keyVaultName}.vault.azure.net"
secretName = "0xffeasaprod-connection-string"

credential = DefaultAzureCredential()

client = SecretClient(vault_url=KVUri, credential=credential)

try:
    retrieved_secret = client.get_secret(secretName)
except ServiceRequestError:
    # log existing
    sys.exit(1)


print(f"The value of secret '{secretName}' in '{keyVaultName}' is: '{retrieved_secret.value}'")
