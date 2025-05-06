from typing import List
from pydantic import BaseModel

class JobApplicantResponse(BaseModel):
    userId: int
    username: str
    generalScore: float
    educationScore: float
    englishScore: float
    skillsScore: float
    experienceScore: float