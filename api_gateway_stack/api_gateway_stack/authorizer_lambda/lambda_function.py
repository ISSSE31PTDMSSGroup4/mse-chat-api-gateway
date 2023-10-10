import jwt
import boto3
import os
import re

ssm = boto3.client('ssm')
PUBLIC_KEY_PEM = ssm.get_parameter(Name=f"{os.environ.get('APP_PUBLIC_KEY_SSM_PARAM_ARN')}")['Parameter']['Value']

def user_logged_in(event):
  if 'cookies' in event:
    access_token_cookie = [cookie for cookie in event['cookies'] if "access_token_cookie" in cookie]
  else:
    return False
  if access_token_cookie == []:
    return False
  else:
    return True

def decode_token(access_token):
    token =jwt.decode(str(access_token),key=PUBLIC_KEY_PEM,algorithms=['RS256'],issuer=os.environ.get('APP_URL'),options={"require": ["exp", "iss", "sub"]})
    return token

def unauthorized(event_id,error):
    return {
        "isAuthorized": False,
        "context":{
            "event_id": error_body,
            "error":error
        }
    }
def lambda_handler(event, context):
    if not user_logged_in(event):
        return unauthorized(event['requestContext']['requestId'],"Missing access token")
    
    access_token_string = [cookie for cookie in event['cookies'] if "access_token_cookie" in cookie][0]
    access_token = re.findall('(?<=access_token_cookie=).*',access_token_string)[0] #cookie is access_token_cookie=xxxx, need to strip the front part

    try:
       user = decode_token(access_token)['sub']
    except:
        return unauthorized(event['requestContext']['requestId'],"Invalid token")

    #return success
    return{
        "isAuthorized": True,
        "context":{
            "user": user
        }
    }
