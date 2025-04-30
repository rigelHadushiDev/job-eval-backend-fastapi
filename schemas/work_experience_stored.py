from pydantic import BaseModel
from typing import List

class StoredWorkExperience(BaseModel):
    work_experience_id: str
    user_id: int
    work_experience_title: str
    work_experience_desc: str
    total_years: float
    title_vector: List[float]
    desc_vector: List[float]
