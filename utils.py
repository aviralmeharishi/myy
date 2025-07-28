import PyPDF2
import docx
import pytesseract
from PIL import Image
import re
import google.generativeai as genai



def get_pdf_text(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f'Error In Reading FIle as {e}'
    



def get_docx_text(docx_file):
    try:
        doc = docx.Document(docx_file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        return f"Error reading DOCX file: {e}"
    



def get_image_text(image_file):
    try:
        image = Image.open(image_file)
        # Using pytesseract to do OCR on the image
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Error reading image file: {e}"

def parse_resume_sections(resume_text):
    """
    Detects and parses the content of key resume sections with corrections.
    """
    patterns = {
        'summary': r'(?im)^\s*(summary|objective|profile|about me|professional summary)',
        'experience': r'(?im)^\s*(experience|employment history|work history|professional experience|career history)',
        'education': r'(?im)^\s*(education|academic qualifications|academics|educational background)',
        'skills': r'(?im)^\s*(skills|technical skills|proficiencies|technologies|key skills|core competencies)',
        'projects': r'(?im)^\s*(projects|personal projects|academic projects|technical projects|portfolio)'
    }
    
    matches = []
    for section_name, pattern in patterns.items():
        for match in re.finditer(pattern, resume_text):
            matches.append((section_name, match.start()))

    if not matches:
        return {'error': "Could not parse resume sections. Please use standard headers."}

    # This part was incorrectly indented in your code
    matches.sort(key=lambda x: x[1])

    parsed_sections = {}
    for i in range(len(matches)):
        section_name, start_index = matches[i]
        
        end_index = len(resume_text)
        if i + 1 < len(matches):
            end_index = matches[i+1][1]
        
        content = resume_text[start_index:end_index].strip()
        
        # Remove the header itself from the content
        header_match = re.search(patterns[section_name], content, re.IGNORECASE | re.MULTILINE)
        if header_match:
            content = content[header_match.end():].strip()
            
        parsed_sections[section_name] = content

    return parsed_sections








def analyze_resume_structure(resume_text):
    """
    Analyzes the resume for structural elements using Python rules.
    Returns a dictionary of findings and a score.
    """
    findings = {
        "contact_info_present": bool(re.search(r'(?i)phone|email|linkedin|github|portfolio', resume_text)),
        "summary_section_found": bool(re.search(r'(?im)^\s*(summary|objective|profile)', resume_text)),
        "experience_section_found": bool(re.search(r'(?im)^\s*(experience|employment history)', resume_text)),
        "education_section_found": bool(re.search(r'(?im)^\s*(education|academic)', resume_text)),
        "skills_section_found": bool(re.search(r'(?im)^\s*(skills|technical skills)', resume_text)),
    }
    
    # Calculate a simple structural score based on the presence of key sections
    score = sum(findings.values()) * 20  # Each finding is worth 20 points
    findings["structural_score"] = score
    
    return findings











# utils.py

# ... (keep all your other functions like get_pdf_text, etc.) ...

import google.generativeai as genai

def get_hybrid_analysis(resume_text, jd_text, structural_findings, language):
    """
    Generates a RELIABLE and language-specific analysis.
    """
    findings_str = "\n".join([f"- {key.replace('_', ' ').title()}: {'Yes' if value else 'No'}" for key, value in structural_findings.items() if key != "structural_score"])

    # --- STRICTER PROMPT ---
    # We are now giving a much more forceful command for the language.
    input_prompt = f"""
    You are an expert ATS and a world-class career coach.
    Your MOST IMPORTANT instruction is to generate the entire response STRICTLY in the following language: **{language}**.
    Do not use any other language. All headers, titles, and text must be in **{language}**.

    **Python Structural Analysis (Baseline Facts):**
    {findings_str}
    - Structural Score (out of 100): {structural_findings['structural_score']}

    **Resume Text:**
    ```
    {resume_text}
    ```

    **Job Description Text:**
    ```
    {jd_text}
    ```
    ---
    **Your Detailed Contextual Analysis (in {language}):**
    Based on all the provided information, generate a report in Markdown format.

    ### **Elite ATS Analysis Report**

    **1. Final ATS Score & Profile Summary:**
       - **Final ATS Score:** Provide a final score out of 100. This should be a weighted average of the Python Structural Score (30% weight) and your contextual analysis of keywords and impact (70% weight).
       - **Coach's Summary:** Write a 2-3 line expert summary on the candidate's suitability.

    **2. Skill-Gap Analysis (Contextual):**
       - **Analysis:** Evaluate how well the skills in the resume align with the job description.
       - **Missing Critical Skills:** List the top 3-5 most critical skills from the JD that are missing.

    **3. Experience & Impact Analysis (Contextual):**
       - **Analysis:** Scrutinize the work experience for quantifiable results.
       - **Actionable Rewrite Suggestion:** Select one weak bullet point and provide a rewritten "strong" version.

    **4. Final Recommendations:**
       - Provide 2-3 concrete, high-priority action items for the user.
    """
    
    # --- LOCKING THE TEMPERATURE ---
    # We are setting temperature to a low value to ensure consistent, non-random outputs.
    generation_config = {
        "temperature": 0.2,
    }
    
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash-latest',
        generation_config=generation_config
    )
    
    response = model.generate_content(input_prompt)
    return response.text
    ```
    {resume_text}
    ```

    **Job Description Text:**
    ```
    {jd_text}
    ```
    ---
    **Your Detailed Analysis:**
    Generate a report using the EXACT following format with the specified tags. Do not add any text outside of these tags.

    [SCORE]
    Provide a final ATS score out of 100. Just the number.
    [/SCORE]

    [SUMMARY]
    Write a 2-3 line expert summary on the candidate's suitability and key areas for improvement.
    [/SUMMARY]

    [SKILLS]
    Critically analyze the skills alignment. List the top 3-5 most critical skills from the JD that are missing.
    [/SKILLS]

    [IMPACT]
    Scrutinize the work experience section for impact. Select one weak bullet point and provide a rewritten "strong" version.
    [/IMPACT]

    [RECOMMENDATIONS]
    Provide 2-3 concrete, high-priority action items for the user.
    [/RECOMMENDATIONS]
    """
    
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content(input_prompt)
    return response.text
