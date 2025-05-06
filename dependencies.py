from sentence_transformers import SentenceTransformer
from data.collections.work_experience_desc_collection import WorkExperienceDescCollection
from data.collections.work_experience_title_collection import WorkExperienceTitleCollection
from services.scoring_service import ScoringService
from services.work_experience_service import WorkExperienceService
from data.collections.job_posting_desc_collection import JobPostingDescCollection
from data.collections.job_posting_title_collection import JobPostingTitleCollection
from services.job_posting_service import JobPostingService

def get_work_experience_service():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    desc = WorkExperienceDescCollection()
    title = WorkExperienceTitleCollection()
    return WorkExperienceService(model, desc, title)

def get_job_posting_service():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    desc = JobPostingDescCollection()
    title = JobPostingTitleCollection()
    return JobPostingService(model, desc, title)

def get_scoring_service():
    job_desc = JobPostingDescCollection()
    job_title = JobPostingTitleCollection()
    work_desc = WorkExperienceDescCollection()
    work_title = WorkExperienceTitleCollection()
    return ScoringService(job_desc, job_title, work_desc, work_title)
