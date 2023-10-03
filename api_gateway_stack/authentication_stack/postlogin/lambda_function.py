from jose import jwt as josejwt
import jwt
import requests
import os
import boto3
from urllib.parse import urlparse
from Crypto.PublicKey import RSA
import uuid
import datetime
import re
ssm = boto3.client('ssm')


PRIVATE_KEY_PEM = ssm.get_parameter(Name=f"{os.environ.get('APP_PRIVATE_KEY_SSM_PARAM_ARN')}")['Parameter']['Value']

##decrypt private key
#APP_PRIVATE_KEY = RSA.import_key(PRIVATE_KEY_PEM)

COGNITO_JWKS_URL = (
  f"https://cognito-idp.{os.environ.get('AWS_REGION')}.amazonaws.com/{os.environ.get('AWS_COGNITO_USER_POOL_ID')}/.well-known/jwks.json"
)

def get_query_param_csrf_state(event):
    if 'queryStringParameters' in event:
        if 'state' in event['queryStringParameters']:
            state = event['queryStringParameters']['state']
            return state
    return False

def get_next_from_cookie(event):
  if 'cookies' in event:
    next_cookie = [cookie for cookie in event['cookies'] if "next" in cookie]
  if next_cookie == []:
    return False
  next_str = next_cookie[0]
  next_url = re.findall('(?<=next=).*',next_str)[0] #cookieval is next=/xyz, need regex to extract
  if is_safe_url(str(next_url)):
    return next_url

  
def is_safe_url(url):
  if urlparse(url).netloc!= '':
    return False
  else: return True 

def get_code(event):
    if 'queryStringParameters' in event:
        if 'code' in event['queryStringParameters']:
            auth_code = event['queryStringParameters']['code']
            return auth_code
    return False
  
def bad_request(body='Bad Request', status_code = 400):
    return {
          "isBase64Encoded": False,
          "statusCode": status_code,
          "body": f"{body}"
     }

def verify(COGNITO_JWKS,token, access_token=None):
  """Verify a cognito JWT"""
  # get the key id from the header, locate it in the cognito keys
  # and verify the key
  header = josejwt.get_unverified_header(token)
  key = [k for k in COGNITO_JWKS if k["kid"] == header['kid']][0]
  verified_token = josejwt.decode(token,
                        key,
                        audience=os.environ.get('COGNITO_USER_POOL_CLIENT_ID'),
                        access_token=access_token)
  return verified_token

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
  """Exchange cognito auth code for Cognito tokens"""
  #http://docs.aws.amazon.com/cognito/latest/developerguide/token-endpoint.html
  ##check CSRF state
  if not get_query_param_csrf_state(event):
    return bad_request(f"Invalid CSRF State \nRequest ID: {event['requestContext']['requestId']}")
  csrf_cookie = [cookie for cookie in event['cookies'] if "csrf_state" in cookie][0] #should always be the first match
  if not'csrf_state='+ str(get_query_param_csrf_state(event)) == csrf_cookie:
    return bad_request(f"Mismatched CSRF \nRequest id: {event['requestContext']['requestId']}")

  #auth code handling
  if not get_code(event):
    return bad_request(f"Invalid Redirect \nRequest ID: {event['requestContext']['requestId']}")
  auth_code = get_code(event)
  request_parameters = {
    'grant_type': 'authorization_code',
    'client_id': os.environ.get('COGNITO_USER_POOL_CLIENT_ID'),
    'code': auth_code,
    "redirect_uri": os.environ.get('APP_REDIRECT_URL')
  }

  #use auth code to exchange for token
  response = requests.post("%s/oauth2/token" % os.environ.get('AWS_COGNITO_DOMAIN'),
                           data=request_parameters)
  if not response.status_code == requests.codes.ok:
    return bad_request(f"Incorrect Authentication Configuration \nRequest ID: {event['requestContext']['requestId']}",500)
  
  ##get cognito well-known keys
  
  COGNITO_JWKS = requests.get(COGNITO_JWKS_URL).json()["keys"]

  ##verify jwt token from cognito
  try:
    verify(COGNITO_JWKS, response.json()["access_token"])
  except Exception as e:
    return bad_request(f"Unable to validate access token \nRequest ID: {event['requestContext']['requestId']}",500)

  #retrieve id token
  try:
    id_token = verify(COGNITO_JWKS, response.json()["id_token"],
                    response.json()["access_token"])
  except Exception as e:
    return bad_request(f"Unable to validate id token \nRequest ID: {event['requestContext']['requestId']}",500)

  #get next param
  if get_next_from_cookie(event):
    next_url = get_next_from_cookie(event)
    if next_url[0]!='/': #no slash, add a slash
      next_url = '/'+next_url
  else:
    next_url = '/'
  
  #construct access token
  #first, get a csrf value that will be written in another cookie
  csrf = str(uuid.uuid4())
  #create access token
  access_token = create_access_token(sub = id_token['email'], expiry = int(os.environ.get('ACCESS_TOKEN_EXPIRY')), csrf = csrf)

  #construct response object
  cookie_objects = [f'access_token_cookie={access_token}; SameSite=Strict; Path=/; Secure; HttpOnly',f'csrf={csrf}; Path=/;','csrf_state=deleted; Path=/; Max-Age=0;','next=deleted; Path=/; Max-Age=0;','logged_in=true; Path=/;',f"access_token_expires={int(datetime.datetime.timestamp(datetime.datetime.now() + datetime.timedelta(seconds=int(os.environ.get('ACCESS_TOKEN_EXPIRY')))))}; Path=/;"]

  #return to origin or next
  return { 
      "cookies" : cookie_objects,
      "isBase64Encoded": False,
      "statusCode": 302,
      "headers": {
            "Location": f"{next_url}"
      },
      "body": ""
  }

  
  
  



