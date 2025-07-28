# app.py

import streamlit as st
import utils  # Your utility file with all the helper functions

# --- Page Setup ---
st.set_page_config(layout="wide")
st.title("CareerCraft - AI 🤖")
st.markdown("### **Elite ATS Scorer**")
st.write("Upload your resume and the Job Description to get an elite-level analysis.")
st.divider()

# --- Main Columns ---
column1, column2 = st.columns(2)

# --- Column 1: Resume Upload ---
with column1:
    st.header("📄 Your Resume")
    resume_file = st.file_uploader("Upload your Resume", type=["pdf", "docx"], label_visibility="collapsed")

# --- Column 2: Job Description Input ---
with column2:
    st.header("💼 Job Description")
    # Tabs for different input methods
    jd_tab1, jd_tab2, jd_tab3 = st.tabs(['Paste Text', "Upload PDF/DOCX", "Upload Image"])

    with jd_tab1:
        jd_text_input = st.text_area("Paste the Job Description text here", height=300)
    with jd_tab2:
        jd_file_input = st.file_uploader("Upload the Job Description file", type=["pdf", "docx"])
    with jd_tab3:
        jd_image_input = st.file_uploader("Upload a screenshot of the Job Description", type=["png", "jpg", "jpeg"])

# --- Analyze Button and Logic ---
if st.button("Analyze My Resume", use_container_width=True):
    # Check if a resume has been uploaded
    if resume_file is not None:
        
        # --- 1. Text Extraction ---
        # Extract text from the uploaded resume file
        resume_text = ""
        if resume_file.type == "application/pdf":
            resume_text = utils.get_pdf_text(resume_file)
        elif resume_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = utils.get_docx_text(resume_file)

        # Extract text from the job description input (any of the three tabs)
        jd_text = ""
        if jd_text_input:
            jd_text = jd_text_input
        elif jd_file_input:
            if jd_file_input.type == "application/pdf":
                jd_text = utils.get_pdf_text(jd_file_input)
            elif jd_file_input.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                jd_text = utils.get_docx_text(jd_file_input)
        elif jd_image_input:
            jd_text = utils.get_image_text(jd_image_input)

        # Check if we have the JD text
        if not jd_text:
            st.error("Please provide the Job Description in one of the formats.")
        else:
            # --- 2. Pre-Analysis and Parsing (Our Current Step) ---
            st.info("Running Content Parser...")
            
            # Call the new parsing function from utils.py
            parsed_resume_sections = utils.parse_resume_sections(resume_text)

            # --- 3. Display Parsed Content for Verification ---
            st.subheader("Parsed Resume Sections (for testing):")
            
            if 'error' in parsed_resume_sections:
                st.error(parsed_resume_sections['error'])
            else:
                # Display the content of each parsed section
                for section, content in parsed_resume_sections.items():
                    st.markdown(f"### {section.replace('_', ' ').title()}")
                    # Show first 500 characters of each section to keep it clean
                    st.text(content[:500] + "...") 
            
            # The AI analysis part will be added here in the next step
            # st.info("Next Step: AI Micro-Analysis on the parsed sections.")

    else:
        # If no resume is uploaded
        st.error("Please upload your resume first.")
