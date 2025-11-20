from fastapi import APIRouter, UploadFile, File, Form
from app.services.parser import ParsePDF
from app.services.extractor import NLPExtractor
from app.services.analyzer import ResumeLLMAnalyzer

router = APIRouter()

@router.post("/analyze")
async def analyze_resume_prompt(job_prompt: str = Form(...) , resume_file: UploadFile = File(...)):
    parsed_resume = ParsePDF.parse_pdf(resume_file)
    extractor = NLPExtractor(resume=parsed_resume)

    skills = extractor.extract_skills()
    titles = extractor.extract_job_titles()
    companies = extractor.extract_companies()
    education = extractor.extract_education()


    analyzer = ResumeLLMAnalyzer(
        full_text= parsed_resume, 
        skills= skills, 
        titles= titles, 
        companies= companies, 
        education= education,
        prompt= job_prompt
)

    summary = analyzer.resume_summary()
    ats_score = analyzer.ats_score()
    ats_description = analyzer.ats_description()
    recomendations = analyzer.resume_reccomendations()
    
    return recomendations