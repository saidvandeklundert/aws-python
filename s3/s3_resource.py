import boto3

s3 = boto3.resource("s3")
obj = s3.Object(
    bucket_name="saidvandeklundert-s3", key="calling_rust_from_python_draw_io.png"
)
print(obj.last_modified)

# access the client through the resource:
s3_resource = boto3.resource("s3")
s3_client = s3_resource.meta.client
print(s3_client.list_buckets())

# Iterate the bucket names:
for bucket in s3_resource.buckets.all():
    print(f"  {bucket.name}")


# S3 list all keys with the prefix 'reports/'
s3 = boto3.resource("s3")
for bucket in s3.buckets.all():
    for obj in bucket.objects.filter(Prefix="reports/"):
        print(f"{bucket.name}:{obj.key}")

# Limit the amount of buckets to iterate:
for bucket in s3.buckets.limit(10):
    print(bucket.name)