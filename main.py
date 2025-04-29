from fastapi import FastAPI
from api.routes.work_experience_routes import router as work_experience_router




app = FastAPI(
    title="Job Application Evaluation - FastAPI BE with ChromaDB",
    version="1.0.0"
)


app.include_router(work_experience_router, tags=["Work Experience"])
