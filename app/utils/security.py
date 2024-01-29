from fastapi import HTTPException, status
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

# Configuration for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuration for JWT
SECRET_KEY = "Addy-codes"  # Use a strong secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # or any duration you prefer

class TokenData:
    username: Optional[str] = None

def verify_password(plain_password, hashed_password):
    """Verify a hashed password against a non-hashed one."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Hash a password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    """Decode and verify a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data
