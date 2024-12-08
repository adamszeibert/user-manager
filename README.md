# User Management REST API

This is a simple user management REST API built with Flask and SQLite. It supports basic operations like creating a user, retrieving a user, updating a user, deleting a user, and logging in.

The application uses SQLite in memory database which means all data is lost when the application stops thus this application is for demonstration purposes only, it is not meant to be used in production. 

## Requirements

- Python 3.6+
- Flask
- Werkzeug
- pytest
- pytest-flask

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/adamszeibert/user-manager.git
    cd user-manager
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the Flask application:
    ```sh
    python app.py
    ```

2. The application will be running at `http://127.0.0.1:5000`.

## API Endpoints

### Create a User

- **URL:** `/users`
- **Method:** `POST`
- **Request JSON:**
    ```json
    {
        "name": "Teszt Elek",
        "email": "teszt.elek@gmail.com",
        "password": "Password1"
    }
    ```
- **Response JSON:**
    ```json
    {
        "id": 1,
        "name": "Teszt Elek",
        "email": "teszt.elek@gmail.com",
        "password": "<hashed_password>"
    }
    ```

### Retrieve a User

- **URL:** `/users/<email>`
- **Method:** `GET`
- **Response JSON:**
    ```json
    {
        "id": 1,
        "name": "Teszt Elek",
        "email": "teszt.elek@gmail.com",
        "password": "<hashed_password>"
    }
    ```

### Update a User

- **URL:** `/users/<email>`
- **Method:** `PUT`
- **Request JSON:**
    ```json
    {
        "name": "Teszt Elek Updated",
        "email": "teszt.elek@gmail.com",
        "password": "newpassword"
    }
    ```
- **Response JSON:**
    ```json
    {
        "id": 1,
        "name": "Teszt Elek Updated",
        "email": "teszt.elek@gmail.com",
        "password": "<hashed_password>"
    }
    ```

### Delete a User

- **URL:** `/users/<email>`
- **Method:** `DELETE`
- **Response:** `204 No Content`

### Login

- **URL:** `/login`
- **Method:** `POST`
- **Request JSON:**
    ```json
    {
        "email": "teszt.elek@gmail.com",
        "password": "Password1"
    }
    ```
- **Response JSON:**
    ```json
    {
        "message": "Login successful",
        "user": {
            "id": 1,
            "name": "Teszt Elek",
            "email": "teszt.elek@gmail.com",
            "password": "<hashed_password>"
        }
    }
    ```

## Running Tests

1. Install the test dependencies:
    ```sh
    pip install pytest pytest-flask
    ```

2. Run the tests:
    ```sh
    pytest
    ```

## Architectural Analysis

As mentioned above, this application is a very simple implementation of a user management REST API. 

### Persistent Database

In order to make this application production ready the in-memory database must be replaced with a persistent database. PostgreSQL or MySQL are great choices.

Migration scripts should be moved to seperate SQL files.

### Connection Pool

A production application should use a fairly large connection pool to manage database connections. The easiest way to add a connection pool to a Flask application is using the `Flask-SQLAlchemy` module.

SQLAlchemy also allows us to easily use entity models making our code cleaner and easier to read.

### Authorization

The `login` endpoint should return a JWT token which should be used to authorize the user when calling the `get_user` endpoint. Each user should be able to retrieve only their own user information, trying to retrieve other users' information should result in HTTP 403. 

### Horizontal Scaling - Worker Processes

While Flask is a great tool to create REST API backends, its performance has limitations as the Flask development server is not optimized for production use.

The easiest way to boost its performance is running the application with multiple worker processes. This can be easily done with `gunicorn` for example:

```sh
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Gunicorn allows multiple requests to be processed by using multiple worker processes while balancing incoming requests across worker processes. It can replace unresponsive workers, making the application fault tolerant, ensuring high availability. Horizontal scaling can be achieved by increasing the number of worker processes.

### Caching

While the size of user data isn't large and complex enough to justify caching but if retreiving user information was slow, adding caching to the `get_user` endpoint could solve the issue. This can be done with the `Flask-Caching` module by adding `@cache.cached(timeout=60)` decorator to `get_user`.

### Gzip Compression

Compressing responses can drastically reduce load times as much less data is transferred between the server and the client. Enabling gzip compression can be done with the `Flask-Compress` module.