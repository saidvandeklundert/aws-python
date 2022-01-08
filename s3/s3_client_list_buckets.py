import boto3


def list_buckets() -> list:
    """List all buckets using S3 client."""
    s3 = boto3.client(
        "s3",
    )

    buckets = []
    response = s3.list_buckets()
    for bucket in response["Buckets"]:
        buckets.append(bucket["Name"])
    return buckets


def list_buckets_resource() -> list:
    """List all buckets using S3 resource."""
    s3 = boto3.resource(
        "s3",
    )

    buckets = []
    for bucket in s3.buckets.all():
        buckets.append(bucket.name)
    return buckets


if __name__ == "__main__":
    print(list_buckets())
    print(list_buckets_resource())
