from .parser import ParsePDF
import spacy
from .nlp_data.skills import skills
from .nlp_data.job_titles import job_titles
from .nlp_data.education import get_universities
import re

# Load spaCy model once at module level (shared across instances)
nlp = spacy.load("en_core_web_sm")

class NLPExtractor():
    def __init__(self, resume):
        self.resume = resume
        self.resume_clean = re.sub(r"\s+", " ", resume.lower())
        # Use the global nlp instance instead of loading again
        self.nlp = nlp
        self.skills = [s.lower() for s in skills]
        self.job_titles = [j.lower() for j in job_titles]
        self.uni = [u.lower() for u in get_universities()]
    
    def extract_skills(self):
        # Extracting all skills from parsed resume text
        found_skills = []
        for skill in self.skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, self.resume_clean):
                found_skills.append(skill)
        return found_skills
            
    def extract_job_titles(self):
        # Extracting all job titles from parsed_text
        found_jobs = []
        for job_title in self.job_titles:
            pattern = r'\b' + re.escape(job_title) + r'\b'
            if re.search(pattern, self.resume_clean):
                found_jobs.append(job_title)
        return found_jobs
    
    def extract_education(self):
        # Extracting all or any universities attended
        found_unis = []
        for uni in self.uni:
            pattern = r'\b' + uni + r'\b'
            if re.search(pattern, self.resume_clean):
                found_unis.append(uni)
        return found_unis
    
    def extract_companies(self):
        found_companies = []
        company_suffixes = ["inc", "llc", "corp", "ltd", "co", "company", "firm", "agency", "partnership"]
        cleaned_text = re.sub(r'\s+', ' ', self.resume)
        doc = self.nlp(cleaned_text)
        for ent in doc.ents:
            if ent.label_ == "ORG":
                name = ent.text.strip()
                if name in found_companies:
                    continue
                elif any(name.lower().endswith(suf) for suf in company_suffixes) and name.lower() not in company_suffixes:
                    found_companies.append(name)
        return found_companies

    def extract_years_experience(self, text):
    # add later
        pass 