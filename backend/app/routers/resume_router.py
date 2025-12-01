from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from services.parser import ParsePDF
from services.extractor import NLPExtractor
from services.analyzer import ResumeLLMAnalyzer
import logging
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/resume")

@router.post("/analyze")
async def analyze_resume_prompt(job_prompt: str = Form(...), resume_file: UploadFile = File(...)):
    try:
        logger.info("=== STARTING RESUME ANALYSIS ===")
        logger.info(f"File: {resume_file.filename}, Size: {resume_file.size}")
        logger.info(f"Job prompt length: {len(job_prompt)}")
        
        # Parse PDF from uploaded file
        logger.info("Step 1: Parsing PDF...")
        parsed_resume = ParsePDF.parse_pdf(resume_file)
        logger.info(f"Parsed {len(parsed_resume)} characters")
        
        # Extract structured data
        logger.info("Step 2: Extracting data...")
        extractor = NLPExtractor(resume=parsed_resume)
        
        logger.info("Extracting skills...")
        skills = extractor.extract_skills()
        logger.info(f"Found {len(skills)} skills")
        
        logger.info("Extracting job titles...")
        titles = extractor.extract_job_titles()
        logger.info(f"Found {len(titles)} titles")
        
        logger.info("Extracting companies...")
        companies = extractor.extract_companies()
        logger.info(f"Found {len(companies)} companies")
        
        logger.info("Extracting education...")
        education = extractor.extract_education()
        logger.info(f"Found {len(education)} education entries")

        # Analyze with LLM
        logger.info("Step 3: Analyzing with LLM (single call)...")
        analyzer = ResumeLLMAnalyzer(
            full_text=parsed_resume, 
            skills=skills, 
            titles=titles, 
            companies=companies, 
            education=education,
            prompt=job_prompt
        )

        logger.info("Calling unified analyze_all...")
        llm_result = analyzer.analyze_all()

        # If the unified call returned an error object, surface it cleanly
        if isinstance(llm_result, dict) and "error" in llm_result:
            logger.error(f"LLM error: {llm_result}")
            raise HTTPException(status_code=500, detail=llm_result)

        summary = llm_result.get("summary")
        ats_score = llm_result.get("ats_score")
        ats_description = llm_result.get("ats_description")
        recomendations = llm_result.get("recomendations")
        
        logger.info("=== ANALYSIS COMPLETE ===")
        
        return {
            "summary": summary, 
            "ats_score": ats_score, 
            "ats_description": ats_description, 
            "recomendations": recomendations,
            "education": education
        }
    except ValueError as e:
        logger.error(f"ValueError: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"CRITICAL ERROR: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")