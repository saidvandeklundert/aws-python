"""
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.send_message
"""
from pprint import pprint
import boto3
import time
from dataclasses import dataclass, field
from typing import Dict, List

message_response_example = {
    "MD5OfMessageBody": "4fded1464736e77865df232cbcb4cd19",
    "MessageId": "e09a4c9a-5bfb-45f0-9de2-2b321484fe20",
    "ResponseMetadata": {
        "RequestId": "22bf06cf-50ce-5d0c-be0a-5c56868b3250",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "22bf06cf-50ce-5d0c-be0a-5c56868b3250",
            "date": "Wed, 02 Mar 2022 20:31:01 GMT",
            "content-type": "text/xml",
            "content-length": "378",
        },
        "RetryAttempts": 0,
    },
}

receive_message_response = {
    "Messages": [
        {
            "MessageId": "65742eaa-3e2d-43a4-a4ec-fe3240e90832",
            "ReceiptHandle": "AQEBwpC0GfEJ6Xs03EZ7hmDCur/hylmB4bzhPkZop9gsjKq1P+3fmdUKykaCOR/wNIsq3153Ppo6lBSze/bkyP8A/CXuBr06oDcaDp8qMWuw4HXtNvQEsNiMO3kXO+HmioOIkFSYHgZ5p1mltIA/3Cy5JCKapPNsPp2VGiECcTdISFndfVCZJbK2pcLr78DA2Qtj6BrPXYNPdWKqtEfk6KlgvwzIjyWCOebb9GsaUr5H4MUfzoV/ZkQr/A9fwJ1Or4XisdIyg4yVr6M4cXss9/+U2gN1CtV+HTJzhLmck/ijw4qYGPP8eek3VXGK1p5dEWG6s+r1YIMEHy+fJV/a1J8mcyOn6O/v407ktP/3fLMZXGxqtWXscyuTx+YMH5y9OjrGPGadhRjCMu5ezJqqanbJ3g==",
            "MD5OfBody": "618dc903bc57957881c714205b378173",
            "Body": "Something very important",
        }
    ],
    "ResponseMetadata": {
        "RequestId": "0aca6c69-5b89-5de3-a2d3-36f0833e8716",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "0aca6c69-5b89-5de3-a2d3-36f0833e8716",
            "date": "Wed, 02 Mar 2022 20:41:27 GMT",
            "content-type": "text/xml",
            "content-length": "875",
        },
        "RetryAttempts": 0,
    },
}


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


x = {
    "ResponseMetadata": {
        "RequestId": "084d6181-a4b4-5390-b45d-3b1878958aa6",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "084d6181-a4b4-5390-b45d-3b1878958aa6",
            "date": "Wed, 02 Mar 2022 20:56:01 GMT",
            "content-type": "text/xml",
            "content-length": "215",
        },
        "RetryAttempts": 0,
    }
}


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
        sqs_client = boto3.client("sqs", region_name=self.region)
        response = sqs_client.delete_message(
            QueueUrl=self.queueu_url,
            ReceiptHandle=receipt_handle,
        )
        pprint(response)
        # x = DeleteResponse(**response)
        return response


if __name__ == "__main__":
    msgnr = Messenger(
        queueu_url="https://eu-central-1.queue.amazonaws.com/717687450252/example-queue",
        region="eu-central-1",
    )
    msg = msgnr.send_message("message 1")
    msg = msgnr.send_message("message 2")
    msg = msgnr.send_message("message 3")
    msg = msgnr.send_message("message 4")
    msg = msgnr.send_message("message 5")

    msg_read = msgnr.read_messages(nr_of_messages=3)

    for m in msg_read:
        m = Message(**m)
        print(f"read message {m.Body}")
        msgnr.delete_message(receipt_handle=m.ReceiptHandle)
