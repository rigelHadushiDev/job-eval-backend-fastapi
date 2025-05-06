from typing import List
from pydantic import BaseModel

class EducationLevelEntry(BaseModel):
    educationLevel: str

class SkillEntry(BaseModel):
    skillName: str
    skillProficiency: int

class ApplicantRequest(BaseModel):
    userId: int
    username: str
    educationLevel: List[EducationLevelEntry]
    englishLevel: str
    skills: List[SkillEntry]
    jobPostingId: int