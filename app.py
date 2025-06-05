import streamlit as st
import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
import plotly.express as px
import pandas as pd

# Streamlit page config
st.set_page_config(page_title="Smart Resume Analyzer", layout="wide")

# Title
st.title("🧠 Smart Resume Analyzer")
st.markdown("Upload your resume and get instant skill insights & recommendations!")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    images = convert_from_bytes(pdf_file.read())
    for img in images:
        text += pytesseract.image_to_string(img)
    return text

# Function to analyze resume
def analyze_resume(file):
    st.markdown("---")
    st.subheader("📊 Resume Analysis Results")
    st.success(f"Successfully uploaded: **{file.name}**")
    
    # Dummy extracted data — you can plug in NLP models here later
    extracted_skills = {
        "Python": 90,
        "Machine Learning": 80,
        "Data Analysis": 70,
        "SQL": 60,
        "Communication": 50,
        "Leadership": 40
    }

    skill_categories = {
        "Technical": 70,
        "Soft Skills": 30
    }

    experience_data = {
        "Company A": 2,
        "Company B": 1,
        "Internship at XYZ": 0.5
    }

    # Skill Bar Chart
    st.markdown("### 📌 Skill Proficiency")
    skill_df = pd.DataFrame(list(extracted_skills.items()), columns=["Skill", "Proficiency"])
    fig1 = px.bar(skill_df, x="Skill", y="Proficiency", color="Proficiency", text="Proficiency", color_continuous_scale="blues")
    st.plotly_chart(fig1, use_container_width=True)

    # Skill Category Pie Chart
    st.markdown("### 🧠 Skill Category Distribution")
    cat_df = pd.DataFrame(list(skill_categories.items()), columns=["Category", "Percentage"])
    fig2 = px.pie(cat_df, names="Category", values="Percentage", color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig2, use_container_width=True)

    # Experience Chart
    st.markdown("### ⏳ Work Experience Summary (Years)")
    exp_df = pd.DataFrame(list(experience_data.items()), columns=["Company", "Years"])
    fig3 = px.bar(exp_df, x="Years", y="Company", orientation="h", color="Years", text="Years", color_continuous_scale="viridis")
    st.plotly_chart(fig3, use_container_width=True)

# Upload section
st.markdown("---")
uploaded_file = st.file_uploader("📄 Upload Your Resume (PDF only)", type=["pdf"])

if uploaded_file:
    analyze_resume(uploaded_file)
else:
    st.info("Please upload a PDF resume to get started.")
