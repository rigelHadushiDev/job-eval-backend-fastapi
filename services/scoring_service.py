from typing import Dict, List, Optional
import numpy as np
import math
from schemas.applicant_request import ApplicantRequest, EducationLevelEntry, SkillEntry
from constants.scoring_weights import EDUCATION_LEVEL_SCORES, ENGLISH_LEVEL_SCORES
from schemas.generate_score_response import GenerateScoreResponse


class ScoringService:
    def __init__(
        self,
        job_desc_collection,
        job_title_collection,
        work_desc_collection,
        work_title_collection
    ):
        self.job_desc_collection = job_desc_collection
        self.job_title_collection = job_title_collection
        self.work_desc_collection = work_desc_collection
        self.work_title_collection = work_title_collection

        self.work_experience_years: float = 0.0

    def calculate_education_score(self, education_levels: Optional[List[EducationLevelEntry]]) -> float:
        if not education_levels:
            return 0.0  
        
        highest_score = max(
            (EDUCATION_LEVEL_SCORES.get(entry.educationLevel.upper(), 0) 
             for entry in education_levels if entry.educationLevel),
            default=0.0
        )
        return highest_score
    
    def calculate_english_score(self, english_level: Optional[str]) -> float:
        if not english_level:  
            return 0.0  
        return ENGLISH_LEVEL_SCORES.get(english_level.upper(), 0.0)

    @staticmethod
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        v1, v2 = np.array(vec1), np.array(vec2)
        norm_product = np.linalg.norm(v1) * np.linalg.norm(v2)
        if norm_product == 0:
            return 0.0
        return float(np.dot(v1, v2) / norm_product)

    @staticmethod
    def experience_score(candidate_exp: float, required_exp: float, steepness: float = 1.0) -> float:
        if candidate_exp == 0.0:
            return 0.0

        if candidate_exp >= required_exp:
            return 1.0
        
        x = candidate_exp - required_exp
        score = 1 / (1 + math.exp(-steepness * x))
        return min(2 * score, 1.0) 


    def compute_work_experience_similarity(self, work_titles, work_descs, job_title_vec, job_desc_vec) -> float:
        total_similarity = 0.0
        total_years = 0.0
        count = 0

        for idx, (title_vec, desc_vec) in enumerate(zip(work_titles['embeddings'], work_descs['embeddings'])):
            title_sim = self.cosine_similarity(title_vec, job_title_vec)
            desc_sim = self.cosine_similarity(desc_vec, job_desc_vec)
            combined_sim = 0.5 * title_sim + 0.5 * desc_sim

            metadata = work_descs['metadatas'][idx]
            experience_years = metadata.get('total_years', 0.0)

            total_similarity += combined_sim
            total_years += experience_years
            count += 1

        if count == 0:
            self.work_experience_years = 0.0
            return 0.0 

        average_similarity = round(total_similarity / count, 4)
        self.work_experience_years = round(total_years, 2)

        return average_similarity
        
    

    def get_vectors(self, user_id: int, job_posting_id: str):
        work_titles = self.work_title_collection.get_all_by_user(user_id)
        work_descs = self.work_desc_collection.get_all_by_user(user_id)

        job_title_data = self.job_title_collection.get_by_id(job_posting_id)
        job_desc_data = self.job_desc_collection.get_by_id(job_posting_id)

        job_title_vec = job_title_data['embeddings'][0]
        job_desc_vec = job_desc_data['embeddings'][0]

        return work_titles, work_descs, job_title_vec, job_desc_vec

    @staticmethod
    def skill_coverage(user_skill_names, job_skill_names) -> float:
        user_set = set(user_skill_names)
        job_set = set(job_skill_names)
        intersection = user_set & job_set
        union = user_set | job_set
        return len(intersection) / len(union) if union else 0.0

    @staticmethod
    def skill_score(user_skills: Optional[List[SkillEntry]], job_skills_str: str) -> float:
        if not user_skills or not job_skills_str:  
            return 0.0  
        
        job_skills = [skill.strip().lower() for skill in job_skills_str.split(",") if skill.strip()]
        skill_proficiency = {name.strip().lower(): prof / 5 for name, prof in user_skills}
        user_skill_names = set(skill_proficiency.keys())

        matched = user_skill_names & set(job_skills)

        if not matched:
            return 0.0

        avg_proficiency = sum(skill_proficiency[skill] for skill in matched) / len(matched)
        coverage = ScoringService.skill_coverage(user_skill_names, job_skills)

        return round(coverage * avg_proficiency, 4)

    def calculate_final_score(self, applicant: ApplicantRequest) -> float:
        user_id = applicant.userId
        job_posting_id = str(applicant.jobPostingId)

        work_titles, work_descs, job_title_vec, job_desc_vec = self.get_vectors(user_id, job_posting_id)

        similarity_score = self.compute_work_experience_similarity(work_titles, work_descs, job_title_vec, job_desc_vec)
        total_years = self.work_experience_years

        job_desc_record = self.job_desc_collection.get_by_id(job_posting_id)
        job_metadata = job_desc_record["metadatas"][0]
        required_exp = job_metadata.get("required_experience_years", 0.0)
        job_skills_str = job_metadata.get("required_skills", "")  

        exp_score = self.experience_score(candidate_exp=total_years, required_exp=required_exp)

        education_score = self.calculate_education_score(applicant.educationLevel)
        english_score = self.calculate_english_score(applicant.englishLevel)

        user_skills = [(entry.skillName, entry.skillProficiency) for entry in applicant.skills] if applicant.skills else []
        skill_score = self.skill_score(user_skills, job_skills_str="")  

        final_score = round((
            0.40 * similarity_score +
            0.20 * exp_score +
            0.15 * education_score +
            0.15 * english_score +
            0.10 * skill_score
        ), 4)

        return GenerateScoreResponse(
            experience_similarity_score=round(similarity_score * 100, 2),
            experience_years_score=round(exp_score * 100, 2),
            education_score=round(education_score * 100, 2),
            english_score=round(english_score * 100, 2),
            skill_score=round(skill_score * 100, 2),
            final_score=round(final_score * 100, 2)
        )
