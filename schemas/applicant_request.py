from typing import List, Optional
from pydantic import BaseModel, Field

class EducationLevelEntry(BaseModel):
    educationLevel: Optional[str] = Field(
        default=None,
        description="Candidate's education level (e.g., 'BACHELOR', 'MASTER', 'PHD')."
    )

class SkillEntry(BaseModel):
    skillName: str = Field(
        ...,
        description="Name of the skill (e.g., 'Python', 'Project Management')."
    )
    skillProficiency: int = Field(
        ...,
        description="Proficiency level from 1 (lowest) to 5 (highest)."
    )

class ApplicantRequest(BaseModel):
    userId: int = Field(
        ..., 
        description="Unique ID of the candidate."
    )
    username: str = Field(
        ..., 
        description="Username or identifier of the candidate."
    )
    educationLevel: Optional[List[EducationLevelEntry]] = Field(
        default=None,
        description="List of education entries (degrees or levels achieved)."
    )
    englishLevel: Optional[str] = Field(
        default=None,
        description="English proficiency level (e.g., 'A1', 'A2', 'C1')."
    )
    skills: Optional[List[SkillEntry]] = Field(
        default=None,
        description="List of skills with corresponding proficiency levels."
    )
    jobPostingId: int = Field(
        ..., 
        description="ID of the job posting the candidate is applying for."
    )
