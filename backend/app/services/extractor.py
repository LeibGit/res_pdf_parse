from parser import ParsePDF
import spacy
from nlp_data.skills import skills
from nlp_data.job_titles import job_titles
from nlp_data.education import get_universities

class NLPExtractor():
    def __init__(self, resume):
        # Load spaCy English model
        self.resume = resume
        self.nlp = spacy.load("en_core_web_sm")
        self.skills = [s.lower() for s in skills]
        self.job_titles = [j.lower() for j in job_titles]
        self.uni = [u.lower() for u in get_universities()]
    
    def extract_skills(self):
        # Extracting all skills from parsed resume text
        found_skills = []
        for skill in self.skills:
            if skill in self.resume:
                found_skills.append(skill)
        return found_skills
            
    def extract_job_titles(self):
        # Extracting all job titles from parsed_text
        found_jobs = []
        for job_title in self.job_titles:
            if job_title in self.resume:
                found_jobs.append(job_title)
        return found_jobs
    
    """
    def extract_years_experience(self, text):
        # add later
        pass 
    """

    def extract_education(self):
        # Extracting all or any universities attended4
        found_unis = []
        for uni in self.uni:
            if uni in self.resume:
                found_unis.append(uni)
        return found_unis

if __name__=="__main__":
    # 1. Parse PDF
    pdf_parser = ParsePDF(r"C:/Users/leibn/Downloads/test_resume.pdf")
    parsed_text = pdf_parser.parse()
    
    #2. Initialize extractor
    extractor = NLPExtractor(parsed_text)

    skills_found = extractor.extract_skills()
    jobs_found = extractor.extract_job_titles()
    education_found = extractor.extract_education()


    print(skills_found)
    print(jobs_found)
    print(education_found)