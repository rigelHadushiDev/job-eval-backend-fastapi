from pydantic import BaseModel

class WorkExperience(BaseModel):
    workExperienceId: str
    userId: int
    workExperienceTitle: str
    workExperienceDescription: str
    totalYears: float