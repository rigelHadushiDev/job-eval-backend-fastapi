from schemas.job_posting import JobPosting
from schemas.job_posting_stored import StoredJobPosting
from utils.text_preprocessing import clean_text, get_embeddings
from fastapi import HTTPException, status

class JobPostingService:
    def __init__(self, model, desc_collection, title_collection):
        self.model = model
        self.desc_collection = desc_collection
        self.title_collection = title_collection

    def process_and_store_job_posting(self, job_posting: JobPosting):
        cleaned_title = clean_text(job_posting.jobPostingTitle)
        cleaned_description = clean_text(job_posting.jobPostingDesc)
        title_vector, desc_vector = get_embeddings(self.model, [cleaned_title], [cleaned_description])
        return self.store_in_db(job_posting, title_vector[0].tolist(), desc_vector[0].tolist())

    def store_in_db(self, job_posting: JobPosting, title_vector: list, desc_vector: list) -> StoredJobPosting:
        self.title_collection.add(
            job_posting_id=job_posting.jobPostingId,
            job_title=job_posting.jobPostingTitle,
            required_english_level=job_posting.requiredEnglishLevel,
            required_experience_years=job_posting.requiredExperienceYears,
            required_skills=job_posting.requiredSkills,
            title_vector=title_vector
        )
        self.desc_collection.add(
            job_posting_id=job_posting.jobPostingId,
            job_description=job_posting.jobPostingDesc,
            required_english_level=job_posting.requiredEnglishLevel,
            required_experience_years=job_posting.requiredExperienceYears,
            required_skills=job_posting.requiredSkills,
            desc_vector=desc_vector
        )
        return StoredJobPosting(
            jobPostingId=job_posting.jobPostingId,
            jobPostingTitle=job_posting.jobPostingTitle,
            jobPostingDesc=job_posting.jobPostingDesc,
            requiredEnglishLevel=job_posting.requiredEnglishLevel,
            requiredExperienceYears=job_posting.requiredExperienceYears,
            requiredSkills=job_posting.requiredSkills,
            titleVector=title_vector,   
            descVector=desc_vector
        )

    def delete_job_posting(self, job_posting_id: str):
        self.get_job_posting_by_id(job_posting_id)
        self.title_collection.delete(job_posting_id)
        self.desc_collection.delete(job_posting_id)

    def get_job_posting_by_id(self, job_posting_id: str):
        desc_result = self.desc_collection.get(
            ids=[job_posting_id],
            include=["metadatas", "embeddings", "documents"]
        )

        if not desc_result or not desc_result.get("ids"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No job posting found for ID: {job_posting_id}"
            )

        metadata = desc_result["metadatas"][0]
        embedding = desc_result["embeddings"][0]

        return {
            "job_posting_id": job_posting_id,
            "job_description": desc_result["documents"][0],
            "required_english_level": metadata.get("required_english_level"),
            "required_experience_years": metadata.get("required_experience_years"),
            "required_skills": metadata.get("required_skills"),
            "desc_embedding": embedding
        }

    def edit_job_posting(self, job_posting_id: str, job_posting: JobPosting) -> StoredJobPosting:

        self.get_job_posting_by_id(job_posting_id)

        cleaned_title = clean_text(job_posting.jobPostingTitle)
        cleaned_description = clean_text(job_posting.jobPostingDesc)
        title_vector, desc_vector = get_embeddings(self.model, [cleaned_title], [cleaned_description])
        title_vector_list = title_vector[0].tolist()
        desc_vector_list = desc_vector[0].tolist()

        self.title_collection.update(
            job_posting_id=job_posting_id,
            job_title=job_posting.jobPostingTitle,
            required_english_level=job_posting.requiredEnglishLevel,
            required_experience_years=job_posting.requiredExperienceYears,
            required_skills=job_posting.requiredSkills,
            title_vector=title_vector_list
        )
        self.desc_collection.update(
            job_posting_id=job_posting_id,
            job_description=job_posting.jobPostingDesc,
            required_english_level=job_posting.requiredEnglishLevel,
            required_experience_years=job_posting.requiredExperienceYears,
            required_skills=job_posting.requiredSkills,
            desc_vector=desc_vector_list
        )

        return StoredJobPosting(
            jobPostingId=job_posting.jobPostingId,
            jobPostingTitle=job_posting.jobPostingTitle,
            jobPostingDesc=job_posting.jobPostingDesc,
            requiredEnglishLevel=job_posting.requiredEnglishLevel,
            requiredExperienceYears=job_posting.requiredExperienceYears,
            requiredSkills=job_posting.requiredSkills,
            titleVector=title_vector_list, 
            descVector=desc_vector_list      
        )
