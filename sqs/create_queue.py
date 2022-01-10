from pprint import pprint
import boto3


def create_queue(queue_name: str):
    client = boto3.client("sqs", region_name="eu-central-1")
    response = client.create_queue(
        QueueName=queue_name,
        Attributes={
            "DelaySeconds": "5",  # default 0, max 900 (15 min)
            "VisibilityTimeout": "29",  # default 30, min 0
        },
    )
    return response


def get_queue_url(queue_name: str):
    sqs_client = boto3.client("sqs", region_name="eu-central-1")
    response = sqs_client.get_queue_url(
        QueueName=queue_name,
    )
    return response["QueueUrl"]


def delete_queue(queue_name: str):
    sqs_client = boto3.client("sqs", region_name="eu-central-1")
    response = sqs_client.delete_queue(QueueUrl=queue_name)
    return response


if __name__ == "__main__":
    queue_name = "example-queue"
    create_queue_resp = create_queue(queue_name)
    pprint(create_queue_resp)
    queue_url_resp = get_queue_url(queue_name)
    pprint(queue_url_resp)
    val = input("Type 'delete' in case you want to delete the 'example-queue':")
    if val == "delete":
        delete_queu_response = delete_queue(queue_name)
        pprint(delete_queu_response)
    else:
        print("'example-queue' is not deleted.")