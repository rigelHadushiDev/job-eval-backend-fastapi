from pydantic import BaseModel, Field
from typing import List

class StoredJobPosting(BaseModel):
    jobPostingId: str = Field(
        ..., 
        description="Unique identifier for the stored job posting (e.g., UUID)."
    )
    jobPostingTitle: str = Field(
        ..., 
        description="Title of the job position (e.g., 'Backend Developer')."
    )
    jobPostingDesc: str = Field(
        ..., 
        description="Detailed description of the job role and responsibilities."
    )
    requiredEnglishLevel: str = Field(
        ..., 
        description="Minimum English proficiency required (e.g., 'A1', 'A2')."
    )
    requiredExperienceYears: float = Field(
        ..., 
        description="Required years of experience for the role."
    )
    requiredSkills: str = Field(
        ..., 
        description="Comma-separated list of required skills (e.g., 'Python, FastAPI, Docker')."
    )
    titleVector: List[float] = Field(
        ..., 
        description="Vector embedding of the job title generated using Sentence Transformers."
    )
    descVector: List[float] = Field(
        ..., 
        description="Vector embedding of the job description generated using Sentence Transformers."
    )
