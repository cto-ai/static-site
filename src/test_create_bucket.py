import sys
import os
import boto3
import create_bucket
import unittest
from botocore.exceptions import ClientError as ClientExceptionError
from unittest.mock import MagicMock

class TestCreateBucket(unittest.TestCase):
    # Test for check_existing_bucket.
    def test_check_existing_bucket(self):
        """Mock test if owner's bucket already exist."""
        cb = create_bucket.CreateBucket()
        bucket_name = 'unittest-ctoai-staticsite'
        s3_client = cb.create_client('access_id', 'access_key', region=None) # Create S3 client object.
        s3_client.head_bucket = MagicMock()

        existing_bucket = cb.check_existing_bucket(s3_client, bucket_name)
        s3_client.head_bucket.assert_called_with(Bucket=bucket_name)
        self.assertEqual(existing_bucket, True)

    # Test for create_client.
    def test_create_bucket_without_region(self):
        """Mock test if region is not specified."""
        cb = create_bucket.CreateBucket()
        bucket_name = 'unittest-ctoai-staticsite'
        public_read = 'public-read'
        s3_client = cb.create_client('access_id', 'access_key', region=None) # Create S3 client object.
        s3_client.create_bucket = MagicMock()

        _create_bucket = cb.create_s3_bucket(s3_client, bucket_name, public_read, region=None)
        s3_client.create_bucket.assert_called_with(Bucket=bucket_name, ACL=public_read)
        self.assertEqual(_create_bucket, True)

    def test_create_bucket_with_region(self):
        """Mock test if region is specified."""
        cb = create_bucket.CreateBucket()
        bucket_name = 'unittest-ctoai-staticsite'
        public_read = 'public-read'
        location = 'us-west-2'
        s3_client = cb.create_client('access_id', 'access_key', region=location) # Create S3 client object.
        s3_client.create_bucket = MagicMock()

        _create_bucket = cb.create_s3_bucket(s3_client, bucket_name, public_read, region=location)
        s3_client.create_bucket.assert_called_with(Bucket=bucket_name, ACL=public_read, CreateBucketConfiguration = {'LocationConstraint': location})
        self.assertEqual(_create_bucket, True)

if __name__ == '__main__':
    unittest.main()