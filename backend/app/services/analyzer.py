import os
from dotenv import load_dotenv
from extractor import NLPExtractor
from parser import ParsePDF
from groq import Groq
import time

load_dotenv()


# Once frontend integration, plan to cross reference ATS score with a specic role description prompt

class ResumeLLMAnalyzer():

    client = Groq(
    api_key=os.getenv("GROK_KEY")
)
    
    def __init__(self, llm_client=client, full_text=None, skills=None, titles=None, companies=None, prompt=None):
        self.client = llm_client # initialize the groq client
        self.model = "llama-3.3-70b-versatile" # get LLM model
        self.skills = skills
        self.titles = titles
        self.companies = companies
        self.full_text = full_text
        self.prompt = prompt

    def resume_summary(self):
        skills = self.skills
        jobs = self.titles
        companies = self.companies
        text = self.full_text
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
                        - if no companies are listed look for any obvious companies 
                        the person worked at, analyze the text provided for it, else just ignore it.
                        - keep it brief, use brevity. Max 3 sentences.
                        - Just provide the summary, I don't need an intro to what you provided.
                        - present the summary as "this resume"
                    """
                }, 
                {
                    "role": "user",
                    "content": f"Skills: {skills} Job Titles: {jobs} Companies: {companies} Text: {text}"
                }
            ], 
            model=self.model
        )
        return summary.choices[0].message.content

    def ats_score(self):
        text = self.full_text
        companies = self.companies
        jobs = self.titles
        skills = self.skills
        # replace with user input of job prompt.
        job_prompt = self.prompt

        ats = self.client.chat.completions.create(
            messages= [
                {
                    "role": "system",
                    "content": f"""Please provide an ATS score out of 100. 
                        Base the score off the following:
                            1. Skills of the applicant
                            2. job exerience of the applicant
                            3. the prestige or recognition of the companies they worked at
                            4. {skills}, {companies}, {jobs} in relevence and prestige to {job_prompt}
                        Rules:
                            1. be unbiased nor in favor or not
                            2. make critical connections between the role description and the persons resume
                            3. respond with a number and only a number, I dont want the description of why you chose it.
                    """
                }, 
                {
                    "role": "user",
                    "content": f"Skills: {skills} Job Titles: {jobs} Companies: {companies} Text: {text} Job_description: {job_prompt}"
                }
            ], 
            model=self.model 
        )
        return ats.choices[0].message.content
    
    def ats_description(self):
        text = self.full_text
        companies = self.companies
        jobs = self.titles
        skills = self.skills
        # replace with user input of job prompt.
        job_prompt = self.prompt

        ats_descript = self.client.chat.completions.create(
            messages=[
                {
                "role": "system",
                "content": f"""### TASK:
                    Provide:
                    1. An ATS match score from 0–100  
                    2. A short summary explaining why the score is what it is  
                    3. The top strengths that match the job description  
                    4. The key missing skills or gaps that reduce the score  

                    ### RULES:
                    - Base all scoring ONLY on the job description below.
                    - Do NOT infer skills that are not explicitly stated in the resume.
                    - If the resume hints at something but does not directly state it, do NOT count it.
                    - answer in 2-3 sentences
                """
                },
                {
                    "role": "user",
                    "content": f"Skills: {skills} Job Titles: {jobs} Companies: {companies} Text: {text} Job_description: {job_prompt}"
                }
            ],
            model=self.model
        )
        return ats_descript.choices[0].message.content
    
    def resume_reccomendations(self):
        text = self.full_text
        skills =self.skills
        jobs = self.titles
        companies = self.companies
        job_prompt = self.prompt

        reccomendations = self.client.chat.completions.create(
            messages= [
                {
                    "role": "system", 
                    "content": f"""Provide a list of improvements that will meaningfully strengthen this resume.
                    ### RULES:
                    - Do NOT invent experience, job titles, or achievements.
                    - Only suggest improvements based on what is already present.
                    - Be specific (e.g., “Quantify achievements 
                    - If you believe the user needs additional exerience in certian areas mention that
                    - answer in 2-3 sentences.
                    """
                }, 
                {
                    "role": "user",
                    "content": f"Skills: {skills} Job Titles: {jobs} Companies: {companies} Text: {text} Job_description: {job_prompt}"
                }
            ], 
            model=self.model
        )
        return reccomendations.choices[0].message.content 


if __name__=="__main__":
    pdf_parser = ParsePDF(r"C:\Users\leibn\Downloads\Leib Roth Resume.docx (16) (1).pdf")
    parsed_text = pdf_parser.parse()
    extractor = NLPExtractor(parsed_text)

    skls = extractor.extract_skills()
    jbs = extractor.extract_job_titles()
    cmpns =extractor.extract_job_titles()
    start_time = time.time()
    new_resume = ResumeLLMAnalyzer(full_text=parsed_text, skills=skls, titles=jbs, companies=cmpns, prompt="Software engineering job at google.")
    print(new_resume.resume_summary())
    print(new_resume.ats_score())
    print(new_resume.ats_description())
    print(new_resume.resume_reccomendations())
    end_time = time.time()
    total_load_time = end_time - start_time
    print(f"Model load time was: {total_load_time}")