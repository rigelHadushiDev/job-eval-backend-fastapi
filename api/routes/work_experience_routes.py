from fastapi import APIRouter, Depends
from schemas.general_response import GeneralResponse
from schemas.work_experience import WorkExperience
from schemas.work_experience_stored import StoredWorkExperience
from services.work_experience_service import WorkExperienceService
from dependencies import get_work_experience_service

router = APIRouter()

@router.post("/work-experience/", tags=["Work Experience"], response_model=StoredWorkExperience)
async def create_work_experience(
    payload: WorkExperience,
    service: WorkExperienceService = Depends(get_work_experience_service)
):
    return service.process_and_store_work_experience(payload)

@router.get("/getWorkExperience/{work_experience_id}", response_model=None)
async def get_work_experience(
    work_experience_id: str,
    service: WorkExperienceService = Depends(get_work_experience_service)
):
    return service.get_work_experience_by_id(work_experience_id)

@router.delete("/deleteWorkExperience/{work_experience_id}", response_model=GeneralResponse)
async def delete_work_experience(
    work_experience_id: str,
    service: WorkExperienceService = Depends(get_work_experience_service)
):
    service.delete_work_experience(work_experience_id)
    return GeneralResponse(message="successfullyDeleted")

@router.put("/editWorkExperience/", tags=["Work Experience"], response_model=StoredWorkExperience)
async def edit_work_experience(
    payload: WorkExperience,
    service: WorkExperienceService = Depends(get_work_experience_service)
):
    return service.edit_work_experience(payload.workExperienceId, payload)