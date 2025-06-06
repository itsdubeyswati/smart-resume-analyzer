def analyze_resume(resume_text, selected_role):
    # Define skills per role (expand as needed)
    job_skills_dict = {
        "Data Scientist": ["Python", "Machine Learning", "Statistics", "SQL", "Pandas"],
        "ML Engineer": ["Python", "TensorFlow", "PyTorch", "Machine Learning", "Docker"],
        "Software Developer": ["Java", "C++", "Git", "Agile", "SQL"],
        "Business Analyst": ["Excel", "PowerPoint", "SQL", "Communication", "Problem Solving"],
        "Product Manager": ["Roadmapping", "Agile", "Communication", "Leadership", "Analytics"],
        "DevOps Engineer": ["Docker", "Kubernetes", "AWS", "CI/CD", "Linux"],
        "Frontend Developer": ["JavaScript", "React", "CSS", "HTML", "Git"],
        "Backend Developer": ["Python", "Django", "APIs", "SQL", "Docker"],
        "Full Stack Developer": ["JavaScript", "React", "Node.js", "SQL", "Git"],
        "Data Analyst": ["Excel", "SQL", "Tableau", "Python", "Statistics"]
    }

    required_skills = job_skills_dict.get(selected_role, [])

    # Simple skill extraction: split words, title-case for matching
    words = resume_text.split()
    resume_skills = list(set([w.strip(",.()").title() for w in words if len(w) > 2]))

    matched_skills = list(set(resume_skills) & set(required_skills))
    missing_skills = list(set(required_skills) - set(matched_skills))
    match_percentage = (len(matched_skills) / len(required_skills) * 100) if required_skills else 0.0

    return {
        'resume_skills': resume_skills,
        'job_skills': required_skills,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'match_percentage': match_percentage
    }
