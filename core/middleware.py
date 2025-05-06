from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from .security import verify_jwt_token

class JWTAuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization token is missing")
        
        token = auth_header[7:] 
        verify_jwt_token(token)

        response = await call_next(request)
        return response