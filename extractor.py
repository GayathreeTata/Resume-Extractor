import re
import fitz  # PyMuPDF
import spacy
import spacy.cli
spacy.cli.download("en_core_web_sm")  # This line ensures the model is downloaded
import spacy
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(pdf_file) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(r'\+?\d[\d\s-]{8,}\d', text)
    return match.group(0) if match else None

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

def extract_skills(text):
    skills_db = ["Python", "Java", "AWS", "SQL", "Machine Learning", "Data Science", "Excel", "React", "C++"]
    return [skill for skill in skills_db if skill.lower() in text.lower()]

def extract_experience(text):
    exp = re.findall(r'(?i)(\d+)\+?\s?(years|yrs) of experience', text)
    return exp[0][0] + " years" if exp else None
def extract_certifications(text: str):
    import re

    cert_keywords = [
        "certified", "certificate", "certification", "AWS Certified",
        "Google Cloud Certified", "Microsoft Certified", "Coursera", "Udemy", "edX"
    ]

    lines = text.split('\n')
    certifications = []
    for line in lines:
        if any(keyword.lower() in line.lower() for keyword in cert_keywords):
            certifications.append(line.strip())

    return certifications

def extract_all(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "experience": extract_experience(text),
        "certifications": extract_certifications(text)  

    }
