# mse-chat-api-gateway

This is the cdk constructs for deployment of Mock API (at the moment) & authentication

The following stacks are present at the moment:

api_gateway_stack: stack for deploying API gateway and authorizer lambda resources

Authentication_stack: stack for deploying lambdas for authentication

keygen_stack: stack for deploying Private and public keys into SSM (for private key) and S3 (for private key). Note: for production settings, use KMS for key storage instead of SSm

mock_lambda_stack: stack for deploying mock lambdas for API testing

To use:

install AWS CDK for python, python, docker (for aws-lambda-python-alpha module)

Run pip install -r requirements.txt

Run cdk diff, then cdk deploy (if AWS credentials are set in account)