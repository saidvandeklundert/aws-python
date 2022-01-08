"""
Script will display information about target object in S3
"""
import boto3


KB = 1024
MB = KB * KB


def list_s3_object_metadata(s3_file_name: str, bucket_name: str) -> dict:
    """
    List data from an object in S3
    """
    s3 = boto3.client("s3")
    response = s3.head_object(Bucket=bucket_name, Key=s3_file_name)

    return response


if __name__ == "__main__":
    bucket_name = "saidvandeklundert-testing"
    file_name = "example_encrypted.txt"
    s3_object_info = list_s3_object_metadata(file_name, bucket_name)

    size = s3_object_info["ContentLength"]
    last_modified = s3_object_info["LastModified"]
    encryption = s3_object_info["ServerSideEncryption"]

    print(
        f"""
        Some facts on the file/object named '{file_name}':
    - the size is {size} bytes, or {size / MB:.4f} MB
    - last modified at {last_modified}",
    - server-side encryption: {encryption}""".strip()
    )
    print("\n\nReturned metadata dictionary:\n", s3_object_info)
    print("Fin.")
