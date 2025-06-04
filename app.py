
# import streamlit as st
# import json
# import os
# from extractor import extract_all
# import spacy.cli

# # Ensure spacy model is downloaded
# spacy.cli.download("en_core_web_sm")

# st.title("📄 Resume Skill Extractor")

# uploaded_file = st.file_uploader("Upload a resume (PDF)", type=["pdf"])

# def generate_summary(data: dict) -> str:
#     """
#     Generate a descriptive summary from the extracted resume data.
#     This function can be customized based on the structure of 'data'.
#     """
#     summary_parts = []

#     # Example fields, adjust based on your extractor's output keys
#     name = data.get("name")
#     if name:
#         summary_parts.append(f"Candidate Name: {name}")

#     title = data.get("title")
#     if title:
#         summary_parts.append(f"Professional Title: {title}")

#     skills = data.get("skills")
#     if skills:
#         summary_parts.append(f"Skills: {', '.join(skills)}")

#     experience = data.get("experience")
#     if experience:
#         # Assuming experience is a list of dicts or strings describing roles
#         exp_summaries = []
#         for exp in experience:
#             if isinstance(exp, dict):
#                 role = exp.get("role", "Role")
#                 company = exp.get("company", "")
#                 duration = exp.get("duration", "")
#                 exp_summaries.append(f"{role} at {company} ({duration})".strip())
#             else:
#                 exp_summaries.append(str(exp))
#         summary_parts.append(f"Experience: { '; '.join(exp_summaries)}")

#     education = data.get("education")
#     if education:
#         edu_summaries = []
#         for edu in education:
#             if isinstance(edu, dict):
#                 degree = edu.get("degree", "")
#                 school = edu.get("school", "")
#                 year = edu.get("year", "")
#                 edu_summaries.append(f"{degree} from {school} ({year})".strip())
#             else:
#                 edu_summaries.append(str(edu))
#         summary_parts.append(f"Education: { '; '.join(edu_summaries)}")

#     if not summary_parts:
#         return "No summary could be generated from the extracted data."

#     return "\n\n".join(summary_parts)

# if uploaded_file:
#     # Create folders if they don't exist
#     os.makedirs("resumes", exist_ok=True)
#     os.makedirs("data", exist_ok=True)

#     # Save uploaded file
#     file_path = f"resumes/{uploaded_file.name}"
#     with open(file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())

#     st.write(f"Uploaded file saved at {file_path}")

#     # Extract data from saved resume PDF
#     try:
#         result = extract_all(file_path)
#         st.subheader("🔍 Extracted Information:")
#         st.json(result)

#         # Generate and display descriptive summary
#         summary = generate_summary(result)
#         st.subheader("📝 Resume Summary:")
#         st.text(summary)

#         # Save extraction results to JSON file
#         json_path = "data/results.json"
#         if os.path.exists(json_path):
#             with open(json_path, "r") as f:
#                 all_results = json.load(f)
#         else:
#             all_results = []

#         all_results.append(result)

#         with open(json_path, "w") as f:
#             json.dump(all_results, f, indent=2)

#         st.success("✅ Resume data extracted, summarized, and saved!")

#     except Exception as e:
#         st.error(f"Extraction failed: {e}")


import streamlit as st
import json
import os
from extractor import extract_all
import spacy.cli

# Ensure spaCy model is downloaded
spacy.cli.download("en_core_web_sm")

# ---- UI CONFIG ----
st.set_page_config(
    page_title="Resume Skill Extractor",
    page_icon="📄",
    layout="centered"
)

# ---- SIDEBAR ----
with st.sidebar:
    st.title("💼 Resume Extractor")
    st.markdown("""
    This tool helps you:
    - 🔍 Extract structured data from your resume  
    - 🧠 Auto-generate a descriptive summary  
    - 💾 Save and view results  
    """)
    st.info("PDF format only. Make sure your file is well-formatted!")

# ---- MAIN TITLE ----
st.title("📄 Smart Resume Skill Extractor")
st.caption("Powered by spaCy, Python & your awesome resume 🚀")

uploaded_file = st.file_uploader("📤 Upload your resume (PDF format)", type=["pdf"])

# ---- SUMMARY GENERATOR ----
def generate_summary(data: dict) -> str:
    summary_parts = []

    name = data.get("name")
    if name:
        summary_parts.append(f"👤 **Candidate Name**: {name}")

    title = data.get("title")
    if title:
        summary_parts.append(f"💼 **Professional Title**: {title}")

    skills = data.get("skills")
    if skills:
        summary_parts.append(f"🧠 **Skills**: {', '.join(skills)}")
    

    experience = data.get("experience")
    if experience:
        exp_summaries = []
        for exp in experience:
            if isinstance(exp, dict):
                role = exp.get("role", "Role")
                company = exp.get("company", "")
                duration = exp.get("duration", "")
                exp_summaries.append(f"{role} at {company} ({duration})".strip())
            else:
                exp_summaries.append(str(exp))
        summary_parts.append(f"📌 **Experience**:\n- " + "\n- ".join(exp_summaries))

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
        summary_parts.append(f"🎓 **Education**:\n- " + "\n- ".join(edu_summaries))

    if not summary_parts:
        return "_No summary could be generated from the extracted data._"

    return "\n\n".join(summary_parts)

# ---- PROCESS RESUME ----
if uploaded_file:
    try:
        os.makedirs("resumes", exist_ok=True)
        os.makedirs("data", exist_ok=True)

        file_path = os.path.join("resumes", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("✅ Resume uploaded successfully!")
        st.markdown(f"**File saved to:** `{file_path}`")

        # Extract info
        result = extract_all(file_path)

        st.subheader("🔍 Extracted Details:")
        st.json(result)

        st.subheader("📝 Auto-Generated Summary:")
        st.markdown(generate_summary(result))

        # Save results to JSON
        # Save results to JSON file
        json_path = "data/results.json"
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                all_results = json.load(f)
        else:
            all_results = []
            all_results.append(result)
            with open(json_path, "w") as f:
                json.dump(all_results, f, indent=2)
                # ✅ Show success
                st.success("💾 Data saved successfully to results.json!")

# 📥 Provide download option for current result
        st.download_button(
            label="📥 Download Extracted Result (JSON)",
            data=json.dumps(result, indent=2),
            file_name="extracted_resume.json",
            mime="application/json"
        )


    except Exception as e:
        st.error("❌ Oops! Something went wrong during processing.")
        st.exception(e)

else:
    st.info("Please upload a resume to begin.")
