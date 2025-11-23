import os
from dotenv import load_dotenv
from .extractor import NLPExtractor
from .parser import ParsePDF
from groq import Groq, APIStatusError
from groq import RateLimitError
import time

load_dotenv()

# Once frontend integration, plan to cross reference ATS score with a specic role description prompt

class ResumeLLMAnalyzer():
    client = Groq(
    api_key=os.getenv("GROK_KEY")
)
    
    def __init__(self, llm_client=client, full_text=None, skills=None, titles=None, companies=None, education=None, prompt=None):
        self.client = llm_client # initialize the groq client
        self.model = "llama-3.1-8b-instant" # get LLM model
        self.skills = skills
        self.titles = titles
        self.companies = companies
        self.education = education
        self.full_text = full_text
        self.prompt = prompt

    def resume_summary(self):
        skills = self.skills
        jobs = self.titles
        companies = self.companies
        education = self.education
        text = self.full_text
        job_prompt = self.prompt
        try: 
            summary = self.client.chat.completions.create(
                messages = [
                    {
                        "role": "system", 
                        "content": f"""
                            You are an AI resume analyst. Summarize the candidate based ONLY on the data provided.  
                            Output a **concise summary in 2 or 3 sentences** covering the following:

                            1. Key skills
                            2. Relevant work experience (include roles & companies if listed)
                            3. Professional strengths
                            4. Education highlights

                            Rules:
                            - Do NOT infer or guess information.
                            - Keep tone objective and professional.
                            - Only return the summary, no intro, headings, or special characters.
                            - Present as a single paragraph, starting with "This resume:"
                        """
                    }, 
                    {
                        "role": "user",
                        "content": f"Skills: {skills} Job Titles: {jobs} Companies: {companies} Text: {text} education: {education} Job_description: {job_prompt}"
                    }
                ], 
                model=self.model
            )
            return summary.choices[0].message.content
    
        except RateLimitError as e:
            return {
                "error": "rate_limit", 
                "messafe": str(e)
            }

    def ats_score(self):
        text = self.full_text
        companies = self.companies
        jobs = self.titles
        education = self.education
        skills = self.skills
        # replace with user input of job prompt.
        job_prompt = self.prompt
        try:
            ats = self.client.chat.completions.create(
                messages= [
                    {
                        "role": "system",
                        "content": f"""
                            You are an AI that calculates an ATS score 0 out of 100 for a resume against a specific job description.
                            Evaluate the candidate based ONLY on:
                            - Skills
                            - Work experience (roles, companies)
                            - Education
                            - Alignment with the job description provided

                            Rules:
                            - Return only a number not a string between 0 and 100, no text, no explanation, no whitespace or characters, just a nummber
                            - don't send back NaN
                            - your explindation should be directly to the user, not in the third person. 
                            - Be unbiased and strictly data-driven.
                            - don't ever respond with anything that would be registered as NaN in react frontend.
                            - Ignore anything not explicitly listed in the resume.
                            - deduct necessary points given the text passed as an argument if it is disorganized, misspelled, confusing or poorly structured. Deduct based
                            on how bad the issues are
                        """
                    }, 
                    {
                        "role": "user",
                        "content": f"Skills: {skills} Job Titles: {jobs} Companies: {companies} Text: {text} education: {education} Job_description: {job_prompt}"
                    }
                ], 
                model=self.model 
            )
            return ats.choices[0].message.content
        
        except RateLimitError as e:
            return {
                "error": "rate_limit", 
                "messafe": str(e)
            }
    
    def ats_description(self):
        text = self.full_text
        companies = self.companies
        jobs = self.titles
        education = self.education
        skills = self.skills
        # replace with user input of job prompt.
        job_prompt = self.prompt

        try:
            ats_description = self.client.chat.completions.create(
                messages=[
                    {
                    "role": "system",
                    "content": f"""
                        You are an AI that explains why a resume received a particular ATS score.
                        Output a short explanation in 2 or 3 sentences including:
                        1. Top strengths that match the job description
                        2. Key missing skills, experience, or education gaps
                        Rules:
                        - Base ONLY on the job description and resume.
                        - Do NOT infer unstated skills or experience.
                        - Do NOT mention the numeric ATS score (already provided separately).
                        - Provide a clean, readable paragraph with no bullet points or special characters.
                       
                    """
                    },
                    {
                        "role": "user",
                        "content": f"Skills: {skills} Job Titles: {jobs} Companies: {companies} Text: {text} Education: {education} Job_description: {job_prompt}"
                    }
                ],
                model=self.model
            )
            return ats_description.choices[0].message.content
        
        except RateLimitError as e:
            return {
                "error": "rate_limit", 
                "messafe": str(e)
            }
    
    def resume_recomendations(self):
        text = self.full_text
        skills =self.skills
        jobs = self.titles
        education = self.education
        companies = self.companies
        job_prompt = self.prompt
        
        try:
            recomendations = self.client.chat.completions.create(
                messages= [
                    {
                        "role": "system", 
                        "content": f"""
                            You are an AI resume advisor. Provide a list of actionable improvements to strengthen this resume.  
                            Rules:
                            - Suggest only based on information present in the resume.
                            - Be specific, e.g., "Quantify achievements", "Gain experience in [specific area]"
                            - Include any missing skills, certifications, or education that are relevant to the job description.                    
                            - Do NOT invent job titles, companies, or achievements.
                            - Keep each suggestion to 1 or 2 sentences.
                            - No extra text, headers, or special characters.
                            - keep bullet points extremely short and don't number them. Stricly make a clear sentence or two. 
                            - do not make an intro to your points, only send back the points
                            - only send back the top 5 most important points
                            don't add any unecessary statements. 
                        """
                    }, 
                    {
                        "role": "user",
                        "content": f"Skills: {skills} Job Titles: {jobs} Companies: {companies} Text: {text} Education: {education} Job_description: {job_prompt}"
                    }
                ], 
                model=self.model
            )
            return recomendations.choices[0].message.content 
    
        except RateLimitError as e:
            return {
                "error": "rate_limit", 
                "messafe": str(e)
            }