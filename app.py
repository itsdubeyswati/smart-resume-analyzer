import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Set page config
st.set_page_config(page_title="Smart Resume Analyzer", layout="wide", initial_sidebar_state="collapsed")

# Hide sidebar and sidebar toggle arrow
st.markdown("""
    <style>
        [data-testid="collapsedControl"], [data-testid="stSidebar"] {
            display: none;
        }

        .main {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }

        .stButton > button {
            background-color: #1f77b4;
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            font-size: 1.1rem;
            border-radius: 8px;
            transition: 0.3s ease;
        }

        .stButton > button:hover {
            background-color: #145a86;
            transform: scale(1.05);
            color: white;
        }

        .stFileUploader, .stSelectbox > div {
            width: 60% !important;
            margin: auto;
            background-color: #2b2b2b !important;
            color: white !important;
            border-radius: 10px;
            border: 1px solid #555;
        }

        .big-title {
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            color: #2c8cff;
        }

        .subtext {
            text-align: center;
            margin-bottom: 2rem;
            font-size: 1rem;
            color: white;
        }

        .section-label {
            margin-top: 2rem;
            font-weight: 600;
            font-size: 1.3rem;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Title & Subtitle
st.markdown("<div class='big-title'>🔍 Smart Resume Analyzer</div>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Upload your resume and select a job role to get insights into your skills</div>", unsafe_allow_html=True)

# Upload Resume
st.markdown("<div class='section-label'>📄 Upload Resume (PDF only)</div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload", type=["pdf"], label_visibility="collapsed")

# Select Job Role
st.markdown("<div class='section-label'>🎯 Select Job Role</div>", unsafe_allow_html=True)
job_role = st.selectbox("", ["Select", "Data Scientist", "Web Developer", "Machine Learning Engineer", "Business Analyst"])

# Centered Analyze Button
analyze = st.button("🚀 Analyze Resume")

# Resume analysis placeholder
if analyze:
    if uploaded_file is None or job_role == "Select":
        st.warning("⚠️ Please upload a resume and select a job role before analyzing.")
    else:
        st.success("✅ Resume successfully analyzed!")

        # Simulated analysis output (replace this with actual logic if available)
        st.markdown("### 🔍 Resume Insights")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Skill Match Distribution (Pie Chart)")
            labels = ['Python', 'SQL', 'ML', 'DL', 'Web Dev']
            values = [25, 20, 15, 20, 20]
            fig1, ax1 = plt.subplots()
            ax1.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            st.pyplot(fig1)

        with col2:
            st.markdown("#### Proficiency Levels (Horizontal Bar)")
            skills = ['Python', 'SQL', 'ML', 'DL', 'Web Dev']
            scores = [80, 70, 60, 50, 65]
            fig2, ax2 = plt.subplots()
            ax2.barh(skills, scores, color='skyblue')
            ax2.set_xlim(0, 100)
            ax2.set_xlabel("Proficiency (%)")
            st.pyplot(fig2)

        st.markdown("#### Skill Balance Radar Chart")
        # Radar chart
        categories = ['Coding', 'Data', 'ML', 'Soft Skills', 'Communication']
        values = [80, 75, 65, 85, 70]
        values += values[:1]  # close the loop
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]

        fig3, ax3 = plt.subplots(subplot_kw={'polar': True})
        ax3.plot(angles, values, 'o-', linewidth=2)
        ax3.fill(angles, values, alpha=0.3)
        ax3.set_xticks(angles[:-1])
        ax3.set_xticklabels(categories)
        ax3.set_yticklabels([])
        st.pyplot(fig3)
