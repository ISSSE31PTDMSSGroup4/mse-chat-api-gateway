
import aws_cdk as cdk
import os
from constructs import Construct
#config contains confidential information and is omitted
try:
  from . import config
except:
  import config
#experimental packages that need to be installed seperately
import aws_cdk.aws_apigatewayv2_alpha as apigatewayv2
from aws_cdk.aws_apigatewayv2_authorizers_alpha import HttpLambdaAuthorizer, HttpLambdaResponseType
from  aws_cdk.aws_apigatewayv2_integrations_alpha import HttpLambdaIntegration, HttpUrlIntegration

####requires aws-lambda-python-alpha
import aws_cdk.aws_lambda_python_alpha as python


class ApiGatewayWithLambdaAuthorizerStack(cdk.Stack):

    def __init__(self, scope: Construct,  id: str, lambda_dict, auth_dict, APP_PUBLIC_KEY_SSM_PARAM,**kwargs) -> None:
        super().__init__(scope, id ,**kwargs)

        authorizer_lambda = python.PythonFunction(
            self,
            'AuthorizerLambda',
            entry=f"{os.path.join(os.path.dirname(__file__),'authorizer_lambda')}",
            index="lambda_function.py",
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_9, #needs 3.10 for urllib error
            handler="lambda_handler",
            timeout=cdk.Duration.seconds(5),
            memory_size=256,
            environment={
                'APP_PUBLIC_KEY_SSM_PARAM_ARN':APP_PUBLIC_KEY_SSM_PARAM.parameter_name,
                'APP_URL' : config.APP_URL
            }
        )
        APP_PUBLIC_KEY_SSM_PARAM.grant_read(authorizer_lambda)
        authorizer = HttpLambdaAuthorizer(
            "mse-chat-authorizer", authorizer_lambda,
            response_types=[HttpLambdaResponseType.SIMPLE],
            results_cache_ttl = cdk.Duration.minutes(15),
            identity_source=['$request.header.cookie']
            )
        
        #auth APIs
        InitiateAuth = auth_dict['Initiate_auth']
        InitiateAuth_integration = HttpLambdaIntegration("InitiateAuthIntegration", InitiateAuth)

        Postlogin = auth_dict['postlogin']
        Postlogin_integration = HttpLambdaIntegration("PostLoginIntegration", Postlogin)
        Logout = auth_dict['Logout']
        Logout_integration = HttpLambdaIntegration("LogoutIntegration", Logout)
        Refresh = auth_dict['Refresh']
        Refresh_integration = HttpLambdaIntegration("RefreshTokenIntegration",Refresh)

        ####
        
        #not in use
        #mockGetUserProfile= lambda_dict['Get_User_Profile']
        #GetUserProfile_integration = HttpLambdaIntegration("mockProfileIntegration", mockGetUserProfile)
        #####
        #for now, manually map request.path.proxy, because not working for some reason. not needed for prod 
        backend_integration = HttpUrlIntegration("backend_integration", config.API_URL, parameter_mapping = apigatewayv2.ParameterMapping().append_header("X-USER",apigatewayv2.MappingValue.context_variable("authorizer.user")).overwrite_path(apigatewayv2.MappingValue.request_path()))

        '''
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
        '''

        http_api = apigatewayv2.HttpApi(
            self,
            'HttpApi',
        )

        #authentication
        http_api.add_routes(
            path = "/api/auth/initiate_auth",
            methods=[apigatewayv2.HttpMethod.GET],
            integration = InitiateAuth_integration
        )
        http_api.add_routes(
            path = "/api/auth/postlogin",
            methods=[apigatewayv2.HttpMethod.GET],
            integration = Postlogin_integration
        )
        http_api.add_routes(
            path = "/api/auth/logout",
            methods=[apigatewayv2.HttpMethod.GET],
            integration = Logout_integration
        )
        http_api.add_routes(
            path = "/api/auth/refresh",
            methods = [apigatewayv2.HttpMethod.GET],
            integration = Refresh_integration,
            authorizer = authorizer
        )
        #backend integration
        http_api.add_routes(
            path="/api/{proxy+}",
            methods=[apigatewayv2.HttpMethod.ANY],
            integration=backend_integration,
            authorizer= authorizer
        )
        #mock API
        '''
        http_api.add_routes(
            path="/api/user/profile",
            methods=[apigatewayv2.HttpMethod.GET],
            integration=GetUserProfile_integration,
            #authorizer= authorizer
        )
        

        http_api.add_routes(
            path="/api/quiz/list",
            methods=[apigatewayv2.HttpMethod.GET],
            integration=GetQuizListByUser_integration,
            #authorizer= authorizer
        )
        http_api.add_routes(
            path="/api/quiz/detail",
            methods=[apigatewayv2.HttpMethod.GET],
            integration=GetQuizDetail_integration,
            #authorizer= authorizer
        )
        http_api.add_routes(
            path="/api/quiz",
            methods = [apigatewayv2.HttpMethod.POST],
            integration=CreateQuiz_integration,
            #authorizer= authorizer
        )
        http_api.add_routes(
            path="/api/quiz",
            methods = [apigatewayv2.HttpMethod.PUT],
            integration=UpdateQuiz_integration,
            #authorizer= authorizer
        )
        http_api.add_routes(
            path="/api/quiz",
            methods = [apigatewayv2.HttpMethod.DELETE],
            integration=RemoveQuiz_integration,
            #authorizer= authorizer
        )
        http_api.add_routes(
            path="/api/quiz/question",
            methods = [apigatewayv2.HttpMethod.POST],
            integration=CreateQuizQuestion_integration,
            #authorizer= authorizer
        )
        http_api.add_routes(
            path="/api/quiz/question",
            methods = [apigatewayv2.HttpMethod.DELETE],
            integration=RemoveQuizQuestion_integration,
            #authorizer= authorizer
        )
        http_api.add_routes(
            path="/api/quiz/question",
            methods = [apigatewayv2.HttpMethod.PUT],
            integration=ModifyQuizQuestion_integration,
            #authorizer= authorizer
        )
        http_api.add_routes(
            path="/api/quiz/submit",
            methods = [apigatewayv2.HttpMethod.POST],
            integration=SubmitQuiz_integration,
            #authorizer= authorizer
        )
        http_api.add_routes(
            path="/api/quiz/question/correct",
            methods = [apigatewayv2.HttpMethod.GET],
            integration=GetQuizQuestionCorrectedCount_integration,
            #authorizer= authorizer
        )
        '''