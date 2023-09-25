import aws_cdk as cdk
import os
from constructs import Construct
import json
import uuid
####pycryptodome required

from Crypto.PublicKey import RSA

APP_URL = 'https://issse31ptdmss.xyz/' #change if necessary, or abstract to env

class DeployKeyStack(cdk.Stack):
     def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        #generate private key
        key = RSA.generate(2048)

        #generate key passphrase
        key_passphrase = str(uuid.uuid4())

        #store the key passphrase (note: for production use AWS KMS to encrypt the private key instead of SSM. SSM parameter store is free but KMS cost USD$1/key)

        private_key_passphrase = cdk.aws_ssm.StringParameter(
            self,
            'PrivateKeyPassphrase',
            parameter_name='/APP/PRIVATE_KEY_PASSPHRASE',
            string_value=key_passphrase
        )

        private_key_param = cdk.aws_ssm.StringParameter(
            self,
            'PrivateKeyParameter',
            parameter_name='/APP/ENCRYPTED_PRIVATE_KEY',
            string_value=key.export_key(passphrase=key_passphrase, pkcs=8,protection="scryptAndAES128-CBC").decode('utf-8')
        )

        public_key = {
            'kty': 'RSA',
            'n': key.n,
            'e': key.e,
        }

        public_key_bucket = cdk.aws_s3.Bucket(
            self,
            'msechat_public_key_bucket',
            versioned=False,
            object_ownership=cdk.aws_s3.ObjectOwnership.OBJECT_WRITER,
            block_public_access=cdk.aws_s3.BlockPublicAccess(block_public_policy=False,block_public_acls=False,ignore_public_acls=False,restrict_public_buckets=False),
            #access_control=cdk.aws_s3.BucketAccessControl.PUBLIC_READ,
            removal_policy=cdk.RemovalPolicy.DESTROY  # For demonstration purposes only
        )

        public_key_bucket.add_to_resource_policy(cdk.aws_iam.PolicyStatement(
            actions=['s3:GetObject'],
            resources=[f'arn:aws:s3:::{public_key_bucket.bucket_name}/public_key.json'],
            effect=cdk.aws_iam.Effect.ALLOW,
            principals=[cdk.aws_iam.ArnPrincipal('*')]
        ))
        deployment = cdk.aws_s3_deployment.BucketDeployment(self, "DeployPublicKey",
            sources=[cdk.aws_s3_deployment.Source.json_data('public_key.json', json.dumps(public_key))],
            destination_bucket=public_key_bucket,
        )



app = cdk.App()
DeployKeyStack(app, "DeployKeyStack")
app.synth()