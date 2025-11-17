import os
from dotenv import load_dotenv
from extractor import NLPExtractor
from parser import ParsePDF
from groq import Groq

load_dotenv()

"""

llm_client = client.chat.completions.create(
    messages=[
        {
            "role": "system", 
            "content": You are an assisant that judges user resume's based on a job description 
            they are going for.You are extremely thoughtfull, creative, and insightfull.,
        }
    ],
    model="llama-3.3-70b-versatile"
)
"""
class ResumeLLMAnalyzer():

    client = Groq(
    api_key=os.getenv("GROK_KEY")
)
    
    def __init__(self, llm_client=client, skills=None, titles=None, companies=None):
        self.client = llm_client # initialize the groq client
        self.model = "llama-3.3-70b-versatile" # get LLM model
        self.skills = skills
        self.titles = titles
        self.companies = companies

    def resume_summary(self):
        skills = self.skills
        summary = self.client.chat.completions.create(
            messages = [
                {
                    "role": "system", 
                    "content": f"""You are a thorough AI agent that analyzes resumes. 
                    Please provide a breif 4 sentence summary of this persons skills."""
                }, 
                {
                    "role": "user",
                    "content": f"{skills}"
                }
            ], 
            model=self.model
        )
        return summary.choices[0].message.content

    def ats_score(self):
        pass

if __name__=="__main__":
    pdf_parser = ParsePDF(r"C:\Users\leibn\Downloads\Leib Roth Resume.docx (16) (1).pdf")
    parsed_text = pdf_parser.parse()
    extractor = NLPExtractor(parsed_text)

    skls = extractor.extract_skills()
    jbs = extractor.extract_job_titles()
    cmpns =extractor.extract_job_titles()

    new_resume = ResumeLLMAnalyzer(skills=skls, titles=jbs, companies=cmpns)
    print(new_resume.resume_summary())