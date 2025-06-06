import fitz  # PyMuPDF
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.chunk import ne_chunk
from nltk.tag import pos_tag
import spacy
import pandas as pd
from datetime import datetime
import streamlit as st

class ResumeParser:
    def __init__(self):
        """Initialize the Resume Parser with necessary NLP models and data"""
        self.setup_nltk()
        self.setup_spacy()
        self.skills_database = self.load_skills_database()
        
    def setup_nltk(self):
        """Download required NLTK data"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
            
        try:
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('averaged_perceptron_tagger')
            
        try:
            nltk.data.find('chunkers/maxent_ne_chunker')
        except LookupError:
            nltk.download('maxent_ne_chunker')
            
        try:
            nltk.data.find('corpora/words')
        except LookupError:
            nltk.download('words')
    
    def setup_spacy(self):
        """Load spaCy model"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            st.error("spaCy English model not found. Please install it using: python -m spacy download en_core_web_sm")
            self.nlp = None
    
    def load_skills_database(self):
        """Load comprehensive skills database categorized by job roles"""
        skills_db = {
            'programming': [
                'python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift',
                'kotlin', 'scala', 'r', 'matlab', 'perl', 'shell', 'bash', 'powershell'
            ],
            'web_development': [
                'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask',
                'spring', 'laravel', 'bootstrap', 'jquery', 'webpack', 'sass', 'less'
            ],
            'data_science': [
                'machine learning', 'deep learning', 'neural networks', 'tensorflow', 'pytorch',
                'keras', 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'plotly',
                'tableau', 'power bi', 'statistics', 'data mining', 'nlp', 'computer vision'
            ],
            'databases': [
                'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'oracle',
                'sqlite', 'nosql', 'elasticsearch', 'neo4j'
            ],
            'cloud': [
                'aws', 'azure', 'google cloud', 'docker', 'kubernetes', 'jenkins', 'terraform',
                'ansible', 'cloudformation', 'lambda', 'ec2', 's3', 'rds'
            ],
            'tools': [
                'git', 'github', 'gitlab', 'bitbucket', 'jira', 'confluence', 'slack', 'trello',
                'figma', 'sketch', 'photoshop', 'illustrator', 'postman', 'swagger'
            ],
            'business': [
                'project management', 'agile', 'scrum', 'kanban', 'business analysis',
                'product management', 'stakeholder management', 'requirements gathering',
                'process improvement', 'strategic planning'
            ],
            'soft_skills': [
                'leadership', 'communication', 'teamwork', 'problem solving', 'analytical thinking',
                'creativity', 'adaptability', 'time management', 'critical thinking', 'collaboration'
            ]
        }
        return skills_db
    
    def extract_text_from_pdf(self, pdf_file):
        """Extract text from PDF file using PyMuPDF"""
        try:
            # Read PDF file
            pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
            text = ""
            
            # Extract text from each page
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text += page.get_text()
            
            pdf_document.close()
            return text
        except Exception as e:
            st.error(f"Error extracting text from PDF: {str(e)}")
            return ""
    
    def clean_text(self, text):
        """Clean and preprocess extracted text"""
        # Remove extra whitespaces and newlines
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep important ones
        text = re.sub(r'[^\w\s\.\,\@\-\+\(\)]', ' ', text)
        # Convert to lowercase for processing
        return text.lower().strip()
    
    def extract_contact_info(self, text):
        """Extract contact information from resume text"""
        contact_info = {}
        
        # Email extraction
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text, re.IGNORECASE)
        contact_info['email'] = emails[0] if emails else None
        
        # Phone number extraction
        phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        contact_info['phone'] = phones[0] if phones else None
        
        # LinkedIn profile extraction
        linkedin_pattern = r'linkedin\.com/in/[\w\-]+'
        linkedin = re.findall(linkedin_pattern, text, re.IGNORECASE)
        contact_info['linkedin'] = linkedin[0] if linkedin else None
        
        # GitHub profile extraction
        github_pattern = r'github\.com/[\w\-]+'
        github = re.findall(github_pattern, text, re.IGNORECASE)
        contact_info['github'] = github[0] if github else None
        
        return contact_info
    
    def extract_education(self, text):
        """Extract education information"""
        education_keywords = [
            'bachelor', 'master', 'phd', 'doctorate', 'diploma', 'certificate',
            'b.tech', 'm.tech', 'b.sc', 'm.sc', 'mba', 'bba', 'b.com', 'm.com'
        ]
        
        education_info = []
        sentences = sent_tokenize(text)
        
        for sentence in sentences:
            for keyword in education_keywords:
                if keyword in sentence.lower():
                    education_info.append(sentence.strip())
                    break
        
        return list(set(education_info))  # Remove duplicates
    
    def extract_experience(self, text):
        """Extract work experience information"""
        experience_patterns = [
            r'(\d+)[\+\s]*years?\s+(?:of\s+)?experience',
            r'experience[:\s]+(\d+)[\+\s]*years?',
            r'(\d+)[\+\s]*yrs?\s+(?:of\s+)?(?:exp|experience)'
        ]
        
        years_experience = []
        for pattern in experience_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            years_experience.extend([int(match) for match in matches])
        
        total_experience = max(years_experience) if years_experience else 0
        
        # Extract company names and job titles (basic extraction)
        job_titles = []
        company_names = []
        
        # Common job title patterns
        job_title_patterns = [
            r'(?:software|senior|junior|lead|principal)\s+(?:developer|engineer|analyst|manager)',
            r'(?:data|business|product|project)\s+(?:scientist|analyst|manager)',
            r'(?:full stack|frontend|backend)\s+developer'
        ]
        
        for pattern in job_title_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            job_titles.extend(matches)
        
        return {
            'total_experience': total_experience,
            'job_titles': list(set(job_titles)),
            'companies': company_names
        }
    
    def extract_skills(self, text):
        """Extract skills from resume text using multiple approaches"""
        extracted_skills = {
            'programming': [],
            'web_development': [],
            'data_science': [],
            'databases': [],
            'cloud': [],
            'tools': [],
            'business': [],
            'soft_skills': []
        }
        
        # Method 1: Direct keyword matching
        for category, skills_list in self.skills_database.items():
            for skill in skills_list:
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                if re.search(pattern, text.lower()):
                    extracted_skills[category].append(skill)
        
        # Method 2: NLP-based extraction using spaCy (if available)
        if self.nlp:
            doc = self.nlp(text)
            
            # Extract entities that might be skills
            for ent in doc.ents:
                if ent.label_ in ['ORG', 'PRODUCT', 'LANGUAGE']:
                    skill_text = ent.text.lower()
                    # Check if this entity matches any skill in our database
                    for category, skills_list in self.skills_database.items():
                        for skill in skills_list:
                            if skill in skill_text or skill_text in skill:
                                if skill not in extracted_skills[category]:
                                    extracted_skills[category].append(skill)
        
        # Method 3: Section-based extraction
        sections = self.identify_resume_sections(text)
        if 'skills' in sections:
            skills_section = sections['skills']
            for category, skills_list in self.skills_database.items():
                for skill in skills_list:
                    pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                    if re.search(pattern, skills_section.lower()):
                        if skill not in extracted_skills[category]:
                            extracted_skills[category].append(skill)
        
        # Remove duplicates and clean up
        for category in extracted_skills:
            extracted_skills[category] = list(set(extracted_skills[category]))
        
        return extracted_skills
    
    def identify_resume_sections(self, text):
        """Identify different sections of the resume"""
        sections = {}
        
        section_patterns = {
            'skills': r'(?:technical\s+)?skills?(?:\s+(?:and|&)\s+(?:technologies|expertise))?[:\s]*(.*?)(?=\n\s*(?:[A-Z][A-Z\s]{3,}|$))',
            'experience': r'(?:work\s+)?experience[:\s]*(.*?)(?=\n\s*(?:[A-Z][A-Z\s]{3,}|$))',
            'education': r'education[:\s]*(.*?)(?=\n\s*(?:[A-Z][A-Z\s]{3,}|$))',
            'projects': r'projects?[:\s]*(.*?)(?=\n\s*(?:[A-Z][A-Z\s]{3,}|$))',
            'certifications': r'certifications?[:\s]*(.*?)(?=\n\s*(?:[A-Z][A-Z\s]{3,}|$))'
        }
        
        for section_name, pattern in section_patterns.items():
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                sections[section_name] = match.group(1).strip()
        
        return sections
    
    def calculate_skill_proficiency(self, text, skills):
        """Estimate skill proficiency based on context"""
        proficiency_scores = {}
        
        proficiency_keywords = {
            'expert': 5,
            'advanced': 4,
            'proficient': 4,
            'experienced': 3,
            'intermediate': 3,
            'familiar': 2,
            'basic': 1,
            'beginner': 1
        }
        
        for category, skill_list in skills.items():
            for skill in skill_list:
                score = 2  # Default score
                
                # Look for proficiency indicators near the skill mention
                skill_context_pattern = r'.{0,50}\b' + re.escape(skill.lower()) + r'\b.{0,50}'
                context_matches = re.findall(skill_context_pattern, text.lower())
                
                for context in context_matches:
                    for keyword, level in proficiency_keywords.items():
                        if keyword in context:
                            score = max(score, level)
                
                proficiency_scores[skill] = score
        
        return proficiency_scores
    
    def parse_resume(self, pdf_file):
        """Main method to parse resume and extract all information"""
        try:
            # Extract text from PDF
            raw_text = self.extract_text_from_pdf(pdf_file)
            if not raw_text:
                return None
            
            # Clean text
            cleaned_text = self.clean_text(raw_text)
            
            # Extract various components
            contact_info = self.extract_contact_info(raw_text)
            education_info = self.extract_education(cleaned_text)
            experience_info = self.extract_experience(cleaned_text)
            skills_info = self.extract_skills(cleaned_text)
            skill_proficiency = self.calculate_skill_proficiency(cleaned_text, skills_info)
            
            # Flatten skills for easier processing
            all_skills = []
            for category, skills_list in skills_info.items():
                all_skills.extend(skills_list)
            
            # Create comprehensive resume data
            resume_data = {
                'raw_text': raw_text,
                'cleaned_text': cleaned_text,
                'contact_info': contact_info,
                'education': education_info,
                'experience': experience_info,
                'skills_by_category': skills_info,
                'all_skills': all_skills,
                'skill_proficiency': skill_proficiency,
                'total_skills_count': len(all_skills),
                'parsing_timestamp': datetime.now().isoformat()
            }
            
            return resume_data
            
        except Exception as e:
            st.error(f"Error parsing resume: {str(e)}")
            return None
    
    def get_skills_summary(self, resume_data):
        """Generate a summary of extracted skills"""
        if not resume_data:
            return None
        
        skills_summary = {
            'total_skills': resume_data['total_skills_count'],
            'skills_by_category': {},
            'top_skills': []
        }
        
        # Count skills by category
        for category, skills_list in resume_data['skills_by_category'].items():
            if skills_list:
                skills_summary['skills_by_category'][category] = len(skills_list)
        
        # Get top skills based on proficiency
        if resume_data['skill_proficiency']:
            sorted_skills = sorted(
                resume_data['skill_proficiency'].items(),
                key=lambda x: x[1],
                reverse=True
            )
            skills_summary['top_skills'] = sorted_skills[:10]
        
        return skills_summary