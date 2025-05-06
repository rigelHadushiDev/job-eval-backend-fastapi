from fastapi import APIRouter, Depends
from dependencies import get_scoring_service
from schemas.applicant_request import ApplicantRequest
from schemas.generate_score_response import GenerateScoreResponse
from services.scoring_service import ScoringService

router = APIRouter()

@router.post("/job-application/", tags=["Job Posting"], response_model=GenerateScoreResponse)
async def create_job_posting(
    payload: ApplicantRequest,
    scoring_service: ScoringService = Depends(get_scoring_service)
):
    print("Received request payload:", payload.model_dump_json(indent=2))
    result = scoring_service.calculate_final_score(payload)
    print("Response Data:", result.model_dump_json(indent=2))
    return result