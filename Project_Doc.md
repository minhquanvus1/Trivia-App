# Trivia App

This is the fantastic app that you can have a wonderful time here. You can play the quiz game, add your own questions, delete questions, search questions and so on.

All the backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Getting Started

### Pre-requisite and Local Development

- Developers should already have Python 3, pip and node installed on their local machines.
- For database, we use PostgreSQL. You can download it from [here](https://www.postgresql.org/download/).

#### Backend

To follow the best practice when working on a Python project, we will create a virtual environment for our project. This will keep your dependencies for this project separate from other projects.

- **Start Virtual Environment**

```bash
# Windows users
cd backend
python -m venv venv
env\Scripts\activate
```

- **Install Dependencies**

```bash
pip install -r requirements.txt
```

- **Set up Database for local development**

```bash
# Windows users
cd backend
psql -U postgres -h localhost
DROP DATABASE IF EXISTS trivia;
CREATE DATABASE trivia;
\c trivia
\i trivia.psql // to populate the **development database**
\q
```

- **Run the development server**

```bash
# Windows Powershell users:
cd backend

$env:FLASK_APP = "flaskr"
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = $true
flask run
```

The backend Flask application will run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.

#### Frontend

The frontend folder contains a complete React frontend to consume the data from the Flask server.

- To run the React frontend application, do the folllowings:

- **Install Node Dependencies**

```bash
cd frontend
npm install // only once to install dependencies
```

- **Run the React app**

```bash
npm start
```

The frontend React application will run on `http://127.0.0.1:3000/`

### Tests

- For Unit Test, we create a test database `trivia_test` to run Test against it.<br>
- To create the test database, run the following commands from the backend folder:

```bash
cd backend

# start the psql terminal
psql -U postgres -h localhost

# drop the database if it exists
DROP DATABASE IF EXISTS trivia_test;

# create the database
CREATE DATABASE trivia_test;

\c trivia_test

# create the tables and populate the **testing database**
\i trivia.psql

\q
```

- To run all Unit Tests for the backend, run the following commands from the backend folder:

```bash

cd backend
python -m test_flaskr
Or: python test_flaskr.py
```

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Introduction:

- These APIs is for the Trivia application. We can use these APIs to create, update, delete and get the Questions, Categories from the database.

### Getting Started:

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1/5000/, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling:

// TODO: add ERROR HANDLING in this section

- Errors are returns in JSON format as follows:

```
{
    "success": False,
    "error": 404,
    "message": "Resource Not Found"
}
```

There are three types of errors:

- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed

### Endpoints:

// TODO: add ENDPOINTS in this section
GET '/categories'

- General: get all the Categories, with their id, and the total number of categories returned.\
- Request Arguments: None
- Returns: An object with keys include:
  - categories: that contains an object of id: category_string (key:value pairs).
  - success: boolean value (True)
  - total_categories: total number of categories returned
- Sample Request: `curl -X GET http://127.0.0.1:5000/categories`
- Sample Response

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```

GET '/questions'
Or: GET '/questions?page={Integer}'

- General: get the list of all questions, with their id, and the total number of categories returned.\
- Request Arguments: ?page={Integer} (optional, default = 1)
- Returns: An object with keys include:

  - success: boolean value (True)
  - questions: that contains a list of questions.
  - total_questions: total number of questions returned
  - categories: that contains an object of id: category_string (key:value pairs).
  - current_category: None

- Sample Request 1: `curl -X GET http://127.0.0.1:5000/questions`
- Sample Response 1

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

- Sample Request 2: `curl -X GET http://127.0.0.1:5000/questions?page=2`
- Sample Response 2

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

## Deployment:

- Currently, this app is not deployed yet. But we can deploy it on Heroku or AWS Elastic Beanstalk.

## Authors:

Quan Tran

## Acknowledgements:

- Thanks to the fantastic team at Udacity for the wonderful course
