## Overview
This web application allows users to store their image files securely in a private space. Users must log in with a username and password to access their files. Once logged in, they can upload new image files, view their previously uploaded files, and delete any unwanted files.

## Prerequisites
- Python 3.x
- Flask
- Flask-Login
- Cryptography

## Installation
- Clone the repository to your local machine.
- Navigate to the project directory in the terminal.
- Install the necessary libraries using pip:

```
pip install Flask flask-login cryptography
```

## Run the app

```
# Only localhost
flask run

# Open to the local network
flask run --host=0.0.0.0
```

Access the application in your browser by visiting 
http://localhost:5000/
