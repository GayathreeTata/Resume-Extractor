# import streamlit as st
# import json
# import os
# from extractor import extract_all
# import spacy.cli

# # Ensure spacy model is downloaded
# spacy.cli.download("en_core_web_sm")

# st.title("📄 Resume Skill Extractor")

# uploaded_file = st.file_uploader("Upload a resume (PDF)", type=["pdf"])

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

#         st.success("✅ Resume data extracted and saved!")

#     except Exception as e:
#         st.error(f"Extraction failed: {e}")


import streamlit as st
import json
import os
import pandas as pd
from extractor import extract_all
import spacy.cli
from datetime import datetime

# Initialize session state for storing resumes
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = []

# Ensure spacy model is downloaded
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# App Configuration
st.set_page_config(
    page_title="Advanced Resume Skill Extractor",
    page_icon="📄",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .skill-pill {
        display: inline-block;
        padding: 5px 15px;
        margin: 3px;
        border-radius: 20px;
        background-color: #4CAF50;
        color: white;
        font-size: 14px;
    }
    .section-card {
        border-radius: 10px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
        padding: 15px;
        margin-bottom: 15px;
    }
    .resume-card {
        border-left: 4px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for filters and actions
with st.sidebar:
    st.title("🔍 Filters")
    
    # Skill filter
    skill_filter = st.text_input("Filter by skill", "")
    
    # Experience level filter
    exp_level = st.selectbox(
        "Experience level",
        ["All", "Entry", "Mid", "Senior"]
    )
    
    # Education filter
    education_filter = st.multiselect(
        "Education level",
        ["Bachelor", "Master", "PhD", "Diploma"]
    )
    
    st.markdown("---")
    if st.button("Clear All Filters"):
        skill_filter = ""
    
    st.markdown("---")
    st.markdown("**Actions**")
    if st.button("Export All Data to CSV"):
        # Implementation would go here
        st.success("Export functionality would be implemented here")

# Main Content
st.title("📄 Advanced Resume Skill Extractor")
st.markdown("Upload and analyze resumes with powerful filtering capabilities")

# File Upload Section
with st.expander("➕ Upload New Resume", expanded=True):
    uploaded_file = st.file_uploader(
        "Drag and drop PDF resume here",
        type=["pdf"],
        help="Only PDF files are supported",
        key="uploader"
    )

# Process uploaded file
if uploaded_file:
    # Create folders if they don't exist
    os.makedirs("resumes", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    # Save uploaded file with progress
    file_path = f"resumes/{uploaded_file.name}"
    with st.spinner("Processing resume..."):
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        try:
            result = extract_all(file_path)
            result['upload_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result['file_name'] = uploaded_file.name
            
            # Add to session state
            st.session_state.resume_data.append(result)
            
            # Save to JSON file
            json_path = "data/results.json"
            if os.path.exists(json_path):
                with open(json_path, "r") as f:
                    all_results = json.load(f)
            else:
                all_results = []
            
            all_results.append(result)
            
            with open(json_path, "w") as f:
                json.dump(all_results, f, indent=2)
            
            st.success("✅ Resume processed successfully!")
            
        except Exception as e:
            st.error(f"❌ Extraction failed: {e}")

# Display Resumes with Filters
if st.session_state.resume_data:
    st.markdown("---")
    st.subheader("📂 Resume Database")
    
    # Apply filters
    filtered_data = st.session_state.resume_data
    
    if skill_filter:
        filtered_data = [
            r for r in filtered_data 
            if any(skill_filter.lower() in skill.lower() 
                 for skill in r.get('skills', []))
        ]
    
    if exp_level != "All":
        filtered_data = [
            r for r in filtered_data 
            if r.get('experience_level', '').lower() == exp_level.lower()
        ]
    
    if education_filter:
        filtered_data = [
            r for r in filtered_data 
            if any(edu.lower() in [e.lower() for e in education_filter]
                 for edu in r.get('education', []))
        ]
    
    # Display filtered results
    if not filtered_data:
        st.warning("No resumes match your filters")
    else:
        for resume in filtered_data:
            with st.container():
                st.markdown(f"### {resume.get('name', 'Unknown Name')}")
                
                cols = st.columns([1, 3])
                with cols[0]:
                    st.markdown(f"**Uploaded:** {resume.get('upload_date', 'N/A')}")
                    st.markdown(f"**File:** {resume.get('file_name', 'N/A')}")
                
                with cols[1]:
                    with st.expander("View Details"):
                        # Contact Info
                        if resume.get('contact'):
                            st.markdown("#### 📞 Contact Information")
                            st.write(resume['contact'])
                        
                        # Skills
                        if resume.get('skills'):
                            st.markdown("#### 💡 Skills")
                            st.markdown(
                                " ".join([f"<span class='skill-pill'>{skill}</span>" 
                                         for skill in resume['skills']]),
                                unsafe_allow_html=True
                            )
                        
                        # Experience
                        if resume.get('experience'):
                            st.markdown("#### 💼 Experience")
                            for exp in resume['experience']:
                                st.markdown(f"**{exp.get('position', '')}** at *{exp.get('company', '')}*")
                                st.markdown(f"*{exp.get('duration', '')}*")
                                st.markdown(exp.get('description', ''))
                                st.markdown("---")
                        
                        # Education
                        if resume.get('education'):
                            st.markdown("#### 🎓 Education")
                            for edu in resume['education']:
                                st.markdown(f"**{edu.get('degree', '')}**")
                                st.markdown(f"*{edu.get('institution', '')}*")
                                st.markdown(f"*{edu.get('year', '')}*")
                                st.markdown("---")
                
                st.markdown("---")

# Summary Statistics Section
if st.session_state.resume_data:
    st.markdown("---")
    st.subheader("📊 Summary Statistics")
    
    # Create DataFrame for analysis
    df = pd.DataFrame(st.session_state.resume_data)
    
    # Skills frequency
    if 'skills' in df.columns:
        all_skills = [skill for sublist in df['skills'] for skill in sublist]
        skills_df = pd.DataFrame(all_skills, columns=['Skill']).value_counts().reset_index()
        skills_df.columns = ['Skill', 'Count']
        
        cols = st.columns(2)
        with cols[0]:
            st.markdown("#### Top Skills")
            st.bar_chart(skills_df.head(10).set_index('Skill'))
        
        with cols[1]:
            st.markdown("#### Skill Frequency")
            st.dataframe(skills_df.head(15), hide_index=True)
    
    # Experience level distribution
    if 'experience_level' in df.columns:
        st.markdown("#### Experience Level Distribution")
        exp_df = df['experience_level'].value_counts().reset_index()
        exp_df.columns = ['Level', 'Count']
        st.bar_chart(exp_df.set_index('Level'))

