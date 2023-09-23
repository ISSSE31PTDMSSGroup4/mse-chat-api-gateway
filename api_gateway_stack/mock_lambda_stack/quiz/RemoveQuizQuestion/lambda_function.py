import json
mock_data = {
  "code": 200,
  "status": "success",
  "message": "Resource removed successfully"
}

def lambda_handler(event, context):
    return mock_data