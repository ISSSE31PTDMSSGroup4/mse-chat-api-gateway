import json
mock_data = {
  "status": "success",
  "message": "Quiz submitted successfully",
  "data": {
    "questions_count": 5,
    "correction_count": 4
  }
}

def lambda_handler(event, context):
    return mock_data