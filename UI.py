# THE USER INTERFACE 

import streamlit as st


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
        if resume:
            if jd_file or jd_img or jd_text:
                st.success("Great! We are READY", icon="✅")
            else:
                st.error("please put JD", icon="🚨")
        else:
            st.error("Please Put Resume", icon="🚨")

        st.info('This is a purely informational message', icon="ℹ️")
                                  