from typing import List, Optional
from pydantic import BaseModel

class EducationLevelEntry(BaseModel):
    educationLevel: Optional[str] = None 

class SkillEntry(BaseModel):
    skillName: str
    skillProficiency: int

class ApplicantRequest(BaseModel):
    userId: int
    username: str
    educationLevel: Optional[List[EducationLevelEntry]] = None  
    englishLevel: Optional[str] = None  
    skills: Optional[List[SkillEntry]] = None 
    jobPostingId: int