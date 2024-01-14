#!/usr/bin/python3

import boto3

ENDPOINT_URL = "http://localstack:4566/"
AWS_S3_CREDS = {
    "aws_access_key_id": "foobar",
    "aws_secret_access_key": "foobar",
    "region_name": "us-east-1"
}

client = boto3.client("s3", endpoint_url=ENDPOINT_URL, **AWS_S3_CREDS)
