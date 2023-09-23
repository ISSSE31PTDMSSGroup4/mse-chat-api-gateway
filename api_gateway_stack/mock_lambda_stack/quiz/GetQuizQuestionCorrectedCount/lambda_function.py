import json
mock_data = {
  "id": 1,
  "title": "MyQuiz 1",
  "question_list": [
    {
      "id": 1,
      "corrected_counter": 10
    },
    {
      "id": 2,
      "corrected_counter": 4
    },
    {
      "id": 3,
      "corrected_counter": 6
    },
    {
      "id": 4,
      "corrected_counter": 2
    },
    {
      "id": 5,
      "corrected_counter": 5
    }
  ],
  "remark": "my first quiz"
}

def lambda_handler(event, context):
    return mock_data