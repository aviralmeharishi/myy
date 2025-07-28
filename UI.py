import streamlit as st
import utils
import re

# --- Page Setup and API Configuration ---
st.set_page_config(layout="wide", page_title="CareerCraft AI")
st.title("CareerCraft AI 🚀 (v3.0)")

try:
    # Configure the Gemini API key from Streamlit's secrets
    utils.genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except AttributeError:
    # This block runs if 'genai' is not yet an attribute of 'utils'
    import google.generativeai as genai
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        utils.genai = genai  # Assign the configured module to utils
    except Exception as e:
        st.error("API Key not found or is invalid. Please check your .streamlit/secrets.toml file.")
        st.stop()
except Exception as e:
    st.error(f"An error occurred during API configuration: {e}")
    st.stop()

# --- UI Layout ---
st.markdown("### **Elite ATS Scorer & Career Coach**")

# Language selection dropdown
selected_language = st.selectbox("Select Report Language", ["English", "Hinglish", "Hindi"])
st.divider()

col1, col2 = st.columns(2)

# Column 1: Resume Upload
with col1:
    st.header("📄 Your Resume")
    resume_file = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"], label_visibility="collapsed")

# Column 2: Job Description Input with multiple options
with col2:
    st.header("💼 Job Description")
    jd_tab1, jd_tab2, jd_tab3 = st.tabs(['Paste Text', "Upload File (PDF/DOCX)", "Upload Image"])
    with jd_tab1:
        jd_text_input = st.text_area("Paste the Job Description text here", height=250, label_visibility="collapsed")
    with jd_tab2:
        jd_file_input = st.file_uploader("Upload the Job Description file", type=["pdf", "docx"], label_visibility="collapsed")
    with jd_tab3:
        jd_image_input = st.file_uploader("Upload a screenshot of the JD", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

# --- Analyze Button and Main Logic ---
if st.button("Run Elite Analysis", use_container_width=True):
    if resume_file and (jd_text_input or jd_file_input or jd_image_input):
        with st.spinner("Rocket Mode On! Running Elite Analysis... This might take a moment..."):
            try:
                # --- 1. Text Extraction ---
                resume_text = utils.get_pdf_text(resume_file) if resume_file.type == "application/pdf" else utils.get_docx_text(resume_file)
                
                jd_text = ""
                is_jd_from_image = False
                if jd_text_input:
                    jd_text = jd_text_input
                elif jd_file_input:
                    jd_text = utils.get_pdf_text(jd_file_input) if jd_file_input.type == "application/pdf" else utils.get_docx_text(jd_file_input)
                elif jd_image_input:
                    jd_text = utils.get_image_text(jd_image_input)
                    if jd_text:
                        is_jd_from_image = True

                # --- OCR Verification Step ---
                if is_jd_from_image:
                    st.divider()
                    with st.expander("⚠️ Please Verify Extracted Text from JD Image", expanded=True):
                        st.info("OCR technology isn't always perfect. Please review and edit the extracted text below to ensure its accuracy before analysis.")
                        verified_jd_text = st.text_area("Edit Extracted Text:", value=jd_text, height=250)
                        jd_text = verified_jd_text # Use the user-verified text
                    st.divider()

                if not resume_text or not jd_text:
                    st.error("Could not read the resume or JD. Please try a different file or check the verified text.")
                else:
                    # --- 2. Python Structural Analysis ---
                    structural_findings = utils.analyze_resume_structure(resume_text)
                    
                    # --- 3. Hybrid AI Analysis ---
                    hybrid_report_str = utils.get_hybrid_analysis(resume_text, jd_text, structural_findings, selected_language)
                    
                    # --- 4. Parse and Display the Structured Report ---
                    st.divider()
                    st.header("🤖 Elite ATS Analysis Report")

                    def extract_content(tag, text):
                        try:
                            # Use regex for more robust parsing
                            match = re.search(f'\\[{tag}\\](.*?)\\[/{tag}\\]', text, re.DOTALL)
                            return match.group(1).strip() if match else f"Could not parse the '{tag}' section."
                        except Exception:
                            return f"Error parsing the '{tag}' section."

                    score = extract_content("SCORE", hybrid_report_str)
                    summary = extract_content("SUMMARY", hybrid_report_str)
                    skills = extract_content("SKILLS", hybrid_report_str)
                    impact = extract_content("IMPACT", hybrid_report_str)
                    recommendations = extract_content("RECOMMENDATIONS", hybrid_report_str)

                    # --- Professional Dashboard Layout ---
                    st.metric(label="Overall ATS Fit Score", value=f"{score}/100")
                    
                    st.subheader("📝 Coach's Summary")
                    st.markdown(summary)

                    with st.expander("✅ Skill Gap Analysis"):
                        st.markdown(skills)
                    
                    with st.expander("💼 Experience & Impact Analysis"):
                        st.markdown(impact)

                    with st.expander("🚀 Actionable Recommendations"):
                        st.markdown(recommendations)

            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    else:
        st.error("Please upload your resume AND provide the job description.")
