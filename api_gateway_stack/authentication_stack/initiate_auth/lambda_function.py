import json
import os
from urllib.parse import urlparse

def is_safe_url(url):
  if urlparse(url).netloc!= '':
    return False
  else: return True

def user_logged_in(event):
  if 'cookies' in event:
    access_token_cookie = [cookie for cookie in event['cookies'] if "access_token_cookie" in cookie]
  else:
    return False
  if access_token_cookie == []:
    return False
  else:
    return True

def random_hex_bytes(n_bytes):
  """Create a hex encoded string of random bytes"""
  return os.urandom(n_bytes).hex()

def cognito_location(csrf_state):
  return  f"{os.environ.get('AWS_COGNITO_DOMAIN')}/login?response_type=code&client_id={os.environ.get('COGNITO_USER_POOL_CLIENT_ID')}&state={csrf_state}&redirect_uri={os.environ.get('APP_REDIRECT_URL')}" 

def lambda_handler(event, context):
    if user_logged_in(event):
      return {
          "isBase64Encoded": False,
          "statusCode": 302,
          "headers": {
               "Location": "/"
          },
          "body": ""
      }
    print(str(event))
    cookie = {}
    csrf_state = random_hex_bytes(8)
    #create a csrf state to prevent csrf login
    cookie['csrf_state'] = csrf_state
    if 'queryStringParameters' in event:
        if 'next' in event['queryStringParameters']:
          next_page = event['queryStringParameters']['next']
          if next_page and is_safe_url(next_page): 
            cookie['next']=next_page
    return {
           "cookies" : [f"{key}={cookie[key]}; SameSite=lax; Path=/; Secure;" for key in cookie.keys()],
          "isBase64Encoded": False,
          "statusCode": 302,
          "headers": {
               "Location": f"{cognito_location(csrf_state)}"
          },
          "body": ""
     }