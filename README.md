# aws-python
Doing stuff with AWS using Python


# Setting things up

You can pip install boto3 and put in place your credentials following [this](https://docs.aws.amazon.com/rekognition/latest/dg/setup-awscli-sdk.html) guide.

What I am working with is 2 files in the .aws directory that is located in my homedir:

A file called `config`:
```
[default]
region=eu-central-1
```

And a file called `credentials`:
```
[default]
aws_access_key_id = ________
aws_secret_access_key = ________
```

# Boto3

The SDK provides an object-oriented API as well as low-level access to AWS services. The `boto3` library is built on top of `botocore`, which also serves as the foundation to the AWS CLI. The `botocore` libray provides the low-level clients, session, credentials and configuration data that `boto3` builds on.

## Botocore

The `botocore` package is a low level interface that is responsible for:
- access to all available AWS services and operations within a service
- marshall parameters for an operation in the correct format (serialization)
- signing the request
- deserialization of the response


This package has does not really provide ergonomics nor does it provide any abstractions, that is where `boto3` comes in.

## Config object.

The configuration object can be used to configure client-specific behaviors, such as the amount of retries or the region name.

```python
import boto3
from botocore.config import Config

client_cfg = Config(
    region_name = 'eu-central-1',    
    retries = {
        'max_attempts': 2,
    }
)

client = boto3.client('s3', config=client_cfg)
```

## Configuration settings.

You can configure the way boto3 behaves by modifying environmental variables and by specifying a configuration file.

## Credentials

There are a number of options to provide boto3 with credentials:
- put then in a configuration file
- pass them to the function in a script
- set them as an environment variale (boto3 has default env values it will attempt to read)

Docs:
[docs](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html#)
[services](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/index.html)

## Clients and resources

Clients and resources offer access to the AWS services. Clients allow you to access low-level, or more granular, access to the service. Resources offer higher-level access. 

### Clients:

```
Clients provide a low-level interface to AWS whose methods map close to 1:1 with service APIs. All service operations are supported by clients. Clients are generated from a JSON service definition file that is maintained by AWS.
```

Creating a client can be done as follows:

```python
import boto3

ssm = boto3.client("ssm")
```


Clients come with waiters that you can interface with. These waiters will poll the status of an AWS resource and inform you when the awaited state is reached or when there is a failure.

The `waiter_names` method reveals the available waiters:

```python
>>> import boto3
>>> s3 = boto3.client("s3")
>>> s3.waiter_names
['bucket_exists', 'bucket_not_exists', 'object_exists', 'object_not_exists']

```

Client sessions are thread-safe, though the documentation does list some [caveats](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/clients.html#caveats).


### Resource:

```
Resources represent an object-oriented interface to Amazon Web Services (AWS). They provide a higher-level abstraction than the raw, low-level calls made by service clients.
```

Resources are generated from the JSON resource definition file. As noted earlier, you can define a resource as follows:

```python
import boto3

s3_resource = boto3.resource("s3")
```

Resources do not offer the same level of granularity as clients, however, through a resource you can also access the client methods:

```python
import boto3

s3_resource = boto3.resource("s3")
s3_client = s3_resource.meta.client
print(s3_client.list_buckets())
```

Every resource instance that you create has attributes and methods that can be devided as follows:
- `identifiers`: example, bucket name
- `attributes`: example, last modified
- `actions`: methods that make a call to the service to do something (create, delete, etc.)
- `references`: references to attributes related to the resource (example, ec2 subnet)
- `sub-resources`: related to the resource. Example, s3 `bucket_name`. TheS3 object cannot exist without a bucket name.
- `collections`: iterable interface to a group of resources

Note about resources: they are NOT threadsafe!

## Session:

This refers to the session that is used to have boto interact with AWS. 

A default session to interact with AWS is created for you automatically when using boto. For instance, when you createa a low level client, boto3 acts as a proxy to the default session.

It is possible, using `boto3.session`, to manage your own sessions and use that session to create clients or resources. Every session can be given it's own configuration (keys, regions, etc.).

Session objects are _not_ thread safe. It is recommended that you create a session object for every thread of process.


## Collections

Collections provide an iterable interface to a group of resources and handle pagination for you.


Example on iterating all S3 buckets and printing their names:
```python
import boto3
s3_resource = boto3.resource("s3")

for bucket in s3_resource.buckets.all():
    print(f"  {bucket.name}")
```