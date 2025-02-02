from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import psycopg2
from psycopg2.extras import RealDictCursor
import jwt
from models import User, Book
from utils import hash_password, verify_password, create_jwt_token, decode_jwt
from database import get_db

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- User Registration ---
@app.post("/register")
def register(user: User, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (user.username,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user.password)
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                   (user.username, user.email, hashed_password))
    db.commit()
    return {"message": "User registered successfully"}

# --- User Login ---
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    
    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE username = %s", (form_data.username,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify password
    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate JWT token
    token = create_jwt_token({"sub": user["username"]})
    
    return {"access_token": token, "token_type": "bearer"}

# --- Get Books ---
@app.get("/books")
def get_books(db=Depends(get_db)):
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    return {"books": books}

# --- Create Book (Protected) ---
@app.post("/books")
def create_book(book: Book, token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    try:
        print(f"Token received: {token}")  # Debug: print the token
        
        user_data = decode_jwt(token)  # Decode the JWT token
        print(f"Decoded user data: {user_data}")  # Debug: print decoded data
        
        username = user_data.get("sub")

        if not username:
            raise HTTPException(status_code=403, detail="User not found")

        # Insert book into the database
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO books (title, author, genre, price, user_id) VALUES (%s, %s, %s, %s, %s)",
            (book.title, book.author, book.genre, book.price, username),
        )
        db.commit()

        return {"message": "Book added successfully"}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# --- Delete Book (Protected) ---
@app.delete("/books/{book_id}")
def delete_book(book_id: int, token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    # Use the utility function to decode the JWT token
    user_data = decode_jwt(token)
    username = user_data.get("sub")

    if not username:
        raise HTTPException(status_code=403, detail="User not found")

    cursor = db.cursor()
    cursor.execute("DELETE FROM books WHERE id = %s AND user_id = %s", (book_id, username))
    db.commit()

    return {"message": "Book deleted successfully"}

