import json
mock_data = {
  "id": 1,
  "title": "MyQuiz 1",
  "questions": [
    {
      "id": 1,
      "title": "What is the largest city in the United States by population?",
      "index": 1,
      "options": [
        "New York",
        "Los Angeles",
        "Chicago",
        "Houston"
      ],
      "answer": "New York",
      "explanation": "New York is the largest city in the United States by population."
    },
    {
      "id": 2,
      "title": "What is the capital of the United Kingdom?",
      "index": 2,
      "options": [
        "Paris",
        "London",
        "Tokyo",
        "Sydney"
      ],
      "answer": "London",
      "explanation": "London is the capital of the United Kingdom."
    },
    {
      "id": 3,
      "title": "Which programming language is known for its simplicity and readability?",
      "index": 3,
      "options": [
        "Python",
        "Java",
        "C++",
        "Ruby"
      ],
      "answer": "Python",
      "explanation": "Python is known for its simplicity and readability."
    },
    {
      "id": 4,
      "title": "What is the highest mountain in the world?",
      "index": 4,
      "options": [
        "Mount Everest",
        "K2",
        "Matterhorn",
        "Kilimanjaro"
      ],
      "answer": "Mount Everest",
      "explanation": "Mount Everest is the highest mountain in the world, located in the Himalayas."
    },
    {
      "id": 5,
      "title": "Which planet is the largest in our solar system?",
      "index": 5,
      "options": [
        "Mercury",
        "Venus",
        "Mars",
        "Jupiter"
      ],
      "answer": "Jupiter",
      "explanation": "Jupiter is the largest planet in our solar system."
    }
  ],
  "remark": "my first quiz"
}

def lambda_handler(event, context):
    return mock_data