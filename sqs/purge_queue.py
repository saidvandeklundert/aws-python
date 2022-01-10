from pprint import pprint
import boto3


def purge_queue(queueu_url: str, region_name: str):
    sqs_client = boto3.client("sqs", region_name=region_name)
    response = sqs_client.purge_queue(QueueUrl=queueu_url)
    return response


if __name__ == "__main__":
    """
    Note!
    This script assumed the queue is empty.
    """
    queueu_url = "https://eu-central-1.queue.amazonaws.com/717687450252/example-queue"
    region_name = "eu-central-1"

    print("Purging queue:")
    pugre_response = purge_queue(queueu_url=queueu_url, region_name=region_name)
    pprint(pugre_response)
