# services/work_experience_service.py

from schemas.work_experience_stored import StoredWorkExperience
from schemas.work_experience import WorkExperience
from utils.text_preprocessing import clean_text, get_embeddings

class WorkExperienceService:
    def __init__(self, model, desc_collection, title_collection):
        self.model = model
        self.desc_collection = desc_collection
        self.title_collection = title_collection

    def process_and_store_work_experience(self, work_exp: WorkExperience):
        cleaned_title = clean_text(work_exp.workExperienceTitle)
        cleaned_description = clean_text(work_exp.workExperienceDescription)
        title_vector, desc_vector = get_embeddings(self.model, [cleaned_title], [cleaned_description])
        return self.store_in_db(work_exp, title_vector[0].tolist(), desc_vector[0].tolist())

    def store_in_db(self, work_exp: WorkExperience, title_vector: list, desc_vector: list) -> StoredWorkExperience:
        self.title_collection.add(
            work_experience_id=work_exp.workExperienceId,
            user_id=work_exp.userId,
            work_experience_title=work_exp.workExperienceTitle,
            total_years=work_exp.totalYears,
            title_vector=title_vector
        )
        self.desc_collection.add(
            work_experience_id=work_exp.workExperienceId,
            user_id=work_exp.userId,
            work_experience_desc=work_exp.workExperienceDescription,
            total_years=work_exp.totalYears,
            desc_vector=desc_vector
        )

        return StoredWorkExperience(
            work_experience_id=work_exp.workExperienceId,
            user_id=work_exp.userId,
            work_experience_title=work_exp.workExperienceTitle,
            work_experience_desc=work_exp.workExperienceDescription,
            total_years=work_exp.totalYears,
            title_vector=title_vector,
            desc_vector=desc_vector
        )

    def delete_work_experience(self, work_experience_id: str):
        self.title_collection.delete(work_experience_id)
        self.desc_collection.delete(work_experience_id)

    def get_work_experience_by_id(self, work_experience_id: str):
        desc_result = self.desc_collection.get(ids=[work_experience_id], include=["metadatas", "embeddings", "documents"])

        if not desc_result or not desc_result.get("ids"):
            raise RuntimeError(f"No work experience found for ID: {work_experience_id}")

        metadata = desc_result["metadatas"][0]
        embedding = desc_result["embeddings"][0]
        document = desc_result["documents"][0]  # ← Get the actual description here

        return {
            "work_experience_id": work_experience_id,
            "user_id": metadata.get("user_id"),
            "work_experience_desc": document,
            "total_years": metadata.get("total_years"),
            "embeddings": embedding
        }


    def edit_work_experience(self, work_experience_id: str, work_exp: WorkExperience) -> StoredWorkExperience:
        cleaned_title = clean_text(work_exp.workExperienceTitle)
        cleaned_description = clean_text(work_exp.workExperienceDescription)
        title_vector, desc_vector = get_embeddings(self.model, [cleaned_title], [cleaned_description])
        title_vector_list = title_vector[0].tolist()
        desc_vector_list = desc_vector[0].tolist()

        self.title_collection.update(
            work_experience_id=work_experience_id,
            user_id=work_exp.userId,
            work_experience_title=work_exp.workExperienceTitle,
            total_years=work_exp.totalYears,
            title_vector=title_vector_list
        )
        self.desc_collection.update(
            work_experience_id=work_experience_id,
            user_id=work_exp.userId,
            work_experience_desc=work_exp.workExperienceDescription,
            total_years=work_exp.totalYears,
            desc_vector=desc_vector_list
        )

        return StoredWorkExperience(
            work_experience_id=work_exp.workExperienceId,
            user_id=work_exp.userId,
            work_experience_title=work_exp.workExperienceTitle,
            work_experience_desc=work_exp.workExperienceDescription,
            total_years=work_exp.totalYears,
            title_vector=title_vector_list,
            desc_vector=desc_vector_list
        )
