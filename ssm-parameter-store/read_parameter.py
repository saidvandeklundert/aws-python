import boto3


ssm = boto3.client("ssm")

PARAMETER = ssm.get_parameter(
    Name="/passwords/infrastructure/ssot_token", WithDecryption=True
)
PASSWORD = PARAMETER["Parameter"]["Value"]

print(f"## SSM Parameter Store value: {PASSWORD}")
