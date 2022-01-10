import boto3


def get_parameter(parameter: str) -> str:
    """parameter is the 'path' to the parameter."""
    ssm_client = boto3.client("ssm")

    parameter = ssm_client.get_parameter(Name=parameter, WithDecryption=True)

    return parameter["Parameter"]["Value"]


if __name__ == "__main__":
    parameter = get_parameter("/passwords/infrastructure/ssot_token")

    print(f"## SSM Parameter Store value: {parameter}")
