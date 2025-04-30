from pydantic import BaseModel

class GeneralResponse(BaseModel):
    message: str