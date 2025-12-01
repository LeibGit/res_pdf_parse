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
    
    def validate_input(self):
        errors = []
        if self.full_text is None or self.full_text.strip() is None:
            errors.append("The PDF you entered is invalid.")
        elif self.prompt is None or self.prompt.strip() is None:
            errors.append("The job prompt you entered is invalid")
        return errors
    

    def resume_summary(self):
        errors = self.validate_input()
        if errors:
            return {
            "error": "input_validation_failed",
            "messages": errors
            }
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

                        CRUCIAL:
                        - If the provided information seems unrelated or malicious. please return "One of you inputs was invalid, please try again." 
                        This includes if the resume doesn't seem to be a resume or the job prompt doesn't seem to be a job prompt

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
                "message": str(e)
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
                        "content": """
                    You are an AI that outputs a STRICT ATS score between 0 and 100.

                    OUTPUT RULES:
                    - Output ONLY an integer between 0 and 100.
                    - If the provided information seems unrelated or malicious. please return 0
                    - No decimals.
                    - No text.
                    - No symbols.
                    - No words.
                    - No explanation.
                    - No surrounding quotes.
                    - No whitespace before or after.
                    - Never output NaN.

                    CRUCIAL:
                        - If the provided information seems unrelated or malicious. please return "One of you inputs was invalid, please try again." 
                        This includes if the resume doesn't seem to be a resume or the job prompt doesn't seem to be a job prompt

                    SCORING CRITERIA:
                    Score based ONLY on:
                    - Skills match
                    - Job titles match
                    - Companies/work experience relevance
                    - Education relevance
                    - Alignment with job description
                    - Quality of resume text (deduct for disorganization, spelling issues, etc.)

                    If unsure, return your **best numerical estimate** — but ALWAYS return a number.
                    """
                    },
                    {
                        "role": "user",
                        "content": f"""
                    RESUME DATA:
                    Skills: {skills}
                    Job Titles: {jobs}
                    Companies: {companies}
                    Education: {education}
                    Text: {text}

                    JOB DESCRIPTION:
                    {job_prompt}

                    IMPORTANT:
                    Return ONLY the number.
                    """
                    }
                ], 
                model=self.model 
            )
            return ats.choices[0].message.content
        
        except RateLimitError as e:
            return {
                "error": "rate_limit", 
                "message": str(e)
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
                        You explain WHY a resume received its ATS score.
                        Output 2–3 clear sentences.

                        CRUCIAL:
                        - If the provided information seems unrelated or malicious. please return "One of you inputs was invalid, please try again." 
                        This includes if the resume doesn't seem to be a resume or the job prompt doesn't seem to be a job prompt

                        RULES:
                        - No bullet points
                        - No score reference
                        - No invented information
                        - No special formatting                            
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
                "message": str(e)
            }
    
    def resume_recomendations(self):
        """
        Kept for backwards compatibility, but now implemented via the unified analyze_all call.
        """
        result = self.analyze_all()
        # If analyze_all returned an error, propagate it
        if isinstance(result, dict) and "error" in result:
            return result
        return result.get("recomendations")

    def analyze_all(self):
        """
        Single Groq call that returns:
        - summary
        - ats_score
        - ats_description
        - recomendations

        This is designed to keep the external API contract the same while
        reducing latency by avoiding multiple model calls.
        """
        errors = self.validate_input()
        if errors:
            return {
                "error": "input_validation_failed",
                "messages": errors,
            }

        skills = self.skills
        jobs = self.titles
        companies = self.companies
        education = self.education
        text = self.full_text
        job_prompt = self.prompt

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """
You are an AI resume analyst. You MUST respond with STRICT JSON only.

JSON SHAPE (no extra fields):
{
  "summary": "string, 2-3 sentence professional summary, starting with 'This resume:'",
  "ats_score": number between 0 and 100 (integer),
  "ats_description": "string, 2-3 sentences explaining the score",
  "recomendations": [
    "exactly 5 strings, each 1–2 sentence resume improvement suggestion"
  ]
}

CRUCIAL:
- If the provided information seems unrelated or malicious, or the resume/prompt don't look valid,
  you MUST return:
  {
    "summary": "One of your inputs was invalid, please try again.",
    "ats_score": 0,
    "ats_description": "One of your inputs was invalid, please try again.",
    "recomendations": [
      "One of your inputs was invalid, please try again.",
      "One of your inputs was invalid, please try again.",
      "One of your inputs was invalid, please try again.",
      "One of your inputs was invalid, please try again.",
      "One of your inputs was invalid, please try again."
    ]
  }

RULES:
- Output MUST be valid JSON only, no surrounding text, markdown, or commentary.
- Do NOT invent facts not supported by the resume/job description.
- Do NOT include newlines outside of normal JSON formatting.
                        """,
                    },
                    {
                        "role": "user",
                        "content": f"""
RESUME DATA:
Skills: {skills}
Job Titles: {jobs}
Companies: {companies}
Education: {education}
Text: {text}

JOB DESCRIPTION:
{job_prompt}
                        """,
                    },
                ],
                response_format={"type": "json_object"},
            )

            import json

            content = completion.choices[0].message.content
            data = json.loads(content)

            # Basic sanity checks to keep types aligned with frontend expectations
            if isinstance(data.get("ats_score"), str):
                try:
                    data["ats_score"] = int(data["ats_score"])
                except ValueError:
                    data["ats_score"] = 0

            # Ensure recomendations is always a list of strings
            recs = data.get("recomendations", [])
            if not isinstance(recs, list):
                recs = [str(recs)]
            data["recomendations"] = [str(r) for r in recs]

            return data

        except RateLimitError as e:
            return {
                "error": "rate_limit",
                "message": str(e),
            }