# 🧠 Resume AI — Automated Resume Scoring & Enhancement Tool

Resume AI is a lightweight machine-learning–powered tool designed to **analyze résumés, score them for ATS compatibility, and provide actionable suggestions for improvement**.  
It uses NLP techniques to evaluate clarity, keyword alignment, formatting, and overall job-fit strength.

---

## 🚀 Features

- **ATS Compatibility Scoring**  
  Evaluates formatting, keyword usage, structure, and readability.

- **Keyword Extraction & Matching**  
  Compares résumé content to a job description and highlights missing role-critical keywords.

- **Smart Suggestions Engine**  
  Provides actionable recommendations to improve phrasing, clarity, quantification, and impact.

- **Section Quality Analysis**  
  Assesses Experience, Skills, Education, and Projects for strength and relevance.

- **PDF / Text Parsing Support**  
  Upload a PDF or input raw text — AI parses and analyzes both.

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **FastAPI** — backend API  
- **OpenAI API** — NLP evaluation  
- **SpaCy** — keyword extraction and parsing  
- **PyPDF2** / **pdfplumber** — PDF text extraction  
- **React / Next.js** (optional UI)

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/resume-ai.git
cd resume-ai

pip install -r requirements.txt
