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
   SQLite database using a simplified interface is provided

Starting the server
  navigate to the src folder in the backend folder and execute the following commands:
    export FLASK_APP=api.py
    export FLASK_ENV=development
    flask run

Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
Authentication: This application requires authentication through Auth0. Auth0 inforation is as follows:

    url: 'woohoo'  (the auth0 domain prefix)
    audience: 'https://drinks' (the audience set for the auth0 app)
    clientId: 'qut7t8xRf2blYUoONRE5ellrVRdPN8A1' (the client id generated for the auth0 app)
    callbackURL: 'http://localhost:8100' (the base url of the running ionic application)
 
 Starting the frontend
    navigate to the frontend folder and execute the following command:
    ionic serve

Error Handling
Errors are returned as JSON objects in the following format:

{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
The API will return four error types when requests fail:

400: bad request
401: invalid authorization (AuthError)
404: resource not found
422: unprocessable
405: wrong method
500: internal server error


