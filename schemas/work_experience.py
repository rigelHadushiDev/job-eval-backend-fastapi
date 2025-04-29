from pydantic import BaseModel
from typing import List

class WorkExperience(BaseModel):
    workExperienceId: str
    userId: int
    workExperienceTitle: str
    workExperienceDescription: str
    totalYears: float
