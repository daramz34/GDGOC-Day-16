from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt



app = FastAPI()


# my secret key and algorithm for JWT ( configuration)
KEY = "my_secret_key"
ALGORITHM = "HS256"



fake_users_db = {
    "daramz@bowen.edu": "password123"
}

class LoginData(BaseModel):
    email: str
    password: str


# checking the token i guess
security = HTTPBearer(auto_error=False)


def check_vip(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Unauthorized - No token provided")
    try:
        payload = jwt.decode(credentials.credentials, key=KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    




@app.post("/auth/login")
def login(user: LoginData):
    if user.email not in fake_users_db or fake_users_db[user.email] != user.password:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # generating the jwt
    payload = {"sub" : user.email}
    token = jwt.encode(payload, key=KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type" : "bearer"}


@app.get("/protected-data")
def get_secret_data(current_user: dict = Depends(check_vip)):
    return {
        "message" : "Welcome to the VIP area!!",
        "user" : current_user["sub"],
        "secret_data" : "Bowen Challenge day 16 complete bankai"
    }