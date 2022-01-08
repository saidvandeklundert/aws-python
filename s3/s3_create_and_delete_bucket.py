import os
import uuid
import boto3


def create_bucket(bucket_name: str, region: str) -> dict:
    """Create a bucket in a specific region."""
    s3_resource = boto3.resource("s3")
    resp_bucket_creation = s3_resource.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={"LocationConstraint": region},
    )
    return resp_bucket_creation


def set_versioning(bucket_name: str) -> dict:
    """Enable versioning for a bucket."""
    s3_resource = boto3.resource("s3")
    bucket_versioning = s3_resource.BucketVersioning(bucket_name)
    versioning_response = bucket_versioning.enable()
    return versioning_response


def check_bucket_versioning(bucket_name: str) -> dict:
    """Check if bucket versioning is enabled."""
    s3_client = boto3.client("s3")
    versioning_response = s3_client.get_bucket_versioning(Bucket=bucket_name)
    return versioning_response


def set_serverside_encryption(bucket_name: str) -> dict:
    """Sets server-side encryption to AES256.

    Check AWS::S3::Bucket ServerSideEncryptionByDefault for
     other options and more details.

    """
    s3_client = boto3.client("s3")
    response = s3_client.put_bucket_encryption(
        Bucket=bucket_name,
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
    return response


def upload_example_file(bucket_name: str) -> None:
    s3_client = boto3.client("s3")
    dirname = os.path.dirname(__file__)
    file_to_upload = os.path.join(dirname, "files/example.txt")
    with open(file_to_upload, "rb") as f:
        s3_client.upload_fileobj(f, bucket_name, "example.txt")


def empty_bucket(bucket_name: str) -> None:
    """

    CAREFULL!

    Removes all the files from a bucket.


    """
    user_input = ""

    while user_input not in ["empty", "exit"]:
        user_input = input(
            f"Type 'empty' to remove all objects from bucket {bucket_name} and delete the bucket. \
        \nType exit to stop the script and remove everything through console:\n"
        )
        if user_input == "empty":
            s3_resource = boto3.resource("s3")
            bucket = s3_resource.Bucket(bucket_name)

            objects = []
            for object in bucket.object_versions.all():
                objects.append({"Key": object.object_key, "VersionId": object.id})
            print(f"Deleting the following files:{objects}")
            bucket.delete_objects(Delete={"Objects": objects})
        elif user_input == "exit":
            raise SystemExit(
                "Nothing was deleted. Go to the console and manually delete the bucket created in this example."
            )


def delete_bucket(bucket_name: str) -> dict:
    s3_resource = boto3.resource("s3")
    delete_response = s3_resource.Bucket(bucket_name).delete()
    return delete_response


if __name__ == "__main__":
    # setup:
    uuid_string = str(uuid.uuid4())
    bucket_name = f"example-{uuid_string}"
    # s3_resource = boto3.resource("s3")
    # s3_client = boto3.client("s3")
    region = "eu-central-1"
    print("Create bucket:")
    creation_response = create_bucket(bucket_name, region)
    print(creation_response)
    print("Set versioning:")
    versioning_response = set_versioning(bucket_name)
    print(versioning_response)
    print("Check versioning:")
    check_versioning_response = check_bucket_versioning(bucket_name)
    print(check_versioning_response)
    print("Set server-side encryption:")
    encryption_response = set_serverside_encryption(bucket_name)
    print(encryption_response)
    print("Uploading the file.")
    upload_example_file(bucket_name)
    print("Emptying the bucket:")
    empty_bucket(bucket_name)
    print("Deleting the bucket:")
    delete_response = delete_bucket(bucket_name)
    print(delete_response)