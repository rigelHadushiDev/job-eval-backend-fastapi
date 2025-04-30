from pydantic import BaseModel
from typing import List

class StoredJobPosting(BaseModel):
    jobPostingId: str
    jobPostingTitle: str
    jobPostingDesc: str
    requiredEducationLevel: str
    requiredEnglishLevel: str
    requiredExperienceYears: float
    requiredSkills: str
    titleVector: List[float]
    descVector: List[float]