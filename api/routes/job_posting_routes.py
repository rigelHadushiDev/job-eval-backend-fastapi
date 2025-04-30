from fastapi import APIRouter, Depends
from schemas.job_posting import JobPosting
from schemas.job_posting_stored import StoredJobPosting
from schemas.general_response import GeneralResponse
from services.job_posting_service import JobPostingService
from dependencies import get_job_posting_service

router = APIRouter()

@router.post("/job-posting/", tags=["Job Posting"], response_model=StoredJobPosting)
async def create_job_posting(
    payload: JobPosting,
    service: JobPostingService = Depends(get_job_posting_service)
):
    return service.process_and_store_job_posting(payload)

@router.get("/getJobPosting/{job_posting_id}", response_model=None)
async def get_job_posting(
    job_posting_id: str,
    service: JobPostingService = Depends(get_job_posting_service)
):
    return service.get_job_posting_by_id(job_posting_id)

@router.delete("/deleteJobPosting/{job_posting_id}", response_model=GeneralResponse)
async def delete_job_posting(
    job_posting_id: str,
    service: JobPostingService = Depends(get_job_posting_service)
):
    service.delete_job_posting(job_posting_id)
    return GeneralResponse(message="successfullyDeleted")

@router.put("/editJobPosting/", tags=["Job Posting"], response_model=StoredJobPosting)
async def edit_job_posting(
    payload: JobPosting,
    service: JobPostingService = Depends(get_job_posting_service)
):
    return service.edit_job_posting(payload.jobPostingId, payload)
