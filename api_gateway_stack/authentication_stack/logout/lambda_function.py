import os

def cognito_location():
  return  f"{os.environ.get('AWS_COGNITO_DOMAIN')}/logout?response_type=code&client_id={os.environ.get('COGNITO_USER_POOL_CLIENT_ID')}&logout_uri={os.environ.get('APP_URL')}"

def lambda_handler(event, context):
        return {
           "cookies" : ['access_token_cookie=deleted; Path=/; Max-Age=0;','csrf=deleted; Path=/; Max-Age=0;','logged_in=deleted; Path=/; Max-Age=0;', 'access_token_expires=deleted; Path=/; Max-Age=0;', 'debug_user=deleted; Path=/; Max-Age=0;'],
          "isBase64Encoded": False,
          "statusCode": 302,
          "headers": {
               "Location": f"{cognito_location()}"
          },
          "body": ""
     }