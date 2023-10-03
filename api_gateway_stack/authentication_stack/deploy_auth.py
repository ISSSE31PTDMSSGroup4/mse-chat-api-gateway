
import aws_cdk as cdk
import os
#config contains confidential information and is omitted
try:
  from . import config
except:
  import config
from constructs import Construct

####requires aws-lambda-python-alpha
import aws_cdk.aws_lambda_python_alpha as python


class DeployAuthStack(cdk.Stack):
     def __init__(self, scope: Construct, id: str, APP_PRIVATE_KEY_SSM_PARAM, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.lambda_dict = {}

        Initate_Auth_Lambda = cdk.aws_lambda.Function(
            self,
            'intiateAuthLambda',
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_8,
            handler='lambda_function.lambda_handler',
            code=cdk.aws_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__),'initiate_auth')), 
            timeout=cdk.Duration.seconds(3),
            environment={
                'COGNITO_USER_POOL_CLIENT_ID':config.COGNITO_USER_POOL_CLIENT_ID,
                'AWS_COGNITO_DOMAIN':config.AWS_COGNITO_DOMAIN,
                'APP_REDIRECT_URL':config.APP_REDIRECT_URL
            }
        )
        self.lambda_dict["Initiate_auth"]=Initate_Auth_Lambda


        #autogenerates layers
        Postlogin_Lambda = python.PythonFunction(
            self,
            'postLoginLambda',
            entry=f"{os.path.join(os.path.dirname(__file__),'postlogin')}",
            index="lambda_function.py",
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_9, #needs 3.10 for urllib error
            handler="lambda_handler",
            timeout=cdk.Duration.seconds(5),
            memory_size=256,
            environment={
                'COGNITO_USER_POOL_CLIENT_ID':config.COGNITO_USER_POOL_CLIENT_ID,
                'AWS_COGNITO_USER_POOL_ID':config.AWS_COGNITO_USER_POOL_ID,
                'AWS_COGNITO_DOMAIN':config.AWS_COGNITO_DOMAIN,
                'APP_REDIRECT_URL':config.APP_REDIRECT_URL,
                'APP_PRIVATE_KEY_SSM_PARAM_ARN':APP_PRIVATE_KEY_SSM_PARAM.parameter_name,
                'ACCESS_TOKEN_EXPIRY': config.ACCESS_TOKEN_EXPIRY,
                'APP_URL' : config.APP_URL
            }
        )
        APP_PRIVATE_KEY_SSM_PARAM.grant_read(Postlogin_Lambda)


        self.lambda_dict["postlogin"]=Postlogin_Lambda
        
        Logout_Lambda = cdk.aws_lambda.Function(
            self,
            'LogoutLambda',
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_8,
            handler='lambda_function.lambda_handler',
            code=cdk.aws_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__),'logout')), 
            timeout=cdk.Duration.seconds(3),
            environment={
                'COGNITO_USER_POOL_CLIENT_ID':config.COGNITO_USER_POOL_CLIENT_ID,
                'AWS_COGNITO_DOMAIN':config.AWS_COGNITO_DOMAIN,
                'APP_URL':config.APP_URL
            }
        )
        self.lambda_dict["Logout"]=Logout_Lambda

