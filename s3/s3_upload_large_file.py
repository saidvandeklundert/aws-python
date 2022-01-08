from pathlib import Path
from typing import Optional
import boto3
from boto3.s3.transfer import TransferConfig, S3Transfer


KB = 1024
MB = KB * KB


def generate_file(size_in_mb: int) -> str:
    """
    Generate a file of a given size in MB, returns the filename
    """
    filename = f"{size_in_mb}MB.bin"
    with open(filename, "wb") as f:
        f.seek(size_in_mb * 1024 * 1024 - 1)
        f.write(b"\0")
    return filename


def large_upload(file_name: str, bucket_name: str, s3_file_name: Optional[str]) -> None:
    """
    Upload a file to S3
    """
    s3_file_name = s3_file_name or file_name
    session = boto3.Session()
    # tc = TransferConfig()  # uncomment to use  default settings
    tc_config = TransferConfig(
        multipart_threshold=1024 * 25,
        max_concurrency=10,
        multipart_chunksize=25 * MB,
        use_threads=True,
    )
    s3_client = session.client("s3")
    transfer_object = S3Transfer(client=s3_client, config=tc_config)
    transfer_object.upload_file(file_name, bucket_name, s3_file_name)


def delete_file_from_s3(s3_file_name: str, bucket_name: str) -> None:
    """
    Delete a file from S3
    """
    s3_resource = boto3.resource("s3")
    s3_resource.Object(bucket_name, s3_file_name).delete()


def list_file_size(s3_file_name: str, bucket_name: str) -> None:
    """
    List a file from S3
    """
    s3 = boto3.client("s3")
    response = s3.head_object(Bucket=bucket_name, Key=s3_file_name)
    size = response["ContentLength"]
    print(f"Size of {s3_file_name} is {size} bytes, or {size / MB} MB")


def delete_local_file(file_name: str) -> None:
    """
    Delete a local file
    """
    path_instance = Path(file_name)
    path_instance.unlink()


if __name__ == "__main__":
    # specify bucketname:
    bucket_name = "saidvandeklundert-testing"
    # generate the file and set the filename:
    upload_file_size = 1
    file_to_upload = generate_file(upload_file_size)

    # upload the file:
    print("Uploading the file.")
    large_upload(file_to_upload, bucket_name, "large_upload.bin")

    # check if file is present in the bucket and return the size:
    list_file_size("large_upload.bin", bucket_name)
    # remove the file from the bucket:
    import time

    time.sleep(3)
    # delete file from S3 and delete the locally generated file:
    delete_file_from_s3("large_upload.bin", bucket_name)
    delete_local_file(file_to_upload)
    print("Fin.")
