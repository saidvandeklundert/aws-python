import boto3


data_to_add = [
    {"id": 1, "name": "Said van de Klundert", "age": 38},
    {
        "id": 2,
        "name": "Jan van de Klundert",
    },
    {
        "id": 3,
        "name": "Marie van de Klundert",
    },
    {
        "id": 4,
        "name": "Anne van de Klundert",
    },
]


def add_items():
    """adding items to the DynamoDB table."""
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.Table("Humans")
    for device in data_to_add:
        table.put_item(Item=device)


def scan_table():
    dynamo_db = boto3.client("dynamodb")
    devices_data = dynamo_db.scan(TableName="Humans")
    return devices_data


if __name__ == "__main__":
    from pprint import pprint

    print("before start:")
    pprint(scan_table())
    add_items()
    print("with items added:")
    pprint(scan_table())
