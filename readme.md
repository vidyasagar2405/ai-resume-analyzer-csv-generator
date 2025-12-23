# 🤖 AI-Powered Resume Analyzer & CSV Generator

An end-to-end **LLM-powered resume analysis system** that automates bulk resume screening by converting unstructured resumes into structured CSV data using **Gemini, LangChain, and Streamlit**.

---

## 📌 Project Overview

Recruiters and HR teams often receive resumes in bulk—commonly as **ZIP files containing PDFs and DOCX documents**.
Manually reviewing and extracting information from each resume is time-consuming, inconsistent, and error-prone.

This project solves that problem by using **Large Language Models (LLMs)** to automatically analyze resumes and generate a **clean, structured CSV** that can be easily filtered, searched, and analyzed.

---

## 🎯 Key Features

* 📁 Upload a **ZIP file** containing multiple resumes
* 📄 Supports **PDF and DOCX** formats
* 🧠 Uses **Gemini LLM with structured output**
* 📊 Extracts consistent resume information
* 📥 Generates a **downloadable CSV file**
* 🌐 Simple and interactive **Streamlit UI**

---

## 🧠 Extracted Resume Information

Each resume is converted into structured fields such as:

* Professional Summary
* Total Experience (text-based)
* Skills (list format)
* Links (LinkedIn, GitHub, Portfolio)

---

## 🏗️ System Architecture

```
ZIP File (PDF / DOCX)
        ↓
File Extraction
        ↓
Text Extraction (PDF & DOCX)
        ↓
Gemini + LangChain
        ↓
Structured Resume Data
        ↓
CSV Generation
        ↓
Download via Streamlit
```

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit**
* **LangChain**
* **Gemini (Google Generative AI)**
* **PyMuPDF (PDF parsing)**
* **python-docx**
* **Pandas**
* **Pydantic**
* **dotenv**

---

## 🚀 How to Run Locally

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/ai-resume-analyzer-csv-generator.git
cd ai-resume-analyzer-csv-generator
```

### 2️⃣ Create & activate virtual environment

```bash
python -m venv csv_generator
source csv_generator/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set up environment variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

### 5️⃣ Run the application

```bash
python -m streamlit run app.py
```

---

## 💼 Use Cases

* HR resume screening automation
* Bulk resume parsing
* Candidate data standardization
* Resume analytics & filtering
* ATS-style preprocessing

---

