API Reference

Getting Started
Installing Dependencies
  Python 3.7
  Follow instructions to install the latest version of python for your platform in the python docs

  Virtual Enviornment
  A virtual environment whenever using Python for projects. Instructions for setting up a virual enviornment for your platform can be found in the python docs

PIP Dependencies
  Once you have your virtual environment setup and running, install dependencies by naviging to the /backend directory and running:
    pip install -r requirements.txt
  This will install all of the required packages we selected within the requirements.txt file.

Database Setup
  With Postgres running, restore a database using the trivia.psql file. From the backend folder in terminal run:
    psql trivia < trivia.psql

Starting the server
  navigate to the backend folder and execute the following commands:
    export FLASK_APP=flaskr
    export FLASK_ENV=development
    flask run

Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
Authentication: This version of the application does not require authentication or API keys.

Error Handling
Errors are returned as JSON objects in the following format:

{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
The API will return four error types when requests fail:

400: bad request
404: resource not found
422: unprocessable
405: wrong method
500: internal server error


GET /categories
General:
    Returns a list of categories and success value.
Sample: curl http://127.0.0.1:5000/categories
  {
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
   
GET /questions
General:
    Returns a list of questions, success value, number of questions, list of categories, and current category.
    Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
Sample: curl http://127.0.0.1:5000/questions?page=1
  {
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": 1, 
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
      "question": "Which Dutch graphic artist-initials M C was a creator of optical illusions?"
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
    }, 
    {
      "answer": "In the kitchen", 
      "category": 5, 
      "difficulty": 1, 
      "id": 25, 
      "question": "Where is my dog?"
    }
  ], 
  "success": true, 
  "total_questions": 44
}


GET /categories/<int:cat_id>/questions
General: 
    Returns questions by category, current category, success value and number of questions in category.
Sample: curl http://127.0.0.1:5000/categories/4/questions
{
  "current_category": 4, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }, 
    {
      "answer": "Miami, FL", 
      "category": 4, 
      "difficulty": 5, 
      "id": 31, 
      "question": "Where was Edison born?"
    }
  ], 
  "success": true, 
  "total_questions": 5
}    


Testing
To run the tests, run

dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py