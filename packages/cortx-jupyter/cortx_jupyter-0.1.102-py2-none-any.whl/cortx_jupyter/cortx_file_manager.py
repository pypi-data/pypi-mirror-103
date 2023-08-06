import json 
import boto3

config_file_path = "credentials.json" 

def _config():
    cfg = {}
    with open(config_file_path) as fp:
       cfg = json.load(fp)
    return cfg

def load_data(file_name):
    config = _config()
    return _get_object(config, config['bucket_name'], file_name)['Body'].read()

# Valid Formats: csv, json
def save_data(file_name, data, format):
    config = _config()
    _put_object(config, config['bucket_name'], data, file_name)


def _put_object(config, bucket, body, object_name):
    s3_client = boto3.client('s3', aws_access_key_id=config['cortx_authenticator']['access_key_id'], aws_secret_access_key=config['cortx_authenticator']['secret_access_key'], region_name='us-east-1', endpoint_url= config['endpoint_url']) 
    return s3_client.put_object(Body=body, Bucket=bucket, Key=object_name)

def _get_object(config, bucket, object_name):
    s3_client = boto3.client('s3', aws_access_key_id=config['cortx_authenticator']['access_key_id'], aws_secret_access_key=config['cortx_authenticator']['secret_access_key'], region_name='us-east-1', endpoint_url= config['endpoint_url'])
    return s3_client.get_object(Bucket=bucket, Key=object_name)