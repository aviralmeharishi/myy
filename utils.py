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
