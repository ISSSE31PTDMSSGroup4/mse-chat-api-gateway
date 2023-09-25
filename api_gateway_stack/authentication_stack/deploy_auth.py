
import aws_cdk as cdk
import os
from constructs import Construct

####requires aws-lambda-python-alpha
import aws_cdk.aws_lambda_python_alpha as python
APP_URL = 'https://issse31ptdmss.xyz/'

class DeployAuthStack(cdk.Stack):
     def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.lambda_dict = {}

        Initate_Auth_Lambda = cdk.aws_lambda.Function(
            self,
            'intiateAuthLambda',
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_8,
            handler='lambda_function.lambda_handler',
            code=cdk.aws_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__),'initiate_auth')), 
            timeout=cdk.Duration.seconds(10),
            environment={
                "APP_URL": APP_URL
            }
        )
        self.lambda_dict["Initiate_auth"]=Initate_Auth_Lambda

        #autogenerates layers
        Postlogin_Lambda = python.PythonFunction(
            self,
            'postLoginLambda',
            entry=f"{os.path.join(os.path.dirname(__file__),'postlogin')}",
            index="lambda_function.py",
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_10, #needs 3.10 for urllib error
            handler="lambda_handler"
        )
        self.lambda_dict["postlogin"]=Postlogin_Lambda


app = cdk.App()
DeployAuthStack(app, "DeployAuthStack")
app.synth()