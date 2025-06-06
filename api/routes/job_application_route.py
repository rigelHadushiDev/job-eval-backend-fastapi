from fastapi import APIRouter, Depends
from dependencies import get_scoring_service
from schemas.applicant_request import ApplicantRequest
from schemas.generate_score_response import GenerateScoreResponse
from services.scoring_service import ScoringService

router = APIRouter()

@router.post(
    "/job-application/",
    tags=["Job Application Scoring"],
    summary="Calculate Candidate Suitability Score",
    description="""
Calculates a candidate's suitability score for a job posting based on work experience similarity, years of experience, education, skills, and English proficiency.
""",
    response_model=GenerateScoreResponse
)
async def calculate_score(
    payload: ApplicantRequest,
    scoring_service: ScoringService = Depends(get_scoring_service)
):
    result = scoring_service.calculate_final_score(payload)
    return result