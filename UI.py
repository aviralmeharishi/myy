# THE USER INTERFACE 

import streamlit as st
import utilis

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
        jd_text = st.text_area("Paste The Job Description", height=300)


    with jd_tab2:
        jd_file = st.file_uploader("Upload The Job Description File", type=['pdf', "docx"])


    with jd_tab3:
        jd_img = st.file_uploader("Upload the Job Description ScreenShot", type=["png", "jpg", "jpeg"])



    if st.button("Analyze My Resume", use_container_width=True):
        if resume is not None:

            resume_text = ""
            if resume.type == "application/pdf":
                resume_text = utilis.get_pdf_text(resume)
            else:
                resume_text = utilis.get_docx_text(resume)



            jd= ""
            if jd_text:
                jd = jd_text
            elif jd_file:
                if jd_file.type == "application/pdf":
                    jd = utilis.get_pdf_text(jd_file)
                else:
                    jd = utilis.get_docx_text(jd_file)
        elif jd_img:
            jd = utilis.get_image_text(jd_img)



        if not jd_text:
            st.error("Please provide the Job Description.")
        else:
            st.success("Text Extracted Successfully! Ready for analysis.")

            st.subheader("Extracted Resume Text (First 500 Chars)")
            st.text(resume_text[:500])


            st.subheader("Extracted Job Description Text (First 500 Chars)")
            st.text(jd[:500])

    else:
        st.error("Please upload your resume first.")

    st.info('This is a purely informational message', icon="ℹ️")
                                  
