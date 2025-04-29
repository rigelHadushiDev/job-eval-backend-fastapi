from fastapi import APIRouter, HTTPException
from schemas.work_experience import WorkExperience
from services.work_experience_service import WorkExperienceService

router = APIRouter()
service = WorkExperienceService()

@router.post("/work-experience/", tags=["Work Experience"])
async def create_work_experience(payload: WorkExperience):
    try:
        # Call the service method that processes and stores the work experience
        service.process_and_store_work_experience(payload)
        return {"message": "Operation successful"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/getWorkExperience/{work_experience_id}", response_model=None)
async def get_work_experience(work_experience_id: str):
    try:
        work_experience = service.get_work_experience_by_id(work_experience_id)
        return work_experience
    except RuntimeError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/deleteWorkExperience/{work_experience_id}")
async def delete_work_experience(work_experience_id: str):
    try:
        service.delete_work_experience(work_experience_id)
        return {"message": f"Work experience ID {work_experience_id} deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/editWorkExperience/", tags=["Work Experience"])
async def edit_work_experience(payload: WorkExperience):
    try:
        service.edit_work_experience(payload.workExperienceId, payload)
        return {"message": f"Work experience ID {payload.workExperienceId} updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
