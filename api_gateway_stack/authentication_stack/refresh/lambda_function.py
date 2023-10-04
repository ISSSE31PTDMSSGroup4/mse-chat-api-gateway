import jwt
from jwt.exceptions import DecodeError,InvalidSignatureError,ExpiredSignatureError,InvalidIssuerError,InvalidIssuedAtError,ImmatureSignatureError,InvalidKeyError,InvalidAlgorithmError, MissingRequiredClaimError
import datetime
import uuid
import boto3
import os
import re

ssm = boto3.client('ssm')

PRIVATE_KEY_PEM = ssm.get_parameter(Name=f"{os.environ.get('APP_PRIVATE_KEY_SSM_PARAM_ARN')}")['Parameter']['Value']
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

def unauthorized(error_body):
    return {
          "isBase64Encoded": False,
          "statusCode": 400,
          "body": f"{error_body}"
     }

def internal_error(error_body):
        return {
          "isBase64Encoded": False,
          "statusCode": 500,
          "body": f"{error_body}"
     }


def decode_token(access_token):
    token =jwt.decode(str(access_token),key=PUBLIC_KEY_PEM,algorithms=['RS256'],issuer=os.environ.get('APP_URL'),options={"require": ["exp", "iss", "sub"]})
    return token

def create_access_token(sub, expiry = 1800, csrf=str(uuid.uuid4())):
  payload = {
    'jti':str(uuid.uuid4()),
    'exp':datetime.datetime.now() + datetime.timedelta(seconds=expiry),
    'iat':datetime.datetime.now(),
    'nbf':datetime.datetime.now(),
    'iss':os.environ.get('APP_URL'),
    'sub':sub,
    'csrf':csrf
  }
  encoded = jwt.encode(payload,PRIVATE_KEY_PEM,algorithm="RS256")
  return encoded

def lambda_handler(event, context):

    if not user_logged_in(event):
        return unauthorized(f"Missing Access Token \nRequest id: {event['requestContext']['requestId']}")
    
    access_token_string = [cookie for cookie in event['cookies'] if "access_token_cookie" in cookie][0]
    access_token = re.findall('(?<=access_token_cookie=).*',access_token_string)[0] #cookie is access_token_cookie=xxxx, need to strip the front part

    try:
       user = decode_token(access_token)['sub']
    except InvalidSignatureError:
        return unauthorized(f"Invalid Token Signature \n Request id: {event['requestContext']['requestId']}")
    except ExpiredSignatureError:
        return unauthorized(f"Expired Token Signature \n Request id: {event['requestContext']['requestId']}")
    except InvalidIssuerError:
        return unauthorized(f"Invalid Token issuer \n Request id: {event['requestContext']['requestId']}")
    except InvalidIssuedAtError:
        return unauthorized(f"Token is issued in the future \n Request id: {event['requestContext']['requestId']}")
    except ImmatureSignatureError:
        return unauthorized(f"Token is valid in the future \n Request id: {event['requestContext']['requestId']}")
    except MissingRequiredClaimError:
        return unauthorized(f"Token does not have required claims \n Request id: {event['requestContext']['requestId']}")
    except InvalidKeyError:
        return internal_error(f"Key format invalid \n Request id: {event['requestContext']['requestId']}")
    except InvalidAlgorithmError:
        return internal_error(f"Key algorithm invalid \n Request id: {event['requestContext']['requestId']}")
    except DecodeError as e:
        print(str(e))
        return internal_error(f"Unable to decode token \n Request id: {event['requestContext']['requestId']}")

    
    csrf = str(uuid.uuid4())
    access_token = create_access_token(user,expiry=int(os.environ.get('ACCESS_TOKEN_EXPIRY')), csrf = csrf)
    cookie_objects = [f'access_token_cookie={access_token}; SameSite=Strict; Path=/; Secure; HttpOnly',f'csrf={csrf}; Path=/;','logged_in=true; Path=/;',f"access_token_expires={int(datetime.datetime.timestamp(datetime.datetime.now() + datetime.timedelta(seconds=int(os.environ.get('ACCESS_TOKEN_EXPIRY')))))}; Path=/;"]

    return { 
      "cookies" : cookie_objects,
      "isBase64Encoded": False,
      "statusCode": 200,
      "headers": "",
      "body": "Token Refresh Successful"
  }