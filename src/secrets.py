import boto3
from cto_ai import prompt

class Secrets:
    def prompt_aws_access_key_id(self) -> str:
        """Prompt for AWS Access Key ID."""
        return prompt.secret(name="aws_access_key_id", message="Please enter your AWS Access Key ID")

    def prompt_aws_secret_access_key(self) -> str:
        """Prompt for AWS Secret Access Key."""
        return prompt.secret(name="aws_secret_access_key", message="Please enter your AWS Secret Access Key")