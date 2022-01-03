import os
import uuid
import boto3

uuid_string = str(uuid.uuid4())
BUCKET_NAME = f"example-{uuid_string}"
s3_resource = boto3.resource("s3")
s3_client = boto3.client("s3")

# Create a bucket:
resp_bucket_creation = s3_resource.create_bucket(
    Bucket=BUCKET_NAME,
    CreateBucketConfiguration={"LocationConstraint": "eu-central-1"},
)

# Turn on versioning for the bucket:
bucket_versioning = s3_resource.BucketVersioning(BUCKET_NAME)
versioning_response = bucket_versioning.enable()
versioning_response = s3_client.get_bucket_versioning(Bucket=BUCKET_NAME)

# Turn on encryption, cannot be done using resource, so we turn to the client:
response = s3_client.put_bucket_encryption(
    Bucket=BUCKET_NAME,
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
encryption_response = s3_client.get_bucket_encryption(Bucket=BUCKET_NAME)

#
s3_client = boto3.client("s3")

# upload a file:
print("Uploading the file.")
dirname = os.path.dirname(__file__)
file_to_upload = os.path.join(dirname, "files/example.txt")
with open(file_to_upload, "rb") as f:
    s3_client.upload_fileobj(f, BUCKET_NAME, "example.txt")

# before we can delete the bucket, we need to delete all the objects:
bucket = s3_resource.Bucket(BUCKET_NAME)

objects = []
for object in bucket.object_versions.all():
    objects.append({"Key": object.object_key, "VersionId": object.id})
print(objects)
bucket.delete_objects(Delete={"Objects": objects})
"""
Objects takes the following format:
'Objects': [
    {
        'Key': 'string',
        'VersionId': 'string'
    },
],
"""
# now that the bucket is empyty, we can delete the bucket:
delete_response = s3_resource.Bucket(BUCKET_NAME).delete()

print("Fin.")