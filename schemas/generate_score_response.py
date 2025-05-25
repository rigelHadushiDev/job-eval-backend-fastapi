from pydantic import BaseModel, Field

class GenerateScoreResponse(BaseModel):
    experience_similarity_score: float = Field(
        ..., 
        description="Semantic similarity score between candidate's work experience and job posting (0 to 100)."
    )
    experience_years_score: float = Field(
        ..., 
        description="Score based on years of experience compared to the job's requirement (0 to 100)."
    )
    education_score: float = Field(
        ..., 
        description="Score based on the highest level of education attained (0 to 100)."
    )
    english_score: float = Field(
        ..., 
        description="Score based on the candidate's English proficiency level (0 to 100)."
    )
    skill_score: float = Field(
        ..., 
        description="Score based on the relevance and proficiency of matched skills (0 to 100)."
    )
    final_score: float = Field(
        ..., 
        description="Overall weighted suitability score (0 to 100)."
    )