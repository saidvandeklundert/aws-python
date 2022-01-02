import boto3

dynamo_db = boto3.client("dynamodb")
devices_data = dynamo_db.scan(TableName="devices")
print(devices_data)