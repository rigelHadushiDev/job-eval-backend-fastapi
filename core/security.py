import jwt
from fastapi import HTTPException
from typing import Optional
from dotenv import load_dotenv
import os
import base64

load_dotenv()
JWT_SECRET_KEY =os.getenv("JWT_SECRET_KEY")

def verify_jwt_token(token: str) -> Optional[dict]:
    try:
        decoded_secret = base64.urlsafe_b64decode(JWT_SECRET_KEY)
        decoded_token = jwt.decode(token, decoded_secret, algorithms=["HS256"])
        return decoded_token  
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="JWT token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid JWT token")