from pypdf import PdfReader
from docx import Document
import re

class ParsePDF():
    def __init__(self, file: str):
        self.file = file

    def parse(self):
        if self.file.endswith(".pdf"):
            return self.parse_pdf
        else:
            raise ValueError("Unsupported file type. Please submit a pdf.")
        
    def parse_pdf(self):
        reader = PdfReader(self.file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

if __name__=="__main__":
    # Test cases
    test_one = ParsePDF(r"C:\Users\leibn\Downloads\Resume_Template.docx")
    print(test_one.parse())