import streamlit as st
import os
import zipfile
import tempfile
import fitz  # PyMuPDF
import pandas as pd
import time

from docx import Document
from typing import TypedDict, Optional, Annotated
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# ------------------------------------------------
# Load Environment
# ------------------------------------------------
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("gemini")

# ------------------------------------------------
# Streamlit Config
# ------------------------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="😎"
)

st.title(":rainbow[🤖 AI-Powered Resume Analyzer & CSV Generator]")

# ------------------------------------------------
# Safer Resume Schema
# ------------------------------------------------
class DataFormat(TypedDict):
    summary: Annotated[str, "Short professional summary"]
    experience: Annotated[Optional[str], "Years of experience or null"]
    skills: list[str]
    links: list[str]

# ------------------------------------------------
# Model (Stable)
# ------------------------------------------------
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

final_model = model.with_structured_output(DataFormat)

# ------------------------------------------------
# File Readers
# ------------------------------------------------
def read_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def read_docx(file_path):
    doc = Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs)

def read_resume(file_path):
    if file_path.lower().endswith(".pdf"):
        return read_pdf(file_path)
    elif file_path.lower().endswith(".docx"):
        return read_docx(file_path)
    return ""

# ------------------------------------------------
# UI
# ------------------------------------------------
uploaded_zip = st.file_uploader(
    "Upload ZIP containing PDF or DOCX resumes",
    type="zip"
)

# ------------------------------------------------
# Processing
# ------------------------------------------------
if uploaded_zip and st.button("Analyze Resumes"):
    results = []

    with st.spinner("Analyzing resumes..."):
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, "resumes.zip")

            with open(zip_path, "wb") as f:
                f.write(uploaded_zip.read())

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir)

            for file in os.listdir(temp_dir):
                if file.lower().endswith((".pdf", ".docx")):
                    file_path = os.path.join(temp_dir, file)

                    resume_text = read_resume(file_path)

                    if not resume_text.strip():
                        continue

                    # 🔒 Prevent token overflow
                    resume_text = resume_text[:12000]

                    prompt = f"""
You are an expert HR resume analyzer.

Extract the following:
- Short professional summary
- Total years of experience (as text)
- Skills (return an empty list [] if none)
- Any links (LinkedIn, GitHub, portfolio — return [] if none)

Resume Text:
{resume_text}
"""

                    try:
                        response = final_model.invoke(prompt)
                        time.sleep(3)
                        response["resume_file"] = file
                        results.append(response)

                    except Exception as e:
                        st.error(f"❌ Failed to process {file}")
                        st.exception(e)

    # ------------------------------------------------
    # CSV Output
    # ------------------------------------------------
    if results:
        df = pd.DataFrame(results)

        df["skills"] = df["skills"].apply(lambda x: ", ".join(x))
        df["links"] = df["links"].apply(lambda x: ", ".join(x))

        csv = df.to_csv(index=False)

        st.success("✅ Resume analysis completed!")
        st.dataframe(df)

        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name="resume_analysis.csv",
            mime="text/csv"
        )
    else:
        st.error("No resumes were successfully processed.")