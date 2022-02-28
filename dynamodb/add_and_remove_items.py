import boto3


data_to_add = [
    {
        "datacenter": "dal09",
        "mgmt-ip": "10.0.0.3",
        "model": "DCS-7048T-A-R",
        "name": "tor05-dal09",
        "vendor": "arista",
        "version": "4.24",
    }
]

items_to_remove = [{"name": "tor05-dal09", "datacenter": "dal09"}]


def add_items():
    """adding items to the DynamoDB table."""
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.Table("devices")
    for device in data_to_add:
        table.put_item(Item=device)


# *, device_names: list[str]
def delete_item(items_to_remove: list[dict]):
    """Remove target device_name from the DynamoDB table.

    Since the example table has a primary key and a sort key,
     both of these will need to be provided as part of 'delete_item'."""
    dynamo_db = boto3.resource("dynamodb")
    table = dynamo_db.Table("devices")
    for item in items_to_remove:
        table.delete_item(Key=item)


def scan_table():
    dynamo_db = boto3.client("dynamodb")
    devices_data = dynamo_db.scan(TableName="devices")
    return devices_data


if __name__ == "__main__":
    from pprint import pprint

    print("before start:")
    pprint(scan_table())
    add_items()
    print("with items added:")
    pprint(scan_table())
    delete_item(items_to_remove=items_to_remove)
    print("with items removed:")
    pprint(scan_table())
