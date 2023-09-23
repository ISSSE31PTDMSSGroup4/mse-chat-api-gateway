
import aws_cdk as cdk
import os
from constructs import Construct

#experimental packages that need to be installed seperately
import aws_cdk.aws_apigatewayv2_alpha as apigatewayv2
from aws_cdk.aws_apigatewayv2_authorizers_alpha import HttpLambdaAuthorizer, HttpLambdaResponseType
from  aws_cdk.aws_apigatewayv2_integrations_alpha import HttpLambdaIntegration


class ApiGatewayWithLambdaAuthorizerStack(cdk.Stack):

    def __init__(self, scope: Construct,  id: str, lambda_dict, **kwargs) -> None:
        super().__init__(scope, id ,**kwargs)

        code_bucket = cdk.aws_s3.Bucket(
            self,
            'msechat_authorizer_lambda_code',
            removal_policy=cdk.RemovalPolicy.DESTROY  # For demonstration purposes only
        )
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


        mockGetUserProfile= lambda_dict['Get_User_Profile']
        GetUserProfile_integration = HttpLambdaIntegration("mockProfileIntegration", mockGetUserProfile)
        
        mockGetQuizListByUser=lambda_dict['Get_Quiz_List_By_User']
        GetQuizListByUser_integration = HttpLambdaIntegration("mockGetQuizListByUserIntegration",mockGetQuizListByUser)

        mockGetQuizDetail = lambda_dict['Get_Quiz_Detail']
        GetQuizDetail_integration = HttpLambdaIntegration("mockGetQuizDetailIntegration",mockGetQuizDetail)

        mockCreateQuiz = lambda_dict['Create_Quiz']
        CreateQuiz_integration = HttpLambdaIntegration("mockCreateQuizIntegration", mockCreateQuiz)

        mockUpdateQuiz = lambda_dict['Update_Quiz']
        UpdateQuiz_integration = HttpLambdaIntegration("mockUpdateQuizIntegration",mockUpdateQuiz)

        mockRemoveQuiz = lambda_dict['Remove_Quiz']
        RemoveQuiz_integration = HttpLambdaIntegration("mockRemoveQuizIntegration",mockRemoveQuiz)

        mockCreateQuizQuestion = lambda_dict['Create_Quiz_Question']
        CreateQuizQuestion_integration = HttpLambdaIntegration("mockCreateQuizQuestionIntegration",mockCreateQuizQuestion)

        mockRemoveQuizQuestion = lambda_dict['Remove_Quiz_Question']
        RemoveQuizQuestion_integration = HttpLambdaIntegration('mockRemoveQuizQuestionIntegration',mockRemoveQuizQuestion)

        mockModifyQuizQuestion = lambda_dict['Modify_Quiz_Question']
        ModifyQuizQuestion_integration = HttpLambdaIntegration('mockModifyQuizQuestionIntegration',mockRemoveQuizQuestion)

        mockSubmitQuiz = lambda_dict['Submit_Quiz']
        SubmitQuiz_integration = HttpLambdaIntegration('mockSubmitQuizIntegration',mockSubmitQuiz)

        mockGetQuizQuestionCorrectedCount = lambda_dict['Get_Quiz_Question_Corrected_Count']
        GetQuizQuestionCorrectedCount_integration = HttpLambdaIntegration('mockGetQuizQuestionCorrectedCountIntegration',mockGetQuizQuestionCorrectedCount)


        http_api = apigatewayv2.HttpApi(
            self,
            'HttpApi',
        )

        http_api.add_routes(
            path="/user/profile",
            methods=[apigatewayv2.HttpMethod.GET],
            integration=GetUserProfile_integration,
            #authorizer= authorizer
        )

        http_api.add_routes(
            path="/quiz/list",
            methods=[apigatewayv2.HttpMethod.GET],
            integration=GetQuizListByUser_integration,
            #authorizer= authorizer
        )
        http_api.add_routes(
            path="/quiz/detail",
            methods=[apigatewayv2.HttpMethod.GET],
            integration=GetQuizListByUser_integration,
            #authorizer= authorizer
        )
        http_api.add_routes(
            path="/quiz",
            methods = [apigatewayv2.HttpMethod.POST],
            integration=CreateQuiz_integration,
            #authorizer= authorizer
        )
        http_api.add_routes(
            path="/quiz",
            methods = [apigatewayv2.HttpMethod.PUT],
            integration=UpdateQuiz_integration,
            #authorizer= authorizer
        )
        http_api.add_routes(
            path="/quiz",
            methods = [apigatewayv2.HttpMethod.DELETE],
            integration=RemoveQuiz_integration,
            #authorizer= authorizer
        )
        http_api.add_routes(
            path="/quiz/question",
            methods = [apigatewayv2.HttpMethod.POST],
            integration=CreateQuizQuestion_integration,
            #authorizer= authorizer
        )
        http_api.add_routes(
            path="/quiz/question",
            methods = [apigatewayv2.HttpMethod.DELETE],
            integration=RemoveQuizQuestion_integration,
            #authorizer= authorizer
        )
        http_api.add_routes(
            path="/quiz/question",
            methods = [apigatewayv2.HttpMethod.PUT],
            integration=ModifyQuizQuestion_integration,
            #authorizer= authorizer
        )
        http_api.add_routes(
            path="/quiz/submit",
            methods = [apigatewayv2.HttpMethod.POST],
            integration=SubmitQuiz_integration,
            #authorizer= authorizer
        )
        http_api.add_routes(
            path="/quiz/question/correct",
            methods = [apigatewayv2.HttpMethod.GET],
            integration=GetQuizQuestionCorrectedCount_integration,
            #authorizer= authorizer
        )