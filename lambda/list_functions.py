from pprint import pprint
import boto3


client = boto3.client("lambda")
response = client.list_functions()
pprint(response)

for d in response["Functions"]:
    print(d["FunctionName"])
