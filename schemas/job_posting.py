from pydantic import BaseModel
from typing import List

class JobPosting(BaseModel):
    jobPostingId: str
    jobPostingTitle: str
    jobPostingDesc: str
    requiredEnglishLevel: str
    requiredExperienceYears: int
    requiredSkills: str
