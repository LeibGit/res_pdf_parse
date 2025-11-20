import sys
from pathlib import Path

# Add the backend directory to Python path to allow imports
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI
from app.services.parser import ParsePDF
from app.services.extractor import NLPExtractor
from app.services.analyzer import ResumeLLMAnalyzer

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "world"}