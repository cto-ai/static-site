import logging
import os
import mimetypes
import boto3
from cto_ai import ux, sdk, prompt
from botocore.exceptions import ClientError as ClientExceptionError
from botocore.client import ClientError

class CreateBucket:
    def create_client(self, access_id, access_key, region=None) -> object:
        """S3 Client."""
        return boto3.client('s3', aws_access_key_id=access_id, aws_secret_access_key=access_key)

    def prompt_bucket_name(self) -> str:
        """Prompt for a S3 bucket name."""
        return prompt.input(name="bucket_name", message="Please enter a bucket name")

    def check_existing_bucket(self, s3_client, bucket_name) -> bool:
        """Checks for existing bucket."""
        try:
            if s3_client.head_bucket(Bucket=bucket_name): # Check for owner's existing bucket.
                return True
        except ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = e.response['Error']['Code']
            if error_code == '403': # Check if global bucket exist.
                return True
            elif error_code == '404': # Bucket doesn't exist.
                return False

    def create_s3_bucket(self, s3_client, bucket_name, public_read, region=None) -> bool:
        """
        Create an S3 bucket

        If a region is not specified, the bucket is created in the S3 default
        region (us-east-1).

        :param bucket_name: Bucket to create
        :param region: String region to create bucket in, e.g., 'us-west-2'
        :return: True if bucket created, else False
        """
        try:
            if region is None:
                s3_client.create_bucket(Bucket=bucket_name, ACL=public_read)
            else:
                location = {'LocationConstraint': region}
                s3_client.create_bucket(Bucket=bucket_name, ACL=public_read,
                                        CreateBucketConfiguration=location)
            return True
        except ClientExceptionError as e:
            logging.error(e)
            return False

    def website_config(self, s3_client, bucket_name) -> None:
        """This function enables the AWS S3 bucket to host a website."""
        s3_client.put_bucket_website(
            Bucket=bucket_name,
            WebsiteConfiguration={
            'ErrorDocument': {'Key': 'error.html'},
            'IndexDocument': {'Suffix': 'home.html'},
            }
        )

    def absolutepath_dir(self) -> None:
        """Generator function used with the upload function. This is used for uploading more than 1 file."""
        path = './website/'
        for root, _, files in os.walk(path):
            files[:] = [f for f in files if not f.startswith('.')] # Ignore dot files.
            for filename in files:
                yield os.path.join(root, filename)

    def upload_file(self, s3_client, file_name, bucket_name, object_name=None) -> bool:
        """
        Upload a file to a S3 bucket

        :param file_name: The path ot the file to upload
        :param bucket_name: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        filename = file_name.replace('./website/', '', 1) # This is needed for the upload function.

        # If S3 object_name was not specified, use file_name.
        if object_name is None:
            object_name = filename

        # Upload files.
        try:
            guess_type = mimetypes.guess_type(filename)[0]
            known_types = ['text/html', 'text/css', 'application/javascript', 'application/json', 'image/svg+xml', 'image/png']
            if guess_type in known_types:
                # As strange as this is, './website/' is needed in the parameter, even though the string was removed earlier in `filename`.
                # You won't be able to upload objects to the bucket if you don't remove the string and just use `file_name`.
                s3_client.upload_file('./website/'+filename, bucket_name, object_name, ExtraArgs={'ACL': 'public-read', 'ContentType': guess_type})
            else:
                s3_client.upload_file('./website/'+filename, bucket_name, object_name, ExtraArgs={'ACL': 'public-read'})
        except ClientExceptionError as e:
            logging.error(e)
            return False
        return True

    def construct_url(self, bucket_name, object_name, region=None) -> None:
        """Construct object URL and print it."""
        url = "https://%s.s3-%s.amazonaws.com/%s" % (bucket_name, region, object_name)
        ux.print(url)