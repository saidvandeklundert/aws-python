import time
import boto3
from dataclasses import dataclass
from enum import Enum


class InstanceState(Enum):
    """Enum to indicate the state of an instance"""

    PENDING = "pending"
    RUNNING = "running"
    SHUTTING_DOWN = "shutting-down"
    TERMINATED = "terminated"
    STOPPING = "stopping"
    STOPPED = "stopped"

    def __str__(self):
        return str(self.value)


@dataclass
class InstanceCreateParameters:
    ami: str
    instance_type: str
    key_name: str
    subnet_id: str


@dataclass
class InstanceTerminationParameters:
    instances: list[str]
    region_name: str = "eu-central-1"


def create_instance(ec2_param: InstanceCreateParameters) -> str:
    """Launches an EC2 instance using the provided parameters."""
    ec2 = boto3.resource("ec2")

    instance = ec2.create_instances(
        ImageId=ec2_param.ami,
        InstanceType=ec2_param.instance_type,
        KeyName=ec2_param.key_name,
        SubnetId=ec2_param.subnet_id,
        MaxCount=1,
        MinCount=1,
    )
    created_instance = instance[0].id
    print("New instance created:", instance[0].id)

    return created_instance


def terminate_instance(instance_id: str):
    """Terminates target instance ID and returns the reponse."""
    ec2_client = boto3.client("ec2", region_name="eu-central-1")
    response = ec2_client.terminate_instances(InstanceIds=[instance_id])
    print(response)


def get_running_instances(*, region_name: str) -> list[dict]:
    """Returns a list of running instances"""

    ec2_client = boto3.client("ec2", region_name=region_name)
    reservations = ec2_client.describe_instances(
        Filters=[
            {
                "Name": "instance-state-name",
                "Values": [InstanceState.RUNNING.value],  # Use InstanceState enum
            }
        ]
    ).get("Reservations")
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances
    return reservations


if __name__ == "__main__":

    ec2_param = InstanceCreateParameters(
        ami="ami-0eb7496c2e0403237",
        instance_type="t2.micro",
        key_name="said-kp",
        subnet_id="subnet-0f35c79b2e49cd7d0",
    )
    instance_id = create_instance(ec2_param=ec2_param)

    time.sleep(30)
    reservations = get_running_instances(region_name="eu-central-1")

    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            public_ip = instance.get("PublicIpAddress", "")
            private_ip = instance.get("PrivateIpAddress", "")
            print(
                f"""
instance:
  instanc-id: {instance_id}
  instance-type: {instance_type}
  public-ip: {public_ip}
  private-ip: {private_ip}
            """
            )

    terminate_instance(instance_id=instance_id)
