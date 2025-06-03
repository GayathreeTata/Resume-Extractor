import streamlit as st
import json
import os
from extractor import extract_all
import spacy.cli

# Ensure spacy model is downloaded
spacy.cli.download("en_core_web_sm")

st.title("📄 Resume Skill Extractor")

uploaded_file = st.file_uploader("Upload a resume (PDF)", type=["pdf"])

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

        st.success("✅ Resume data extracted and saved!")

    except Exception as e:
        st.error(f"Extraction failed: {e}")

