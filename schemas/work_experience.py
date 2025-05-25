from pydantic import BaseModel, Field

class WorkExperience(BaseModel):
    workExperienceId: str = Field(
        ..., 
        description="Unique identifier for the work experience entry (e.g., UUID)."
    )
    userId: int = Field(
        ..., 
        description="ID of the user who owns this work experience."
    )
    workExperienceTitle: str = Field(
        ..., 
        description="Title of the job role held (e.g., 'Software Engineer')."
    )
    workExperienceDescription: str = Field(
        ..., 
        description="Detailed description of the role, responsibilities, and achievements."
    )
    totalYears: float = Field(
        ..., 
        description="Total number of years of experience in this role."
    )
