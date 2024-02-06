from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI, Request, TemplateResponse
from jinja2 import Environment, PackageLoader
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.hash import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
import random

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # one week in minutes


# Set up database connection
DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Define User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    hashed_password = Column(String)
    key = Column(String)

# Set up password hashing and JWT authentication
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"

def verify_password(plain_password, hashed_password):
    return bcrypt.verify(plain_password, hashed_password)

def get_password_hash(password):
    return bcrypt.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Define FastAPI app and routes
app = FastAPI()

env = Environment(loader=PackageLoader("myapp", "templates"))

@app.get("/", response_class=TemplateResponse)
async def index(request: Request):
    return {"request": request}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login(username: str, password: str):
    session = SessionLocal()
    user = session.query(User).filter(User.username == username).first()
    session.close()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def get_key():
    return generate_key()

@app.post("/user/add")
async def add_user(username: str, password: str, key: str = Depends(get_key)):
    session = SessionLocal()
    hashed_password = get_password_hash(password)
    new_user = User(username=username, hashed_password=hashed_password, key=key)
    session.add(new_user)
    session.commit()
    session.close()
    return {"message": f"User {username} added to the authorized users list"}


# Define generate_key function
def generate_key(length=10):
    """Generate a random key of given length"""
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+[]{}|;,.<>?/~'
    return ''.join(random.choice(chars) for _ in range(length))

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
