import uuid
import boto3

uuid_string = str(uuid.uuid4())
s3_resource = boto3.resource("s3")
s3_client = boto3.client("s3")
# Create a bucket:
resp_bucket_creation = s3_resource.create_bucket(
    Bucket=f"example-{uuid_string}",
    CreateBucketConfiguration={"LocationConstraint": "eu-central-1"},
)

# Turn on versioning for the bucket:
bucket_versioning = s3_resource.BucketVersioning(f"example-{uuid_string}")
versioning_response = bucket_versioning.enable()
versioning_response = s3_client.get_bucket_versioning(Bucket=f"example-{uuid_string}")

# Turn on encryption, cannot be done using resource, so we turn to the client:
response = s3_client.put_bucket_encryption(
    Bucket=f"example-{uuid_string}",
    ServerSideEncryptionConfiguration={
        "Rules": [
            {
                "ApplyServerSideEncryptionByDefault": {
                    "SSEAlgorithm": "AES256",
                }
            },
        ]
    },
)
encryption_response = s3_client.get_bucket_encryption(Bucket=f"example-{uuid_string}")

# delete the bucket:
# import time
# time.sleep(120)
delete_response = s3_resource.Bucket(f"example-{uuid_string}").delete()