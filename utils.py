from fastapi import HTTPException
from passlib.context import CryptContext
import jwt
import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Password Hashing
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# JWT Token Creation
SECRET_KEY = "secret"

def create_jwt_token(data: dict):
    expiration = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
    data.update({"exp": expiration})
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Not authenticated")
