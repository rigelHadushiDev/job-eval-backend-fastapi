from fastapi import APIRouter, Depends
from schemas.job_posting import JobPosting
from schemas.job_posting_stored import StoredJobPosting
from schemas.general_response import GeneralResponse
from services.job_posting_service import JobPostingService
from dependencies import get_job_posting_service

router = APIRouter()

@router.post(
    "/job-posting/",
    tags=["Job Posting"],
    summary="Create a new job posting",
    description="Accepts job posting details, processes embeddings, and stores it in the ChromaDB vector database.",
    response_model=StoredJobPosting
)
async def create_job_posting(
    payload: JobPosting,
    service: JobPostingService = Depends(get_job_posting_service)
):
    return service.process_and_store_job_posting(payload)


@router.get(
    "/getJobPosting/{job_posting_id}",
    tags=["Job Posting"],
    summary="Get a job posting by ID",
    description="Fetches a job posting and its stored embeddings using its unique identifier.",
    response_model=StoredJobPosting  
)
async def get_job_posting(
    job_posting_id: str,
    service: JobPostingService = Depends(get_job_posting_service)
):
    return service.get_job_posting_by_id(job_posting_id)


@router.delete(
    "/deleteJobPosting/{job_posting_id}",
    tags=["Job Posting"],
    summary="Delete a job posting",
    description="Deletes a job posting and its corresponding vectors from ChromaDB.",
    response_model=GeneralResponse
)
async def delete_job_posting(
    job_posting_id: str,
    service: JobPostingService = Depends(get_job_posting_service)
):
    service.delete_job_posting(job_posting_id)
    return GeneralResponse(message="successfullyDeleted")


@router.put(
    "/editJobPosting/",
    tags=["Job Posting"],
    summary="Edit an existing job posting",
    description="Edits an existing job posting, updates its embeddings, and saves changes to ChromaDB.",
    response_model=StoredJobPosting
)
async def edit_job_posting(
    payload: JobPosting,
    service: JobPostingService = Depends(get_job_posting_service)
):
    return service.edit_job_posting(payload.jobPostingId, payload)
