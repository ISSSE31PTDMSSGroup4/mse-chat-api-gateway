
import aws_cdk as cdk
import os
from constructs import Construct

#experimental packages that need to be installed seperately
import aws_cdk.aws_apigatewayv2_alpha as apigatewayv2
from aws_cdk.aws_apigatewayv2_authorizers_alpha import HttpLambdaAuthorizer, HttpLambdaResponseType
from  aws_cdk.aws_apigatewayv2_integrations_alpha import HttpLambdaIntegration


mock_arn = 'arn:aws:lambda:ap-southeast-1:040501387259:function:mockapi' ###mock_function ARN


class ApiGatewayWithLambdaAuthorizerStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        code_bucket = cdk.aws_s3.Bucket(
            self,
            'msechat_authorizer_lambda_code',
            removal_policy=cdk.RemovalPolicy.DESTROY  # For demonstration purposes only
        )
        mock_profile_function= cdk.aws_lambda.Function.from_function_arn(
        self,
        'mockapi',
        mock_arn
        )

        mock_profile_integration = HttpLambdaIntegration("mockProfileIntegration", mock_profile_function)


        # Define the Lambda function for authorization
        authorizer_lambda = cdk.aws_lambda.Function(
            self,
            'AuthorizerLambda',
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_8,
            handler='index.lambda_handler',
            code=cdk.aws_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), 'authorizer_lambda')), 
            timeout=cdk.Duration.seconds(10),
        )

        # Grant necessary permissions to the Lambda function
        code_bucket.grant_read(authorizer_lambda)
        authorizer_lambda.add_to_role_policy(cdk.aws_iam.PolicyStatement(
            actions=["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
            resources=["*"]
        ))

        authorizer = HttpLambdaAuthorizer(
            "mse-chat-authorizer", authorizer_lambda,
            response_types=[HttpLambdaResponseType.SIMPLE]
            )
        http_api = apigatewayv2.HttpApi(
            self,
            'HttpApi',
        )
        http_api.add_routes(
            path="/user/profile",
            methods=[apigatewayv2.HttpMethod.GET],
            integration=mock_profile_integration,
            authorizer= authorizer
        )


app = cdk.App()
ApiGatewayWithLambdaAuthorizerStack(app, "ApiGatewayWithLambdaAuthorizerStack")
app.synth()