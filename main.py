from fastapi import FastAPI
from api.routes.work_experience_routes import router as work_experience_router
from api.routes.job_posting_routes import router as job_posting_router
from api.routes.job_application_route import router as job_application_router
from core.middleware import JWTAuthenticationMiddleware

app = FastAPI(
    title="CodePioneers Career Portal Microservice",
    description=(
        "This microservice is responsible for computing a candidate’s overall suitability "
        "score by comparing embeddings and applying smart data science algorithms."
    ),
    version="1.0.0",
    contact={
        "name": "Rigel Hadushi",
        "url": "https://github.com/rigelHadushiDev",
        "email": "rigelhadushi4@gmail.com"
    },
    docs_url="/docs",       
    redoc_url="/redoc",  
    openapi_url="/openapi.json"  
)

app.add_middleware(JWTAuthenticationMiddleware)
app.include_router(work_experience_router, tags=["Work Experience"])
app.include_router(job_posting_router, tags=["Job Posting Experience"])
app.include_router(job_application_router, tags=["Job Application Experience"])
