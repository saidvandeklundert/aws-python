import boto3
from pprint import pprint


def create_table() -> None:
    """Creates a DynamoDB table"""
    dynamodb = boto3.resource("dynamodb")

    table = dynamodb.create_table(
        TableName="Humans",
        KeySchema=[
            {"AttributeName": "id", "KeyType": "HASH"},  # Partition key
            {"AttributeName": "name", "KeyType": "RANGE"},  # Sort key
        ],
        AttributeDefinitions=[
            {"AttributeName": "id", "AttributeType": "N"},
            {"AttributeName": "name", "AttributeType": "S"},
        ],
        ProvisionedThroughput={
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1,
        },  # this is free!
    )

    print(
        f"Table Humans is in status {table.table_status}, waiting for \
            the table to be fully provisioned."
    )
    table.meta.client.get_waiter("table_exists").wait(TableName="Humans")
    state = dynamodb.Table("Humans").table_status
    print(f"Table created, status is now:{state}")


def delete_table():
    """Deletes a DynamoDB table"""
    dynamodb = boto3.resource("dynamodb")

    table = dynamodb.Table("Humans")
    ret = table.delete()
    pprint(ret)


if __name__ == "__main__":
    create_table()
    print("Enter 'delete' to remove the table 'Human':")
    x = input()
    if x == "delete":
        delete_table()
    else:
        print("chose not to delete")
