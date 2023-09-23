import json
mock_data = {
  "code": 200,
  "status": "success",
  "message": "Resource created successfully"
}
def lambda_handler(event, context):
    return mock_data