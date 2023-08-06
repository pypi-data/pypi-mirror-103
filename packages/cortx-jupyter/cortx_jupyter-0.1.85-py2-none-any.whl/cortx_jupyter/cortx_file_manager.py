import json 
from .utils import (
    _get_base64_file,
    _save_base64_file
    )
from collections import namedtuple

Config = namedtuple('Config', [
    'logger', 'prefix', 'region', 's3_bucket', 's3_host', 's3_auth',
    'multipart_uploads', 'endpoint_url'
])

config_file_path = "credentials.json" 

def _config():
    config = {}
    with open(config_file_path) as fp:
       config = json.load(fp)

    return Config(
            region=config.region_name,
            bucket_name=config.bucket_name,
            host_name=config.host_name,
            cortx_authenticator=config.authentication.get_credentials,
            prefix=config.prefix,
            multipart_uploads=config.multipart_uploads,
            endpoint_url=config.endpoint_url
        )

def load_data(file_name):
    if _check_file_exists(file_name):
        return _get_base64_file(_config(), file_name, True)

# Valid Formats: csv, json
def save_data(file_name, data, format):
    _save_base64_file(_config(), None, data, file_name)



    