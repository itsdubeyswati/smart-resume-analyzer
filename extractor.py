import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text

def extract_entities(text):
    # Simple keyword-based extraction (can be enhanced with spaCy)
    skill_keywords = [
        "python", "java", "c++", "html", "css", "javascript",
        "react", "nodejs", "sql", "mongodb", "machine learning",
        "deep learning", "tensorflow", "pytorch", "nlp",
        "data analysis", "pandas", "numpy", "matplotlib", "flask"
    ]
    found_skills = []
    text_lower = text.lower()
    for skill in skill_keywords:
        if re.search(r"\b" + re.escape(skill) + r"\b", text_lower):
            found_skills.append(skill)
    return found_skills
