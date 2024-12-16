import os
import importlib


def return_secret(secret_to_extract):
    try:
        # Dynamically import the secret from the secrets_config module
        secrets_config = importlib.import_module('configs.secrets_config')
        local_secret = getattr(secrets_config, secret_to_extract, None)
    except ModuleNotFoundError:
        # If the module is not found, fallback to None for the secret
        local_secret = None

    # Use environment variables if available, otherwise fallback to local secrets
    return os.getenv(secret_to_extract, local_secret)


def csv_secret_to_array(csv_secret):
    return csv_secret.split(',')
