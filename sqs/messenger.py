"""
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.send_message
"""
from pprint import pprint
import boto3

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class QueueAttributes:
    ApproximateNumberOfMessages: int
    ApproximateNumberOfMessagesDelayed: int
    ApproximateNumberOfMessagesNotVisible: int
    CreatedTimestamp: int
    DelaySeconds: int
    LastModifiedTimestamp: int
    MaximumMessageSize: int
    MessageRetentionPeriod: int
    QueueArn: str
    ReceiveMessageWaitTimeSeconds: int
    SqsManagedSseEnabled: bool
    VisibilityTimeout: int


@dataclass
class Message:
    MessageId: str
    ReceiptHandle: str
    MD5OfBody: str
    Body: str  # the actual message


@dataclass
class ResponseMetadata:
    RequestId: str
    HTTPStatusCode: str
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int


@dataclass
class ReadMessageResponse:
    ResponseMetadata: ResponseMetadata
    Messages: List[Message] = field(default_factory=list)

    def __iter__(self):
        return iter(self.Messages)


@dataclass
class ResponseMetadata:
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]


@dataclass
class SendMessageResponse:
    MD5OfMessageBody: str
    MessageId: str
    ResponseMetadata: ResponseMetadata


@dataclass
class DeleteResponse:
    ResponseMetadata: ResponseMetadata
    RequestId: str
    HTTPStatusCode: int
    RetryAttempts: int
    HTTPHeaders: Dict[str, str] = field(default_factory=dict)


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


@dataclass
class Messenger:
    # TODO: add read_all() method
    queueu_url: str
    region: str

    def send_message(self, message: str) -> SendMessageResponse:
        """Send a message to the queue."""
        sqs_client = boto3.client("sqs", region_name=self.region)

        response = sqs_client.send_message(
            QueueUrl=self.queueu_url, MessageBody=message
        )
        return SendMessageResponse(**response)

    def read_messages(self, nr_of_messages: int = 1) -> ReadMessageResponse:
        """Read a number of messages from the queue."""
        sqs_client = boto3.client("sqs", region_name=self.region)
        response = sqs_client.receive_message(
            QueueUrl=self.queueu_url,
            MaxNumberOfMessages=nr_of_messages,  # max 10, default 1
            WaitTimeSeconds=0,
        )
        return ReadMessageResponse(**response)

    def delete_message(self, receipt_handle: str):
        """Delete target message from the queueu"""
        sqs_client = boto3.client("sqs", region_name=self.region)
        response = sqs_client.delete_message(
            QueueUrl=self.queueu_url,
            ReceiptHandle=receipt_handle,
        )
        return response

    def get_queue_count(self) -> int:
        """Returns the 'ApproximateNumberOfMessages' from the queueu."""
        sqs_client = boto3.client("sqs", region_name=self.region)
        response = sqs_client.get_queue_attributes(
            QueueUrl=self.queueu_url,
            AttributeNames=["ApproximateNumberOfMessages"],
        )

        return response["Attributes"]["ApproximateNumberOfMessages"]

    def get_queue_attributes(self) -> QueueAttributes:
        """Returns the queueu attributes."""
        sqs_client = boto3.client("sqs", region_name=self.region)
        response = sqs_client.get_queue_attributes(
            QueueUrl=self.queueu_url,
            AttributeNames=["All"],
        )
        ret = QueueAttributes(**response["Attributes"])
        return ret


if __name__ == "__main__":
    msgnr = Messenger(
        queueu_url="https://eu-central-1.queue.amazonaws.com/717687450252/example-queue",
        region="eu-central-1",
    )
    print(msgnr.get_queue_count())
    print(msgnr.get_queue_attributes())

    msg = msgnr.send_message("message 1")
    msg = msgnr.send_message("message 2")
    msg = msgnr.send_message("message 3")
    msg = msgnr.send_message("message 4")
    msg = msgnr.send_message("message 5")

    msg_read = msgnr.read_messages(nr_of_messages=10)

    for m in msg_read:
        m = Message(**m)
        print(f"read message {m.Body}")
        msgnr.delete_message(receipt_handle=m.ReceiptHandle)

    print(msgnr.get_queue_count())
    pprint(vars(msgnr.get_queue_attributes()))
