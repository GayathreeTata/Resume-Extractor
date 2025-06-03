
import streamlit as st
import json
import os
from extractor import extract_all
import spacy.cli

# Ensure spacy model is downloaded
spacy.cli.download("en_core_web_sm")

st.title("📄 Resume Skill Extractor")

uploaded_file = st.file_uploader("Upload a resume (PDF)", type=["pdf"])

def generate_summary(data: dict) -> str:
    """
    Generate a descriptive summary from the extracted resume data.
    This function can be customized based on the structure of 'data'.
    """
    summary_parts = []

    # Example fields, adjust based on your extractor's output keys
    name = data.get("name")
    if name:
        summary_parts.append(f"Candidate Name: {name}")

    title = data.get("title")
    if title:
        summary_parts.append(f"Professional Title: {title}")

    skills = data.get("skills")
    if skills:
        summary_parts.append(f"Skills: {', '.join(skills)}")

    experience = data.get("experience")
    if experience:
        # Assuming experience is a list of dicts or strings describing roles
        exp_summaries = []
        for exp in experience:
            if isinstance(exp, dict):
                role = exp.get("role", "Role")
                company = exp.get("company", "")
                duration = exp.get("duration", "")
                exp_summaries.append(f"{role} at {company} ({duration})".strip())
            else:
                exp_summaries.append(str(exp))
        summary_parts.append(f"Experience: { '; '.join(exp_summaries)}")

    education = data.get("education")
    if education:
        edu_summaries = []
        for edu in education:
            if isinstance(edu, dict):
                degree = edu.get("degree", "")
                school = edu.get("school", "")
                year = edu.get("year", "")
                edu_summaries.append(f"{degree} from {school} ({year})".strip())
            else:
                edu_summaries.append(str(edu))
        summary_parts.append(f"Education: { '; '.join(edu_summaries)}")

    if not summary_parts:
        return "No summary could be generated from the extracted data."

    return "\n\n".join(summary_parts)

if uploaded_file:
    # Create folders if they don't exist
    os.makedirs("resumes", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    # Save uploaded file
    file_path = f"resumes/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.write(f"Uploaded file saved at {file_path}")

    # Extract data from saved resume PDF
    try:
        result = extract_all(file_path)
        st.subheader("🔍 Extracted Information:")
        st.json(result)

        # Generate and display descriptive summary
        summary = generate_summary(result)
        st.subheader("📝 Resume Summary:")
        st.text(summary)

        # Save extraction results to JSON file
        json_path = "data/results.json"
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                all_results = json.load(f)
        else:
            all_results = []

        all_results.append(result)

        with open(json_path, "w") as f:
            json.dump(all_results, f, indent=2)

        st.success("✅ Resume data extracted, summarized, and saved!")

    except Exception as e:
        st.error(f"Extraction failed: {e}")
