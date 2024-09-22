"""A Python Pulumi program"""

import pulumi
import pulumi_aws as aws
import os

# "my-s3-bucket" is called the 'logical name'
bucket = aws.s3.Bucket('my-s3-bucket')
filepath = os.path.join('site', 'index.html')
obj = aws.s3.BucketObject('index.html',
                          bucket=bucket.bucket,
                          source=pulumi.FileAsset(filepath)
                          )

pulumi.export('bucket_name', bucket.bucket)