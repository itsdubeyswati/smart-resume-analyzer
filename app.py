import streamlit as st
import os
from extractor import extract_text_from_pdf
from matcher import analyze_resume
from visualizer import (
    create_skills_chart,
    create_match_visualization,
    create_skills_distribution_bar,
    create_match_gauge,
    create_skills_radar,
    # create_skills_wordcloud,  # Optional, see notes below
)
from suggestions import get_improvement_suggestions

def main():
    # Page config - must be first Streamlit call
    st.set_page_config(
        page_title="Smart Resume Analyzer",
        page_icon="💼",
        layout="centered"
    )

    # Custom CSS for blue theme
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .skill-tag {
        background-color: #e3f2fd;
        color: #1565c0;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        margin: 0.25rem;
        display: inline-block;
        font-size: 0.9rem;
    }
    .missing-skill-tag {
        background-color: #ffebee;
        color: #c62828;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        margin: 0.25rem;
        display: inline-block;
        font-size: 0.9rem;
    }
    .section-header {
        color: #1f77b4;
        font-size: 1.4rem;
        font-weight: bold;
        margin: 1.5rem 0 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown('<h1 class="main-header">💼 Smart Resume Analyzer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-powered resume analysis to match your skills with job requirements</p>', unsafe_allow_html=True)

    # Job role selection
    job_roles = [
        "Data Scientist",
        "ML Engineer", 
        "Software Developer",
        "Business Analyst",
        "Product Manager",
        "DevOps Engineer",
        "Frontend Developer",
        "Backend Developer",
        "Full Stack Developer",
        "Data Analyst"
    ]
    
    selected_role = st.selectbox(
        "🎯 Select Target Job Role:",
        job_roles,
        help="Choose the job role you want to analyze your resume against"
    )

    # File upload
    uploaded_file = st.file_uploader(
        "📄 Upload Your Resume (PDF)",
        type=['pdf'],
        help="Upload your resume in PDF format for analysis"
    )

    if uploaded_file is not None:
        # Save uploaded file temporarily
        with open("temp_resume.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Extract text from PDF
        with st.spinner("🔍 Extracting text from your resume..."):
            resume_text = extract_text_from_pdf("temp_resume.pdf")

        if resume_text:
            st.success("✅ Resume text extracted successfully!")

            # Analyze resume
            with st.spinner("🤖 Analyzing your resume..."):
                analysis_result = analyze_resume(resume_text, selected_role)

            # Show match score and skills found
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="metric-container">
                    <h3>Match Score</h3>
                    <h1>{analysis_result.get('match_percentage', 0):.1f}%</h1>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-container">
                    <h3>Skills Found</h3>
                    <h1>{len(analysis_result.get('matched_skills', []))} / {len(analysis_result.get('job_skills', []))}</h1>
                </div>
                """, unsafe_allow_html=True)

            # Skills analysis section
            st.markdown('<h2 class="section-header">📊 Skills Analysis</h2>', unsafe_allow_html=True)

            # Matched skills
            if analysis_result.get('matched_skills'):
                st.markdown("**✅ Skills Found in Your Resume:**")
                skills_html = ""
                for skill in analysis_result['matched_skills']:
                    skills_html += f'<span class="skill-tag">{skill}</span>'
                st.markdown(skills_html, unsafe_allow_html=True)

            # Missing skills
            if analysis_result.get('missing_skills'):
                st.markdown("**❌ Missing Skills:**")
                missing_skills_html = ""
                for skill in analysis_result['missing_skills']:
                    missing_skills_html += f'<span class="missing-skill-tag">{skill}</span>'
                st.markdown(missing_skills_html, unsafe_allow_html=True)

            # Visual Analysis
            st.markdown('<h2 class="section-header">📈 Visual Analysis</h2>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)

            with col1:
                try:
                    skills_chart = create_skills_chart(analysis_result)
                    st.plotly_chart(skills_chart, use_container_width=True)
                except Exception as e:
                    st.error(f"Error generating skills chart: {e}")

                try:
                    skills_dist = create_skills_distribution_bar(analysis_result)
                    st.plotly_chart(skills_dist, use_container_width=True)
                except Exception as e:
                    st.error(f"Error generating skills distribution chart: {e}")

            with col2:
                try:
                    match_viz = create_match_visualization(analysis_result)
                    st.plotly_chart(match_viz, use_container_width=True)
                except Exception as e:
                    st.error(f"Error generating match visualization: {e}")

                try:
                    match_gauge = create_match_gauge(analysis_result)
                    st.plotly_chart(match_gauge, use_container_width=True)
                except Exception as e:
                    st.error(f"Error generating match gauge: {e}")

            # Radar chart full width
            try:
                skills_radar = create_skills_radar(analysis_result)
                st.plotly_chart(skills_radar, use_container_width=True)
            except Exception as e:
                st.error(f"Error generating skills radar chart: {e}")

            # Improvement suggestions
            st.markdown('<h2 class="section-header">💡 Improvement Suggestions</h2>', unsafe_allow_html=True)
            suggestions = get_improvement_suggestions(analysis_result, selected_role)
            for i, suggestion in enumerate(suggestions, 1):
                st.markdown(f"**{i}.** {suggestion}")

        else:
            st.error("❌ Could not extract text from the PDF. Please ensure it's a valid PDF file.")

        # Clean up temp file
        if os.path.exists("temp_resume.pdf"):
            os.remove("temp_resume.pdf")

    else:
        st.info("Please upload your resume in PDF format to start analysis.")

if __name__ == "__main__":
    main()
