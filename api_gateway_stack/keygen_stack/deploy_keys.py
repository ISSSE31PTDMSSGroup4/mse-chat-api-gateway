import aws_cdk as cdk
import os
from constructs import Construct
import json
import uuid
####pycryptodome, jwcrypto required

from Crypto.PublicKey import RSA
from jwcrypto import jwk

generate_new_keys = False

APP_URL = 'https://issse31ptdmss.xyz/' #change if necessary, or abstract to env

class DeployKeyStack(cdk.Stack):
     def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.private_key_param =None
        
        if generate_new_keys:
            #generate private key
            key = RSA.generate(2048)
            key_file = open('private_key.pem','wb')
            key_file.write(key.export_key('PEM'))
            key_file.close()
        else:
            #read private key
            key_file = open('private_key.pem','r')
            key = RSA.import_key(key_file.read())
            key_file.close()


        #store the key passphrase (note: for production use AWS KMS to encrypt the private key instead of SSM. SSM parameter store is free but KMS cost USD$1/key)

        private_key_param = cdk.aws_ssm.StringParameter(
            self,
            'PrivateKeyParameter',
            parameter_name='/APP/PRIVATE_KEY',
            string_value=key.export_key().decode('utf-8')
        )

        public_key = jwk.JWK.from_pem(bytes(key.export_key().decode('utf-8'), 'utf-8')).export_public()

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
            sources=[cdk.aws_s3_deployment.Source.json_data('public_key.json', public_key)],
            destination_bucket=public_key_bucket,
        )
        
        #make it exportable
        self.private_key_param = private_key_param



app = cdk.App()
DeployKeyStack(app, "DeployKeyStack")
app.synth()