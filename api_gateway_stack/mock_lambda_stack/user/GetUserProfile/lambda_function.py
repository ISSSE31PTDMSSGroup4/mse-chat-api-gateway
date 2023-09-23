import json
mock_data = {
  "id": 0,
  "name": "Mock account",
  "avartar": "https://mdbcdn.b-cdn.net/img/new/avatars/2.webp",
  "email": "mockaccount@gmail.com",
  "about": "This is the test profile content \n This is second line content \n This is third line content"
}

def lambda_handler(event, context):
    return mock_data