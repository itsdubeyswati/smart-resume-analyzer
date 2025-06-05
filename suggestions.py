skills_list = [
    "python", "machine learning", "deep learning", "data science", "sql", "nlp",
    "tensorflow", "pytorch", "excel", "aws", "azure", "git", "github", "docker",
    "html", "css", "javascript", "power bi", "tableau", "flask", "fastapi"
]

def get_skill_matches(resume_text, jd_text):
    found = []
    missing = []
    for skill in skills_list:
        if skill.lower() in resume_text.lower():
            found.append(skill)
        elif skill.lower() in jd_text.lower():
            missing.append(skill)
    return found, missing
