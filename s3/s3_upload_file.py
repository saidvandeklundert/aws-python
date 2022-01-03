import os
import boto3

dirname = os.path.dirname(__file__)
file_to_upload = os.path.join(dirname, "files/example.txt")

BUCKET_NAME = "saidvandeklundert-testing"


s3_client = boto3.client("s3")

# upload the file:
print("Uploading the file.")
with open(file_to_upload, "rb") as f:
    # print(f.read())
    s3_client.upload_fileobj(f, BUCKET_NAME, "example.txt")

"""
The 'upload_fileobj' method is a managed transfer.
  This will perform a multipart upload in multiple threads if necessary.
"""

# download the file:
print("Downloading the file.")
with open(os.path.join(dirname, "downloaded_example.txt"), "wb") as data:
    s3_client.download_fileobj(BUCKET_NAME, "example.txt", data)

# delete the file:

val = input("Enter 'delete' in case you want to delete the file:")
if val == "delete":
    response = s3_client.delete_object(
        Bucket=BUCKET_NAME,
        Key="example.txt",
    )
    print(response)
    print("File was deleted from S3.")
else:
    print("File was not deleted from S3.")

with open(file_to_upload, "rb") as f:
    s3_client.upload_fileobj(
        f,
        BUCKET_NAME,
        "example_encrypted.txt",
        ExtraArgs={"ServerSideEncryption": "aws:kms"},
    )
    # AES256 ( SSE-S3: AES-256 encryption using keys handled and managed by AWS )
    # aws:kms ( uses KMS)
