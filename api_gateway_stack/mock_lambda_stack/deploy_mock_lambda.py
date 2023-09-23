import aws_cdk as cdk
import os
from constructs import Construct

class MockLambdaStack(cdk.Stack):
     def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self.lambda_dict = {}
        ### User Profile
        Get_User_Profile_lambda = cdk.aws_lambda.Function(
        self,
        'GetUserProfileLambda',
        runtime=cdk.aws_lambda.Runtime.PYTHON_3_8,
        handler='lambda_function.lambda_handler',
        code=cdk.aws_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), 'user','GetUserProfile')), 
        timeout=cdk.Duration.seconds(10),
        )

        self.lambda_dict["Get_User_Profile"]=Get_User_Profile_lambda
        ###
        ##Create Quiz
        Create_Quiz_lambda = cdk.aws_lambda.Function(
        self,
        'CreateQuizLambda',
        runtime=cdk.aws_lambda.Runtime.PYTHON_3_8,
        handler='lambda_function.lambda_handler',
        code=cdk.aws_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), 'quiz','CreateQuiz')), 
        timeout=cdk.Duration.seconds(10),
        )

        self.lambda_dict["Create_Quiz"]=Create_Quiz_lambda
        ####        
        ##Create Quiz Question
        Create_Quiz_Question_lambda = cdk.aws_lambda.Function(
        self,
        'CreateQuizQuestionLambda',
        runtime=cdk.aws_lambda.Runtime.PYTHON_3_8,
        handler='lambda_function.lambda_handler',
        code=cdk.aws_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), 'quiz','CreateQuizQuestion')), 
        timeout=cdk.Duration.seconds(10),
        )

        self.lambda_dict["Create_Quiz_Question"]=Create_Quiz_Question_lambda
        ####    
        ##Get Quiz Detail
        Get_Quiz_Detail_lambda = cdk.aws_lambda.Function(
        self,
        'GetQuizDetail',
        runtime=cdk.aws_lambda.Runtime.PYTHON_3_8,
        handler='lambda_function.lambda_handler',
        code=cdk.aws_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), 'quiz','GetQuizDetail')), 
        timeout=cdk.Duration.seconds(10),
        )

        self.lambda_dict["Get_Quiz_Detail"]=Get_Quiz_Detail_lambda
        ####   
        ##Get Quiz List By User
        Get_Quiz_List_By_User_lambda = cdk.aws_lambda.Function(
        self,
        'GetQuizListByUser',
        runtime=cdk.aws_lambda.Runtime.PYTHON_3_8,
        handler='lambda_function.lambda_handler',
        code=cdk.aws_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), 'quiz','GetQuizListByUser')), 
        timeout=cdk.Duration.seconds(10),
        )

        self.lambda_dict["Get_Quiz_List_By_User"]=Get_Quiz_List_By_User_lambda
        ####    
        ##Get Quiz Question Corrected Count
        Get_Quiz_Question_Corrected_Count_lambda = cdk.aws_lambda.Function(
        self,
        'GetQuizQuestionCorrectedCount',
        runtime=cdk.aws_lambda.Runtime.PYTHON_3_8,
        handler='lambda_function.lambda_handler',
        code=cdk.aws_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), 'quiz','GetQuizQuestionCorrectedCount')), 
        timeout=cdk.Duration.seconds(10),
        )

        self.lambda_dict["Get_Quiz_Question_Corrected_Count"]=Get_Quiz_Question_Corrected_Count_lambda
        ####
        ##Modify Quiz Question
        Modify_Quiz_Question_lambda = cdk.aws_lambda.Function(
        self,
        'ModifyQuizQuestion',
        runtime=cdk.aws_lambda.Runtime.PYTHON_3_8,
        handler='lambda_function.lambda_handler',
        code=cdk.aws_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), 'quiz','ModifyQuizQuestion')), 
        timeout=cdk.Duration.seconds(10),
        )

        self.lambda_dict["Modify_Quiz_Question"]=Modify_Quiz_Question_lambda
        ####
        ##Remove Quiz
        Remove_Quiz_lambda = cdk.aws_lambda.Function(
        self,
        'RemoveQuiz',
        runtime=cdk.aws_lambda.Runtime.PYTHON_3_8,
        handler='lambda_function.lambda_handler',
        code=cdk.aws_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), 'quiz','RemoveQuiz')), 
        timeout=cdk.Duration.seconds(10),
        )

        self.lambda_dict["Remove_Quiz"]=Remove_Quiz_lambda
        ####
        ##Remove Quiz Question
        Remove_Quiz_Question_lambda = cdk.aws_lambda.Function(
        self,
        'RemoveQuizQuestion',
        runtime=cdk.aws_lambda.Runtime.PYTHON_3_8,
        handler='lambda_function.lambda_handler',
        code=cdk.aws_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), 'quiz','RemoveQuizQuestion')), 
        timeout=cdk.Duration.seconds(10),
        )

        self.lambda_dict["Remove_Quiz_Question"]=Remove_Quiz_Question_lambda
        ####
        ##Submit Quiz
        Submit_Quiz_lambda = cdk.aws_lambda.Function(
        self,
        'SubmitQuiz',
        runtime=cdk.aws_lambda.Runtime.PYTHON_3_8,
        handler='lambda_function.lambda_handler',
        code=cdk.aws_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), 'quiz','SubmitQuiz')), 
        timeout=cdk.Duration.seconds(10),
        )

        self.lambda_dict["Submit_Quiz"]=Submit_Quiz_lambda
        ####
        ##Update Quiz
        Update_Quiz_lambda = cdk.aws_lambda.Function(
        self,
        'UpdateQuiz',
        runtime=cdk.aws_lambda.Runtime.PYTHON_3_8,
        handler='lambda_function.lambda_handler',
        code=cdk.aws_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), 'quiz','UpdateQuiz')), 
        timeout=cdk.Duration.seconds(10),
        )

        self.lambda_dict["Update_Quiz"]=Update_Quiz_lambda
        #### 

app = cdk.App()
MockLambdaStack(app, "MockLambdaStack")
app.synth()