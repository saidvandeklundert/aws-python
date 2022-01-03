import boto3
from botocore.config import Config

client_cfg = Config(
    retries={
        "max_attempts": 2,
    }
)


s3 = boto3.client("s3", config=client_cfg)
response = s3.list_buckets()

# print the name of every bucket:
for bucket in response["Buckets"]:
    print(f'  {bucket["Name"]}')
