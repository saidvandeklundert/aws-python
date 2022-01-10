"""
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.send_message
"""
from pprint import pprint
import boto3
import time


def send_message(queueu_url: str, region_name: str, message: str):
    sqs_client = boto3.client("sqs", region_name=region_name)

    response = sqs_client.send_message(QueueUrl=queueu_url, MessageBody=message)
    return response


def receive_message(queueu_url: str, region_name: str, nr_of_messages: int = 1):
    sqs_client = boto3.client("sqs", region_name=region_name)
    response = sqs_client.receive_message(
        QueueUrl=queueu_url,
        MaxNumberOfMessages=nr_of_messages,  # max 10, default 1
        WaitTimeSeconds=0,
    )
    return response


def delete_message(queueu_url: str, region_name: str, receipt_handle: str):
    sqs_client = boto3.client("sqs", region_name=region_name)
    response = sqs_client.delete_message(
        QueueUrl=queueu_url,
        ReceiptHandle=receipt_handle,
    )

    return response


if __name__ == "__main__":
    queueu_url = "https://eu-central-1.queue.amazonaws.com/717687450252/example-queue"
    region_name = "eu-central-1"
    print("sending message:")
    send_response = send_message(
        queueu_url=queueu_url,
        region_name=region_name,
        message='{"important-key":"important-value-1"}',
    )
    pprint(send_response)
    time.sleep(2)
    receive_response = receive_message(
        queueu_url=queueu_url, region_name=region_name, nr_of_messages=10
    )

    send_message_id = send_response["MessageId"]
    send_message_md5 = send_response["MD5OfMessageBody"]
    print(
        f"Message that was send to the queue has id {send_message_id} and md5 {send_message_md5}."
    )

    to_delete = []
    print("Messages in the queue:")
    for msg in receive_response["Messages"]:
        pprint(msg)
        to_delete.append(msg["ReceiptHandle"])
    print(f"Deleting messages with the following receipt handles:")
    for item in to_delete:
        print(item)
    for receipt_handle in to_delete:

        delete_response = delete_message(
            queueu_url=queueu_url,
            region_name=region_name,
            receipt_handle=receipt_handle,
        )
        pprint(delete_response)
