from dataclasses import dataclass
import boto3
from typing import List
from pprint import pprint
from botocore.exceptions import ClientError
import csv


def create_table() -> None:
    """Creates a DynamoDB table if it does not already exist"""
    dynamo_db = boto3.client("dynamodb")
    response = dynamo_db.list_tables(Limit=100)
    if "Humans" in response["TableNames"]:
        dynamodb = boto3.resource("dynamodb")
        state = dynamodb.Table("Humans").table_status
        print(f"Humans table exists already and is in state {state}")

    else:
        dynamodb = boto3.resource("dynamodb")

        table = dynamodb.create_table(
            TableName="Humans",
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"},  # Partition key
                {"AttributeName": "name", "KeyType": "RANGE"},  # Sort key
            ],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "N"},
                {"AttributeName": "name", "AttributeType": "S"},
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1,
            },  # 1 RCU and 1 WCU is free!
        )

        table.meta.client.get_waiter("table_exists").wait(TableName="Humans")
        state = dynamodb.Table("Humans").table_status
        print(f"Humans table has been created and is in state {state}")


@dataclass
class Human:
    id: int
    name: str
    weight: int
    height: int


class DynamoDBRepository:
    def __init__(self):
        self.table_name = "Humans"
        self.resource = boto3.resource("dynamodb")
        self.client = boto3.client("dynamodb")
        self.table = self.resource.Table(self.table_name)

    def put_item(self, human: Human):
        """Update the table with an item."""
        response = self.table.put_item(Item=vars(human))
        pprint(response)

    def put_batch_item(self, humans: List[Human]):
        """Update the table with a batch of items."""
        with self.table.batch_writer() as batch:
            for human in humans:
                batch.put_item(Item=vars(human))

    def get_item(self, *, name, id_nr):
        """Return target item from the database."""
        try:
            response = self.table.get_item(Key={"id": id_nr, "name": name})
        except ClientError as e:
            print(e.response["Error"]["Message"])
        else:
            return response["Item"]

    def delete_item(self, human: Human):
        """Return target item from the database."""
        try:
            response = self.table.delete_item(Key={"id": human.id, "name": human.name})
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                print(e.response["Error"]["Message"])
            else:
                raise
        else:
            return response

    def get_all(self):
        """Scans the table and returns it."""
        devices_data = self.client.scan(TableName=self.table_name)
        return devices_data


HUMANS = [
    Human(id=1, name="Jan", weight=25, height=110),
    Human(id=2, name="Jan", weight=25, height=110),
    Human(id=3, name="Said", weight=85, height=185),
    Human(id=4, name="Anne", weight=50, height=158),
]


def humans_from_csv(file_name: str) -> List[Human]:
    humans: List[Human] = []
    with open(file_name, "rt") as f:
        csv_data = csv.DictReader(f)
        for row in csv_data:
            humans.append(
                Human(
                    id=int(row["id"]),
                    name=row["name"],
                    weight=int(row["weight"]),
                    height=int(row["height"]),
                )
            )
    return humans


if __name__ == "__main__":

    create_table()

    repo = DynamoDBRepository()
    for human in HUMANS:
        repo.put_item(human)

    moar_humans = humans_from_csv("data/humans.csv")

    repo.put_batch_item(moar_humans)

    pprint(repo.get_all())
    pprint(repo.get_item(name="Jan", id_nr=2))
    for human in HUMANS:
        repo.delete_item(human)
    for human in moar_humans:
        repo.delete_item(human)
    pprint(repo.get_all())
