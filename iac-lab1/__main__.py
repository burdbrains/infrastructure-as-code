"""A Python Pulumi program"""

import pulumi
import pulumi_aws as aws
import os
import mimetypes

config = pulumi.Config()
site_dir = config.require('siteDir')
stack = pulumi.get_stack()

# "my-s3-bucket" is called the 'logical name'
# example = aws.s3.BucketV2("example", bucket="my-tf-example-bucket")
new_bucket = aws.s3.BucketV2('new-bucket', bucket=f'my-s3-new-bucket-{stack}')

new_bucket_ownership_controls = aws.s3.BucketOwnershipControls(f'{stack}-s3-ownership',
    bucket=new_bucket.id,
    rule={
        'object_ownership': 'BucketOwnerPreferred',
    })

new_bucket_public_access = aws.s3.BucketPublicAccessBlock(f'{stack}-s3-accessblock',
                                                      bucket=new_bucket.id,
                                                      block_public_acls=False,
                                                      block_public_policy=False,
                                                      ignore_public_acls=False,
                                                      restrict_public_buckets=False
                                                      )

new_bucket_acl = aws.s3.BucketAclV2(f'{stack}-s3-acl',
                                bucket=new_bucket.id,
                                acl='public-read',
                                opts=pulumi.ResourceOptions(depends_on=[
                                    new_bucket_public_access,
                                    new_bucket_ownership_controls
                                ]))

new_bucket_website = aws.s3.BucketWebsiteConfigurationV2(f'{stack}-s3-webconfig',
                                                        bucket=new_bucket.id,
                                                        index_document={
                                                            'suffix': 'index.html'
                                                        })

for cfile in os.listdir(site_dir):
    filepath = os.path.join(site_dir, cfile)
    mime_type, _unneeded = mimetypes.guess_type(filepath)
    obj = aws.s3.BucketObject(cfile,
                            bucket=new_bucket.id,
                            source=pulumi.FileAsset(filepath),
                            acl="public-read",
                            content_type=mime_type
                            )

pulumi.export(f'{stack}_bucket_name', new_bucket.bucket)
pulumi.export(f'{stack}_bucket_endpoint', pulumi.Output.concat('http://', new_bucket_website.website_endpoint))