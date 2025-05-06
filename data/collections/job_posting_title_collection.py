from clients.chroma_client import chroma_client

collection = chroma_client.get_or_create_collection(name="job_posting_titles")

class JobPostingTitleCollection:
    def add(
        self,
        job_posting_id: str,
        job_title: str,
        required_english_level: str,
        required_experience_years: float,
        required_skills: str,
        title_vector: list[float]
    ):
        collection.add(
            documents=[job_title],
            metadatas=[{
                "job_posting_id": job_posting_id,
                "required_english_level": required_english_level,
                "required_experience_years": required_experience_years,
                "required_skills": required_skills
            }],
            embeddings=[title_vector],
            ids=[job_posting_id]
        )

    def delete(self, job_posting_id: str):
        collection.delete(ids=[job_posting_id])

    def update(
        self,
        job_posting_id: str,
        job_title: str,
        required_english_level: str,
        required_experience_years: float,
        required_skills: str,
        title_vector: list[float]
    ):
        self.delete(job_posting_id)
        self.add(
            job_posting_id,
            job_title,
            required_english_level,
            required_experience_years,
            required_skills,
            title_vector
        )

    def get_by_id(self, job_posting_id: str):
        return collection.get(
            ids=[job_posting_id],
            include=["metadatas", "embeddings", "documents"]
        )

    def get(self, ids: list[str], include: list[str] = None):
        return collection.get(ids=ids, include=include)
