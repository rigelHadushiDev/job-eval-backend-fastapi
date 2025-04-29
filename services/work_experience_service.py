from utils.text_preprocessing import clean_text, get_embeddings
from db.collections.work_experience_desc_collection import WorkExperienceDescCollection
from db.collections.work_experience_title_collection import WorkExperienceTitleCollection
from schemas.work_experience import WorkExperience
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

desc_collection = WorkExperienceDescCollection()
title_collection = WorkExperienceTitleCollection()

class WorkExperienceService:
    def __init__(self):
        self.model = model
        self.desc_collection = desc_collection
        self.title_collection = title_collection

    def process_and_store_work_experience(self, work_exp: WorkExperience):
        print(f"Processing work experience for user: {work_exp.userId}, title: {work_exp.workExperienceTitle}")

        cleaned_title = clean_text(work_exp.workExperienceTitle)
        cleaned_description = clean_text(work_exp.workExperienceDescription)

        print(f"Cleaned title: {cleaned_title}")
        print(f"Cleaned description: {cleaned_description}")

        try:
            title_vector, desc_vector = get_embeddings(self.model, [cleaned_title], [cleaned_description])

            print(f"Generated title vector: {title_vector}")
            print(f"Generated description vector: {desc_vector}")
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            raise

        self.store_in_db(work_exp, title_vector[0], desc_vector[0])

    def store_in_db(self, work_exp: WorkExperience, title_vector: list, desc_vector: list):
        try:
            self.title_collection.add(
                work_experience_id=work_exp.workExperienceId,
                user_id=work_exp.userId,
                work_experience_title=work_exp.workExperienceTitle,
                total_years=work_exp.totalYears,
                title_vector=title_vector
            )

            print(f"Title vector stored for work experience ID: {work_exp.workExperienceId}")

            self.desc_collection.add(
                work_experience_id=work_exp.workExperienceId,
                user_id=work_exp.userId,
                work_experience_desc=work_exp.workExperienceDescription,
                total_years=work_exp.totalYears,
                desc_vector=desc_vector
            )

            print(f"Description vector stored for work experience ID: {work_exp.workExperienceId}")

        except Exception as e:
            print(f"Error storing work experience in DB: {e}")

    
    def delete_work_experience(self, work_experience_id: str):
        try:
            print(f"Deleting work experience ID: {work_experience_id}")
            self.title_collection.delete(work_experience_id)
            self.desc_collection.delete(work_experience_id)
            print(f"Work experience ID {work_experience_id} deleted successfully.")
        except Exception as e:
            print(f"Error deleting work experience: {e}")
            raise

    def get_work_experience_by_id(self, work_experience_id: str):
        try:
            print(f"Fetching work experience ID: {work_experience_id}")
            desc_result = self.desc_collection.get(ids=[work_experience_id], include=["metadatas", "embeddings", "documents"])
            print(f"desc_result:", desc_result)

            if desc_result is None or not desc_result.get("ids") or not desc_result["ids"]:
                raise RuntimeError(f"No work experience found for ID: {work_experience_id}")

            metadata_list = desc_result.get("metadatas")
            embedding_list = desc_result.get("embeddings")

            if not metadata_list or embedding_list is None or len(embedding_list) == 0:
                raise RuntimeError(f"No data found for ID: {work_experience_id}")

            metadata = metadata_list[0]
            embedding = embedding_list[0].tolist()  # <-- HERE: convert to list

            return {
                "work_experience_id": work_experience_id,
                "user_id": metadata.get("user_id"),
                "work_experience_desc": metadata.get("work_experience_desc"),
                "total_years": metadata.get("total_years"),
                "embeddings": embedding
            }

        except Exception as e:
            print(f"Error retrieving work experience by ID: {e}")
            raise

    def edit_work_experience(self, work_experience_id: str, work_exp: WorkExperience):
        try:
            print(f"Editing work experience ID: {work_experience_id}")

            # Clean the updated fields
            cleaned_title = clean_text(work_exp.workExperienceTitle)
            cleaned_description = clean_text(work_exp.workExperienceDescription)

            # Generate new embeddings
            title_vector, desc_vector = get_embeddings(self.model, [cleaned_title], [cleaned_description])

            # Update in database
            self.title_collection.update(
                work_experience_id=work_experience_id,
                user_id=work_exp.userId,
                work_experience_title=work_exp.workExperienceTitle,
                total_years=work_exp.totalYears,
                title_vector=title_vector[0]
            )

            self.desc_collection.update(
                work_experience_id=work_experience_id,
                user_id=work_exp.userId,
                work_experience_desc=work_exp.workExperienceDescription,
                total_years=work_exp.totalYears,
                desc_vector=desc_vector[0]
            )

            print(f"Work experience ID {work_experience_id} updated successfully.")
        except Exception as e:
            print(f"Error editing work experience: {e}")
            raise
