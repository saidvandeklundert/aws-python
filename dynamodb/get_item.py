import boto3
from boto3.dynamodb.conditions import Key
from pprint import pprint


def get_item():
    """Get item from the DynamoDB table."""
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.Table("devices")
    response = table.query(KeyConditionExpression=Key("name").eq("core02-wdc01"))
    for item in response["Items"]:
        pprint(item)


if __name__ == "__main__":
    get_item()
