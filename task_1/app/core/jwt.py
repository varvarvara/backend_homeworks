from fastapi import FastAPI, Depends, HTTPException, Header, status
from typing import Optional
from sqlalchemy.orm import Session
from app.core.db import SessionLocal, engine, get_db #Base - а зачем это?
from app.models.users import User
from app.core.security import create_access_token, hash_password, verify_password, decode_access_token
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.users import UserRegister, UserLogin
from app.core import security

app = FastAPI()

@app.post("/signup")
def signup(user: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing: 
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = hash_password(user.password)
    new_user=User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"username": new_user.username, "id": new_user.id}

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer", "user": db_user}

@app.route("/protected")
def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=status.HTTP_403_UNAUTHORIZED, detail="Creds missing")
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalidor expired token")
    
    return {"message": "Protected route accessed", "user": payload["sub"]}