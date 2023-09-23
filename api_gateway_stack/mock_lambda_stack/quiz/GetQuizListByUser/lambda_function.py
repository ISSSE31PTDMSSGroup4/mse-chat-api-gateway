import json
mock_data = [
  {
    "id": 1,
    "title": "MyQuiz 1",
    "question_list": [
      {
        "id": 1
      },
      {
        "id": 2
      },
      {
        "id": 3
      },
      {
        "id": 4
      },
      {
        "id": 5
      }
    ],
    "remark": "my first quiz"
  },
  {
    "id": 2,
    "title": "MyQuiz 2",
    "question_list": [
      {
        "id": 6
      },
      {
        "id": 7
      },
      {
        "id": 8
      }
    ],
    "remark": "my second quiz"
  },
  {
    "id": 3,
    "title": "Fast Quiz",
    "question_list": [
      {
        "id": 9
      },
      {
        "id": 10
      }
    ],
    "remark": "It is very short quiz just contains 2 questions"
  }
]

def lambda_handler(event, context):
    return mock_data