# Trivia App

This is the fantastic app that you can have a wonderful time here. You can play the quiz game, add your own questions, delete questions, search questions and so on.

All the backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Getting Started

### Pre-requisite and Local Development

- Developers should already have Python 3, pip and node installed on their local machines.
- For database, we use PostgreSQL. You can download it from [here](https://www.postgresql.org/download/).

#### Backend

To follow the best practice when working on a Python project, we will create a virtual environment for our project. This will keep your dependencies for this project separate from other projects.

- ** Start Virtual Environment**

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

### Endpoints:

// TODO: add ENDPOINTS in this section

## Deployment:

- Currently, this app is not deployed yet. But we can deploy it on Heroku or AWS Elastic Beanstalk.

## Authors:

Quan Tran

## Acknowledgements:

- Thanks to the fantastic team at Udacity for the wonderful course
