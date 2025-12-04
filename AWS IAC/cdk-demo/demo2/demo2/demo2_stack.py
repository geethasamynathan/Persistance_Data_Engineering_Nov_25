from aws_cdk import (
    Stack,
    aws_s3 as s3
)
from constructs import Construct

class Demo2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Create S3 bucket
        s3.Bucket(
            self,
            "MyDemoBucket",
            versioned=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED
        )
