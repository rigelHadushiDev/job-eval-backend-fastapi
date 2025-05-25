from pydantic import BaseModel, Field

class JobPosting(BaseModel):
    jobPostingId: str = Field(
        ..., 
        description="Unique identifier for the job posting (e.g., UUID)."
    )
    jobPostingTitle: str = Field(
        ..., 
        description="Title of the job position (e.g., 'Software Engineer')."
    )
    jobPostingDesc: str = Field(
        ..., 
        description="Detailed description of the job role and responsibilities."
    )
    requiredEnglishLevel: str = Field(
        ..., 
        description="Minimum English proficiency required (e.g., 'Intermediate', 'Advanced')."
    )
    requiredExperienceYears: int = Field(
        ..., 
        description="Minimum number of years of relevant experience required for the role."
    )
    requiredSkills: str = Field(
        ..., 
        description="Comma-separated list of required skills (e.g., 'Python, Docker, SQL')."
    )
