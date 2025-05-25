from pydantic import BaseModel, Field

class GeneralResponse(BaseModel):
    message: str = Field(
        ..., 
        description="Response message indicating the outcome (e.g., 'successfullyDeleted')."
    )