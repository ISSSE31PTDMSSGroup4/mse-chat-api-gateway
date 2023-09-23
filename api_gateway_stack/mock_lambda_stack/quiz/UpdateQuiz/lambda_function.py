import json
mock_data = {
  "code": 200,
  "status": "success",
  "message": "Resource updated successfully"
}

def lambda_handler(event, context):
    return mock_data