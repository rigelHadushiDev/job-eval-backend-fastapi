from fastapi import APIRouter, Depends
from schemas.general_response import GeneralResponse
from schemas.work_experience import WorkExperience
from schemas.work_experience_stored import StoredWorkExperience
from services.work_experience_service import WorkExperienceService
from dependencies import get_work_experience_service

router = APIRouter()

@router.post(
    "/work-experience/",
    tags=["Work Experience"],
    summary="Create work experience entry",
    description="Processes and stores a candidate's work experience, generating embeddings for semantic comparison.",
    response_model=StoredWorkExperience
)
async def create_work_experience(
    payload: WorkExperience,
    service: WorkExperienceService = Depends(get_work_experience_service)
):
    return service.process_and_store_work_experience(payload)


@router.get(
    "/getWorkExperience/{work_experience_id}",
    tags=["Work Experience"],
    summary="Get work experience by ID",
    description="Retrieves a stored work experience entry by its unique identifier.",
    response_model=StoredWorkExperience  # You had 'None', which disables docs—this is better
)
async def get_work_experience(
    work_experience_id: str,
    service: WorkExperienceService = Depends(get_work_experience_service)
):
    return service.get_work_experience_by_id(work_experience_id)


@router.delete(
    "/deleteWorkExperience/{work_experience_id}",
    tags=["Work Experience"],
    summary="Delete work experience",
    description="Deletes a work experience record and its associated vector from ChromaDB.",
    response_model=GeneralResponse
)
async def delete_work_experience(
    work_experience_id: str,
    service: WorkExperienceService = Depends(get_work_experience_service)
):
    service.delete_work_experience(work_experience_id)
    return GeneralResponse(message="successfullyDeleted")


@router.put(
    "/editWorkExperience/",
    tags=["Work Experience"],
    summary="Edit work experience entry",
    description="Edits an existing work experience record, updates its embedding, and saves it to ChromaDB.",
    response_model=StoredWorkExperience
)
async def edit_work_experience(
    payload: WorkExperience,
    service: WorkExperienceService = Depends(get_work_experience_service)
):
    return service.edit_work_experience(payload.workExperienceId, payload)
