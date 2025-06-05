from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_similarity(resume_skills, target_skills):
    matched_skills = []
    unmatched_skills = []

    resume_text = " ".join(resume_skills).lower()
    for skill in target_skills:
        if skill.lower() in resume_text:
            matched_skills.append(skill)
        else:
            unmatched_skills.append(skill)
    
    return matched_skills, unmatched_skills
