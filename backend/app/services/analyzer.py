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
        jobs = self.titles
        companies = self.companies
    
        summary = self.client.chat.completions.create(
            messages = [
                {
                    "role": "system", 
                    "content": f"""You are an analytical AI that summarizes resumes using only the information provided.
                        Write a concise **3-sentence factual summary** describing this persons:
                        1. Key skills
                        2. Relevant experience
                        3. Professional strengths

                        Rules:
                        - **Use only information explicitly present in the resume.**
                        - **No assumptions, guesses, or inferred details.**
                        - Keep the tone objective, professional, and neutral.
                    """
                }, 
                {
                    "role": "user",
                    "content": f"Skills: {skills} Job Titles: {jobs} Companies: {companies}"
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