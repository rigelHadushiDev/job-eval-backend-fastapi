import jwt
from fastapi import HTTPException
from typing import Optional
from dotenv import load_dotenv
import os
import base64

load_dotenv()
JWT_SECRET_KEY =os.getenv("JWT_SECRET_KEY")

def verify_jwt_token(token: str) -> Optional[dict]:
    print(f"Verifying JWT token...Token: {token}")
    print(f"Verifying Secret: {JWT_SECRET_KEY}")
    try:
        decoded_secret = base64.urlsafe_b64decode(JWT_SECRET_KEY)
        decoded_token = jwt.decode(token, decoded_secret, algorithms=["HS256"])
        print(f"Decoded JWT payload: {decoded_token}")
        return decoded_token  # Return decoded payload if valid
    except jwt.ExpiredSignatureError:
        print("JWT token has expired.")
        raise HTTPException(status_code=401, detail="JWT token has expired")
    except jwt.InvalidTokenError:
        print("JWT token is invalid.")
        raise HTTPException(status_code=401, detail="Invalid JWT token")