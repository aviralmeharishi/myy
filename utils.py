import re
import PyPDF2
import docx
from PIL import Image
import pytesseract
import spacy
import google.generativeai as genai

# Load the spaCy model once
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None

# --- 1. Text Extraction Functions ---
def get_text(file):
    """Extracts text from PDF, DOCX, or Image files."""
    try:
        if file.type == "application/pdf":
            reader = PyPDF2.PdfReader(file)
            return "".join(page.extract_text() or "" for page in reader.pages)
        elif "document" in file.type:
            doc = docx.Document(file)
            return "\n".join(para.text for para in doc.paragraphs)
        elif "image" in file.type:
            image = Image.open(file)
            return pytesseract.image_to_string(image)
    except Exception:
        return None

# --- 2. Python-Based Analysis Functions ---
def analyze_resume_structure(resume_text):
    """Analyzes the resume for key structural elements using Python rules."""
    findings = {
        "contact_info_present": bool(re.search(r'(?i)phone|email|linkedin|github', resume_text)),
        "summary_found": bool(re.search(r'(?im)^\s*(summary|objective|profile)', resume_text)),
        "experience_found": bool(re.search(r'(?im)^\s*(experience|employment history)', resume_text)),
        "education_found": bool(re.search(r'(?im)^\s*(education|academic)', resume_text)),
        "skills_found": bool(re.search(r'(?im)^\s*(skills|technical skills)', resume_text)),
    }
    score = sum(findings.values()) * 20
    findings["structural_score"] = score
    return findings

def extract_entities(text, labels=["ORG"]):
    """Extracts named entities like company names (ORG) from text using spaCy."""
    if not nlp: return []
    doc = nlp(text)
    return list(set([ent.text for ent in doc.ents if ent.label_ in labels]))

# --- 3. NEW: Single, Optimized AI Analysis Function ---
def get_final_analysis(resume_text, jd_text, resume_companies, language):
    """Generates the complete analysis in a single, optimized API call."""
    prompt = f"""
    You are an expert ATS and a world-class career coach. Perform a two-part analysis.
    CRITICAL RULE: The entire response MUST be in the language: **{language}**.
    The tags like [MISMATCH], [IMPACT_SCORE], etc., MUST remain in English.

    **Part 1: Strict Mismatch Check**
    Compare the target company from the Job Description with the list of companies mentioned in the resume.
    Job Description: "{jd_text[:500]}..." 
    Companies listed in Resume: {resume_companies}
    Is there a clear mismatch? For example, if the JD is for 'Google' and the resume summary says 'seeking a role at Microsoft'.

    [MISMATCH]
    Answer ONLY with 'Yes', 'No', or 'Not Applicable'.
    [/MISMATCH]

    **Part 2: Qualitative Analysis**
    Now, provide a detailed analysis of the resume against the JD.

    [IMPACT_SCORE]
    On a scale of 1-10, how impactful is the work experience section? Just the number.
    [/IMPACT_SCORE]

    [SKILLS_SCORE]
    On a scale of 1-10, how well do the skills align with the JD? Just the number.
    [/SKILLS_SCORE]

    [SUMMARY]
    Write a 2-3 line expert summary.
    [/SUMMARY]

    [SKILLS_ANALYSIS]
    List the top 3-5 critical skills from the JD that are missing.
    [/SKILLS_ANALYSIS]

    [IMPACT_ANALYSIS]
    Select one weak bullet point and provide a rewritten "strong" version.
    [/IMPACT_ANALYSIS]

    [RECOMMENDATIONS]
    Provide 2-3 concrete, high-priority action items.
    [/RECOMMENDATIONS]
    """
    model = genai.GenerativeModel('gemini-1.5-flash-latest', generation_config={"temperature": 0.2})
    response = model.generate_content(prompt)
    return response.text
