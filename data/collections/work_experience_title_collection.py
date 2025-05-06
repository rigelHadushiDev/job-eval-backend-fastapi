from clients.chroma_client import chroma_client

collection = chroma_client.get_or_create_collection(name="work_experience_titles")

class WorkExperienceTitleCollection:
    def add(self, work_experience_id: str, user_id: int, work_experience_title: str, total_years: float, title_vector: list[float]):
        collection.add(
            documents=[work_experience_title],
            metadatas=[{
                "user_id": user_id,
                "total_years": total_years
            }],
            embeddings=[title_vector],
            ids=[work_experience_id]
        )

    def delete(self, work_experience_id: str):
        collection.delete(ids=[work_experience_id])

    def update(self, work_experience_id: str, user_id: int, work_experience_title: str, total_years: float, title_vector: list[float]):
        self.delete(work_experience_id)
        self.add(work_experience_id, user_id, work_experience_title, total_years, title_vector)

    def get_by_id(self, work_experience_id: str):
            result = collection.get(
                ids=[work_experience_id],
                include=["metadatas", "embeddings", "documents"] 
            )
            return result

    def get_all_by_user(self, user_id: int):
        return collection.get(
            where={"user_id": user_id},
            include=["embeddings", "metadatas", "documents"]
        )

    def get(self, ids: list[str], include: list[str] = None):
        return collection.get(ids=ids, include=include)