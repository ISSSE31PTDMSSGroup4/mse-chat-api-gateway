import jwt
import requests
def get_csrf_state(event):
    if 'queryStringParameters' in event:
        if 'state' in event['queryStringParameters']:
            state = event['queryStringParameters']['state']
            return state
    return False

def bad_request(body='Bad Request'):
    return {
          "isBase64Encoded": False,
          "statusCode": 400,
          "body": f"{body}"
     }

def lambda_handler(event, context):
  """Exchange cognito auth code for Cognito tokens"""
  #http://docs.aws.amazon.com/cognito/latest/developerguide/token-endpoint.html
  if not get_csrf_state(event):
    return bad_request(f"Invalid CSRF State \nRequest ID: {event['requestContext']['requestId']}")
  csrf_cookie = [cookie for cookie in event['cookies'] if "csrf_state" in cookie][0] #should always be the first match
  if not'csrf_state='+ str(get_csrf_state(event)) == csrf_cookie:
    return bad_request(f"Mismatched CSRF \nRequest id: {event['requestContext']['requestId']}")
    
  



