# FastAPI Bookstore

This is a FastAPI application for managing a bookstore. It includes user registration, login, and CRUD operations for books.

## Features

- User registration and login with JWT authentication
- Create, read, and delete books
- Secure endpoints with JWT tokens

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/amaan-igs/FastAPI.git
    cd FastAPI-Bookstore
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```sh
    psql -U postgres -f SQL/setup.sql
    ```

5. Run the application:
    ```sh
    uvicorn main:app --reload
    ```

## Endpoints

- `POST /register`: Register a new user
- `POST /login`: Login and get a JWT token
- `GET /books`: Get a list of books
- `POST /books`: Create a new book (requires authentication)
- `DELETE /books/{book_id}`: Delete a book (requires authentication)

## Environment Variables

Create a `.env` file in the root directory and add the following:
```
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```