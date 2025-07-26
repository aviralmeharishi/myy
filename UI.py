# THE USER INTERFACE 

import streamlit as st
import utils  # CORRECTED: Was 'utilis'

st.set_page_config(layout="wide")
st.title("CareerCraft - AI 🤖")
st.markdown("# **ATS Scorer 😎😎**")

st.write("HERE YOU NEED TO UPLOAD YOUR RESUME(PDF OR DOC) AND THE JOB DESCRIPTION(TEXT, IMAGE, PDF, DOC) AND GET AN ELITE LEVEL ANALYSIS 😎")
st.divider()

column1, column2 = st.columns(2)

with column1:
    st.header("Please Upload Your Resume 📄📄")
    resume = st.file_uploader(label="Upload Your Resume Here....", type=['pdf', "docx"], label_visibility="collapsed")

with column2:
    st.header("Job Description 💼 ")
    jd_tab1, jd_tab2, jd_tab3 = st.tabs(['Paste Text', "Upload PDF/DOCX", "Upload Image"])

    with jd_tab1:
        jd_text_input = st.text_area("Paste The Job Description", height=300)
    with jd_tab2:
        jd_file = st.file_uploader("Upload The Job Description File", type=['pdf', "docx"])
    with jd_tab3:
        jd_img = st.file_uploader("Upload the Job Description ScreenShot", type=["png", "jpg", "jpeg"])

if st.button("Analyze My Resume", use_container_width=True):
    if resume is not None:
        # --- Resume Text Extraction ---
        resume_text = ""
        if resume.type == "application/pdf":
            resume_text = utils.get_pdf_text(resume)  # CORRECTED
        else:
            resume_text = utils.get_docx_text(resume) # CORRECTED

        # --- Job Description Text Extraction ---
        jd = "" # Final variable to hold JD text
        if jd_text_input:
            jd = jd_text_input
        elif jd_file:
            if jd_file.type == "application/pdf":
                jd = utils.get_pdf_text(jd_file)  # CORRECTED
            else:
                jd = utils.get_docx_text(jd_file) # CORRECTED
        elif jd_img:
            jd = utils.get_image_text(jd_img) # CORRECTED

        # --- Final Check and Display ---
        if not jd: # CORRECTED: Check the final 'jd' variable
            st.error("Please provide the Job Description in one of the formats.")
        else:
            st.success("Text Extracted Successfully! Ready for analysis.")
            
            st.subheader("Extracted Resume Text (First 500 Chars)")
            st.text(resume_text[:500])

            st.subheader("Extracted Job Description Text (First 500 Chars)")
            st.text(jd[:500]) # CORRECTED: Display the final 'jd' variable

    else:
        st.error("Please upload your resume first.")

    st.info('This is a purely informational message', icon="ℹ️")
                                  
