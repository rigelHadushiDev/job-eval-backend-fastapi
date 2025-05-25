from pydantic import BaseModel, Field
from typing import List

class StoredWorkExperience(BaseModel):
    work_experience_id: str = Field(
        ..., 
        description="Unique identifier for the stored work experience entry."
    )
    user_id: int = Field(
        ..., 
        description="ID of the user who owns this work experience."
    )
    work_experience_title: str = Field(
        ..., 
        description="Title of the role or position held (e.g., 'Backend Developer')."
    )
    work_experience_desc: str = Field(
        ..., 
        description="Detailed description of responsibilities and achievements in the role."
    )
    total_years: float = Field(
        ..., 
        description="Total number of years the user spent in this role."
    )
    title_vector: List[float] = Field(
        ..., 
        description="Semantic embedding vector generated from the job title."
    )
    desc_vector: List[float] = Field(
        ..., 
        description="Semantic embedding vector generated from the job description."
    )
