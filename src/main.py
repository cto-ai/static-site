import sys, os
import logos
import secrets
import create_bucket
from cto_ai import ux

def keyboard_exit() -> None:
    """Prints keyboard exist warning message."""
    print("Exiting Op.")
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

"""
Main function
"""
def main() -> None:
    # Logo branding.
    logos.logo_print()
    ux.print(logos.intro)

    public_read = 'public-read'
    region = 'us-west-2' # hardcoded.
    object_name = 'views/home.html'

    # Create Secrets objects.
    secret_ = secrets.Secrets()
    access_key_id = secret_.prompt_aws_access_key_id()
    secret_access_key = secret_.prompt_aws_secret_access_key()

    # Create Client objects.
    cb = create_bucket.CreateBucket()
    s3_client = cb.create_client(access_key_id, secret_access_key)

    # Prompt for a bucket-name and check for existing bucket.
    for n in range(5):
        bucket_name = cb.prompt_bucket_name()
        bucket_already_exist = cb.check_existing_bucket(s3_client, bucket_name)
        if not bucket_already_exist:
            break
        if n == 5:
            ux.print("You've exceeded the limit of retries. Exiting Op.")
            os._exit(0)

    # Create a S3 bucket.
    cb.create_s3_bucket(s3_client, bucket_name, public_read, region) # Create bucket.
    cb.website_config(s3_client, bucket_name) # Enable static website hosting.

    # Upload a file to a S3 bucket.
    generator = cb.absolutepath_dir()
    for filename in generator:
        cb.upload_file(s3_client, filename, bucket_name, object_name=None)

    # Print URL.
    cb.construct_url(bucket_name, object_name, region) 
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        keyboard_exit()