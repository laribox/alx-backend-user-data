# User Authentication Service

## Project Overview

This project provides a user authentication service implemented using Python, Flask, SQLAlchemy, and bcrypt. It includes features like user registration, password hashing, and user session management. The service interacts with a SQLite database for user data storage.

## Features

1. **User Model**: A SQLAlchemy model for managing user data in a database.
2. **Database Operations**: Functions for adding, updating, and querying users in the database.
3. **Password Hashing**: Secure password storage using bcrypt.
4. **User Registration**: A method to register new users while checking for duplicates.
5. **Flask Application**: A basic Flask app that serves endpoints for user-related operations.

## Requirements

- Python 3.7
- Ubuntu 18.04 LTS
- SQLAlchemy 1.3.x
- Pycodestyle 2.5
- Flask
- bcrypt

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/alx-backend-user-data.git
    cd alx-backend-user-data/0x03-user_authentication_service
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Install `bcrypt`:
    ```bash
    pip install bcrypt
    ```

## Usage

### Running the Application
1. Start the Flask server:
    ```bash
    python app.py
    ```
2. Access the application on `http://localhost:5000`.

### Running Tests
- You can test individual features by running the corresponding Python files provided in the `main.py` examples.

## Files and Directories

- **`user.py`**: Contains the SQLAlchemy model for the `User` table.
- **`db.py`**: Provides methods for database operations, such as adding and querying users.
- **`auth.py`**: Includes authentication logic such as password hashing and user registration.
- **`app.py`**: A Flask app serving a basic route.
- **`README.md`**: Documentation for the project.
- **`requirements.txt`**: List of Python dependencies.

## Code Style

The project follows the `pycodestyle` (version 2.5) guidelines. Ensure your code complies by running:
```bash
pycodestyle <filename>

