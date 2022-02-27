import boto3


def scan_table():
    dynamo_db = boto3.client("dynamodb")
    devices_data = dynamo_db.scan(TableName="devices")
    return devices_data


if __name__ == "__main__":
    print(scan_table())
