from pypdf import PdfReader
from docx import Document

class ParsePDF():
    def __init__(self, file: str):
        self.file = file

    def parse(self):
        if self.file.endswith(".pdf"):
            return self.parse_pdf()
        else:
            raise ValueError("Unsupported file type. Please submit a pdf.")
        
    def parse_pdf(self):
        reader = PdfReader(self.file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
