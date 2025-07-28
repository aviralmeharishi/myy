import streamlit as st
import utils

# --- Page Setup and API Configuration ---
st.set_page_config(layout="wide")
st.title("CareerCraft AI 🚀 (Hybrid v2.0)")

try:
    utils.genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except AttributeError:
    import google.generativeai as genai
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        utils.genai = genai
    except Exception as e:
        st.error("API Key not found or configured incorrectly. Please check your secrets.toml file.")
        st.stop()

# --- UI Layout ---
st.markdown("### **Hybrid ATS Scorer**")
st.write("Get a comprehensive analysis powered by a Python+AI hybrid engine.")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.header("📄 Your Resume")
    resume_file = st.file_uploader("Upload your Resume", type=["pdf", "docx"], label_visibility="collapsed")

with col2:
    st.header("💼 Job Description")
    jd_text_input = st.text_area("Paste the Job Description text here", height=300)

# --- Analyze Button Logic ---
if st.button("Run Elite Analysis", use_container_width=True):
    if resume_file and jd_text_input:
        with st.spinner("Rocket Mode On! Running Hybrid Analysis..."):
            try:
                # 1. Text Extraction
                resume_text = utils.get_pdf_text(resume_file) if resume_file.type == "application/pdf" else utils.get_docx_text(resume_file)
                jd_text = jd_text_input

                if not resume_text:
                    st.error("Could not read the resume file. Please ensure it's not corrupted or password-protected.")
                else:
                    # 2. Python Structural Analysis
                    structural_findings = utils.analyze_resume_structure(resume_text)
                    
                    # 3. Hybrid AI Analysis
                    hybrid_report = utils.get_hybrid_analysis(resume_text, jd_text, structural_findings)
                    
                    # 4. Display Report
                    st.divider()
                    st.markdown(hybrid_report)

            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")
    else:
        st.error("Please upload your resume and paste the job description.")


