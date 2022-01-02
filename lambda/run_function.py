from pprint import pprint
import boto3
import base64

client = boto3.client("lambda")
response = client.invoke(
    FunctionName="klundert-lambda-sam-helloworldpython3-E5pK6x3FSUfk",  # yes, this is how I name my functions
    InvocationType="RequestResponse",
    LogType="Tail",
)

pprint(response)
log_result_encoded = response["LogResult"]
log_result_decoded = base64.b64decode(log_result_encoded)
pprint(log_result_decoded)
