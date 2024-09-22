"""A Python Pulumi program"""

import pulumi
import pulumi_aws as aws

# "my-s3-bucket" is called the 'logical name'
bucket = aws.s3.Bucket("my-s3-bucket")
pulumi.export("bucket_name", bucket.bucket)