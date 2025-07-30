import streamlit as st
import utils
import re

# --- Page Setup and API Configuration ---
st.set_page_config(layout="wide", page_title="CareerCraft AI")
st.title("CareerCraft AI 🚀 (Elite Final)")

try:
    utils.genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except AttributeError:
    import google.generativeai as genai
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        utils.genai = genai
    except Exception:
        st.error("API Key not found. Please check your .streamlit/secrets.toml file.")
        st.stop()

# --- UI Layout ---
st.markdown("### **The Truly Reliable ATS Scorer**")
selected_language = st.selectbox("Select Report Language", ["English", "Hinglish", "Hindi"])
st.divider()

col1, col2 = st.columns(2)
with col1:
    st.header("📄 Your Resume")
    resume_file = st.file_uploader("Upload your Resume", type=["pdf", "docx"], label_visibility="collapsed")
with col2:
    st.header("💼 Job Description")
    jd_file = st.file_uploader("Upload Job Description", type=["pdf", "docx", "png", "jpg"], label_visibility="collapsed")

# --- Main Logic ---
if st.button("Run Final Elite Analysis", use_container_width=True):
    if resume_file and jd_file:
        with st.spinner("Running Elite Engine... This is the final, reliable version..."):
            try:
                # 1. Text Extraction
                resume_text = utils.get_text(resume_file)
                jd_text = utils.get_text(jd_file)

                if not resume_text or not jd_text:
                    st.error("Could not read one of the files. Please ensure it's not corrupted.")
                else:
                    # 2. Python-Based Analysis
                    structural_findings = utils.analyze_resume_structure(resume_text)
                    resume_companies = utils.extract_entities(resume_text, labels=["ORG"])
                    
                    # 3. AI Micro-Analysis
                    mismatch_result = utils.check_details_mismatch(jd_text, resume_companies)
                    ai_report_str = utils.get_qualitative_analysis(resume_text, jd_text, selected_language)

                    # 4. Final Scoring in Python (The Reliable Part)
                    def extract_content(tag, text):
                        try:
                            return re.search(f'\\[{tag}\\](.*?)\\[/{tag}\\]', text, re.DOTALL).group(1).strip()
                        except Exception: return ""

                    impact_score = int(extract_content("IMPACT_SCORE", ai_report_str) or 0) * 10
                    skills_score = int(extract_content("SKILLS_SCORE", ai_report_str) or 0) * 10
                    structural_score = structural_findings["structural_score"]

                    final_score = int((structural_score * 0.25) + (skills_score * 0.45) + (impact_score * 0.30))

                    # --- THE PENALTY SYSTEM ---
                    penalty_applied = False
                    if "yes" in mismatch_result.lower():
                        final_score = int(final_score * 0.70) # Apply 30% penalty
                        penalty_applied = True

                    # 5. Display Report
                    st.divider()
                    st.header("🤖 Elite ATS Analysis Report")

                    if penalty_applied:
                        st.error("⚠️ **Critical Mismatch Found!** A 30% penalty has been applied to your score. The resume does not seem to be tailored for the company in the job description.", icon="🚨")

                    st.metric(label="Final ATS Score", value=f"{final_score}/100")
                    
                    st.subheader("📝 Coach's Summary")
                    st.markdown(extract_content("SUMMARY", ai_report_str))

                    with st.expander("✅ Skill Gap Analysis"):
                        st.markdown(extract_content("SKILLS_ANALYSIS", ai_report_str))
                    
                    with st.expander("💼 Experience & Impact Analysis"):
                        st.markdown(extract_content("IMPACT_ANALYSIS", ai_report_str))

                    with st.expander("🚀 Actionable Recommendations"):
                        st.markdown(extract_content("RECOMMENDATIONS", ai_report_str))

            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.error("Please upload both your resume and the job description.")
