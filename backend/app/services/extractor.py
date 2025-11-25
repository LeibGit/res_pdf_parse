from .parser import ParsePDF
from .nlp_data.skills import skills
from .nlp_data.job_titles import job_titles
from .nlp_data.education import get_universities
import re

class NLPExtractor():
    def __init__(self, resume):
        self.resume = resume
        self.resume_clean = re.sub(r"\s+", " ", resume.lower())
        
        # Import your data lists
        from .nlp_data.skills import skills
        from .nlp_data.job_titles import job_titles
        from .nlp_data.education import get_universities
        
        self.skills = [s.lower() for s in skills]
        self.job_titles = [j.lower() for j in job_titles]
        self.uni = [u.lower() for u in get_universities()]
    
    def extract_skills(self):
        found_skills = []
        for skill in self.skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, self.resume_clean):
                found_skills.append(skill)
        return found_skills
            
    def extract_job_titles(self):
        found_jobs = []
        for job_title in self.job_titles:
            pattern = r'\b' + re.escape(job_title) + r'\b'
            if re.search(pattern, self.resume_clean):
                found_jobs.append(job_title)
        return found_jobs
    
    def extract_education(self):
        found_unis = []
        for uni in self.uni:
            pattern = r'\b' + uni + r'\b'
            if re.search(pattern, self.resume_clean):
                found_unis.append(uni)
        return found_unis
    
    def extract_companies(self):
        """Extract company names using regex patterns instead of spaCy"""
        found_companies = []
        company_suffixes = ["inc", "llc", "corp", "ltd", "co", "company", "firm", "agency", "partnership", "corporation", "limited"]
        
        # Pattern to find capitalized words followed by company suffixes
        # Matches things like "Google Inc", "Microsoft Corporation", etc.
        patterns = [
            r'\b([A-Z][a-zA-Z0-9\s&]+?)\s+(?:Inc\.?|LLC|Corp\.?|Ltd\.?|Corporation|Limited|Company)\b',
            r'\b([A-Z][a-zA-Z0-9]+)\s+(?:Inc\.?|LLC|Corp\.?|Ltd\.?)\b',
            # Match standalone capitalized company names (2+ words starting with capitals)
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, self.resume)
            for match in matches:
                company = match.group(1).strip()
                
                # Filter out common false positives
                if len(company) < 3:
                    continue
                if company.lower() in ['experience', 'education', 'skills', 'summary', 'objective']:
                    continue
                if company not in found_companies:
                    found_companies.append(company)
        
        # Deduplicate and clean
        return list(set(found_companies))

    def extract_years_experience(self, text):
        """Extract years of experience from text"""
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?experience',
            r'experience[:\s]+(\d+)\+?\s*(?:years?|yrs?)',
            r'(\d+)\+?\s*(?:years?|yrs?)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return int(match.group(1))
        return None