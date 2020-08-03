a7e5aaf7fa15647b5b2e0f65e14b641b-1494542659.us-west-2.elb.amazonaws.com

# Casting Agency Project 

## Content 
1.Motivation
2.Installing Dependencies
3.Running server locally
4.Application Endpoints
5.Authentication
6.Testing
7.Running server on Heroku

## Motivation

This is the fifth and final project of the Full Stack developer Nanodegree. It covers the following technical topics:

Database modeling with postgres & sqlalchemy
API to performance CRUD Operations on database with Flask
Automated testing with Unittest
Authorization & Role based Authentification with Auth0
Deployment on Heroku


The project resembles a casting agency which is responsible for creating movies, managing and assigning actors to these movies.
Within the agency there are three roles: executive producer, casting director and casting assistant.


## Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running server locally

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Application Endpoints

```

Endpoints

GET '/actors'
GET '/movies'
POST '/actors'
POST '/movies'
PATCH '/actors/<int:id>'
PATCH '/movies/<int:id>'
DELETE '/actors/<int:id>'
DELETE '/movies/<int:id>'



GET '/actors'
- Fetches a list of actors
- Request Arguments: None
- Returns: An object with a success key and a list of actors. 
{
    'success': True,
    'actors': [{
                'id': 1,
                'name': Tom Hanks,
                'age': 60,
               },
	       {
                'id': 2,
                'name': Anne Hathaway,
                'age': 35,
              }]
}

GET '/movies'
- Fetches a list of movies
- Request Arguments: None
- Returns: An object with a success key and a list of movies.
{
    'success': True,
    'movies': [{
                'id': 1,
                'title': Inception,
                'release_date': 2010-4-20,
               },
	       {
                'id': 1,
                'title': The terminal,
                'release_date': 2006-4-20,
               }]
}


POST '/actors'
- adds an actor to the database
- Request Arguments: name and age
- Returns: An object with a success key and a list which contains the new actor object.
{
    'success': True,
    'actors': [{
                'id': 1,
                'name': Tom Hanks,
                'age': 60,
               }]
}

POST '/movies'
- adds a movie to the database
- Request Arguments: title and release date
- Returns: An object with a success key and a list which contains the new movie object.
{
    'success': True,
    'movies': [{
                'id': 1,
                'title': Inception,
                'release_date': 2010-4-20,
               }]
}



DELETE '/actors/<int:id>'
- Deletes the actor with id: id
- Request Arguments: None
- Returns: A dictionary with multiple keys which are the id of the deleted actor and success key
{
  "delete": 2, 
  "success": true
}

DELETE '/movies/<int:id>'
- Deletes the movie with id: id
- Request Arguments: None
- Returns: A dictionary with multiple keys which are the id of the deleted movie and success key
{
  "delete": 1, 
  "success": true
}

PATCH '/actors/<int:id>'
- updates the actor with id: id
- Request Arguments: name or age or both
- Returns: An object with a success key and a list which contains the updated actor object.
{
    'success': True,
    'actors': [{
                'id': 1,
                'name': Tom Hanks,
                'age': 60,
               }]
}

PATCH '/movies/<int:id>'
- updates the movie with id: id
- Request Arguments: title or release date or both
- Returns: An object with a success key and a list which contains the updated movie object.
{
    'success': True,
    'movies': [{
                'id': 1,
                'title': Inception,
                'release_date': 2010-4-20,
               }]
}

```

## Authentication

#### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, regular web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:actors`
    - `post:actors`
    - `patch:actors`
    - `delete:actors`
    - `get:movies`
    - `post:movies`
    - `patch:movies`
    - `delete:movies`
6. Create new roles for:
    - Casting Assistant
        - can `get:actors` and `get:movies`
    - Casting Director
        - can perform all actions except `post:movies` and `delete:movies`
    - Executive Producer
	- can perform all actions


## Testing
To run the tests, run
```
createdb agency_test
python test_app.py
```

## Running server on Heroku


