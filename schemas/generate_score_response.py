from pydantic import BaseModel

class GenerateScoreResponse(BaseModel):
    experience_similarity_score: float
    experience_years_score: float
    education_score: float
    english_score: float
    skill_score: float
    final_score: float