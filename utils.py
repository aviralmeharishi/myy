import PyPDF2
import docx
import pytesseract
from PIL import Image




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
    patterns = {
        "Summary" : r'(?im)^\s*(summary|about me|description|objective|profile|)',
        "Experience" : r'(?im)^\s*(experience|employment history|work history|professional experience)',
        'education': r'(?im)^\s*(education|academic qualifications|academics)',
        'skills': r'(?im)^\s*(skills|technical skills|proficiencies|technologies)',
        'projects': r'(?im)^\s*(projects|personal projects|academic projects)'
    }
    matches = []
    for section_name, pattern in patterns.items():
        for match in re.finditer(pattern, resume_text):
            matches.append((section_name, match.start()))
    if not matches:
        return {'error': "Could not parse resume sections. Please use standard headers like 'Summary', 'Experience', etc."}
        matches.sort(key=lambda x: x[1])
        
    parsed_sections = {}
    for i in range(len(matches)):
        section_name, start_index = matches[i]
        if i + 1 < len(matches):
            end_index = matches[i+1][1]
        else:
            end_index = len(resume_text)
        section_content = resume_text[start_index:end_index].strip()
        parsed_sections[section_name] = section_content
    return parsed_sections
