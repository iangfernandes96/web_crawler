#!/usr/bin/python3

"""
Module: s3_client
Description: Wrapper functions for interacting with an S3-compatible service.
"""

import boto3
from io import BytesIO

ENDPOINT_URL = "http://localstack:4566/"
AWS_S3_CREDS = {
    "aws_access_key_id": "foobar",
    "aws_secret_access_key": "foobar",
    "region_name": "us-east-1"
}

s3_client = boto3.client("s3", endpoint_url=ENDPOINT_URL, **AWS_S3_CREDS)


def upload_file_object_to_s3(file_bytes: BytesIO,
                             bucket_name: str,
                             file_name: str):
    """
    Uploads a BytesIO object to the specified S3 bucket with the given filename.

    Args: # noqa
    - file_bytes (BytesIO): BytesIO object containing the file content.
    - bucket_name (str): Name of the S3 bucket.
    - file_name (str): Desired filename for the object in the S3 bucket.

    Returns:
    - None
    """
    s3_client.upload_fileobj(file_bytes, bucket_name, file_name)


def get_presigned_s3_link(client_method_name: str,
                          params: dict,
                          expiration: int) -> str:
    """
    Generates a presigned URL for a specific S3 client method.

    Args:   # noqa
    - client_method_name (str): Name of the S3 client method (e.g., 'get_object').
    - params (dict): Parameters to be passed to the S3 client method.
    - expiration (int): Expiration time for the presigned URL (in seconds).

    Returns:
    - str: Presigned URL for the specified S3 client method.
    """
    return s3_client.generate_presigned_url(client_method_name,
                                            Params=params,
                                            ExpiresIn=expiration)
