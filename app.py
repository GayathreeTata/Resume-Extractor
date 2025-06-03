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
from extractor import extract_all
import spacy.cli
from streamlit_extras.colored_header import colored_header
from streamlit_extras.card import card
from streamlit_extras.stylable_container import stylable_container
import time

# Ensure spacy model is downloaded
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# App Configuration
st.set_page_config(
    page_title="✨ Resume Skill Extractor",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    .st-bb {
        background-color: #f0f2f6;
    }
    .st-at {
        background-color: #ffffff;
    }
    .st-eb {
        padding: 20px;
    }
    .skill-pill {
        display: inline-block;
        padding: 5px 15px;
        margin: 5px;
        border-radius: 20px;
        background-color: #4CAF50;
        color: white;
        font-size: 14px;
    }
    .section-card {
        border-radius: 10px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        padding: 15px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("Resume Skill Extractor")
    st.markdown("""
    Upload your resume in PDF format and we'll extract:
    - Skills
    - Experience
    - Education
    - Contact Information
    """)
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit")

# Main Content
colored_header(
    label="✨ Resume Skill Extractor",
    description="Upload your resume to extract valuable insights",
    color_name="blue-70"
)

# File Uploader with Enhanced UI
with stylable_container(
    key="upload_container",
    css_styles="""
    {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 25px;
    }
    """
):
    uploaded_file = st.file_uploader(
        "📤 Drag and drop your resume (PDF) here or click to browse",
        type=["pdf"],
        help="Only PDF files are supported"
    )

if uploaded_file:
    # Create folders if they don't exist
    os.makedirs("resumes", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    # Save uploaded file with progress
    file_path = f"resumes/{uploaded_file.name}"
    with st.spinner("Saving your resume..."):
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    
    # Success message
    st.toast("✅ File uploaded successfully!", icon="✅")
    
    # Extract data with progress bar
    progress_text = "Analyzing your resume..."
    my_bar = st.progress(0, text=progress_text)
    
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    
    try:
        result = extract_all(file_path)
        
        # Display results in expandable sections
        with st.expander("📄 **Extracted Resume Data**", expanded=True):
            tab1, tab2, tab3 = st.tabs(["📊 Summary", "🔍 Full Details", "📂 JSON View"])
            
            with tab1:
                st.subheader("🔍 Key Information")
                cols = st.columns(3)
                
                with cols[0]:
                    card(
                        title="Skills",
                        text=f"{len(result.get('skills', []))} skills found",
                        styles={
                            "card": {
                                "width": "100%",
                                "height": "120px"
                            }
                        }
                    )
                    st.markdown("<div class='section-card'>" + 
                               "<h4>Top Skills</h4>" + 
                               "".join([f"<span class='skill-pill'>{skill}</span>" for skill in result.get('skills', [])[:10]]) + 
                               "</div>", unsafe_allow_html=True)
                
                with cols[1]:
                    card(
                        title="Experience",
                        text=f"{len(result.get('experience', []))} positions found",
                        styles={
                            "card": {
                                "width": "100%",
                                "height": "120px"
                            }
                        }
                    )
                    if result.get('experience'):
                        st.markdown("<div class='section-card'><h4>Recent Roles</h4>", unsafe_allow_html=True)
                        for exp in result.get('experience', [])[:3]:
                            st.markdown(f"**{exp.get('position', '')}** at {exp.get('company', '')}")
                            st.markdown(f"*{exp.get('duration', '')}*")
                            st.markdown("---")
                        st.markdown("</div>", unsafe_allow_html=True)
                
                with cols[2]:
                    card(
                        title="Education",
                        text=f"{len(result.get('education', []))} institutions found",
                        styles={
                            "card": {
                                "width": "100%",
                                "height": "120px"
                            }
                        }
                    )
                    if result.get('education'):
                        st.markdown("<div class='section-card'><h4>Education</h4>", unsafe_allow_html=True)
                        for edu in result.get('education', [])[:3]:
                            st.markdown(f"**{edu.get('degree', '')}**")
                            st.markdown(f"*{edu.get('institution', '')}*")
                            st.markdown("---")
                        st.markdown("</div>", unsafe_allow_html=True)
            
            with tab2:
                st.subheader("Detailed Resume Analysis")
                st.write(result)
            
            with tab3:
                st.subheader("Raw JSON Data")
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
        
        # Success animation
        st.balloons()
        st.success("🎉 Resume data extracted and saved successfully!")
        
    except Exception as e:
        st.error(f"❌ Extraction failed: {e}")
        st.exception(e)
