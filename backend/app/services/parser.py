from pypdf import PdfReader
from docx import Document
import re

class ParsePDF():
    def __init__(self, pdf):
        self.pdf = pdf
    
    def check_file_type():
        pass


    def read_pdf(self):
        reader = PdfReader(self.pdf)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    
    def read_docx(self):
        pass

if __name__=="__main__":
    test_one = ParsePDF(r"C:/Users/leibn/Downloads/Resume.pdf")
    print(test_one.read_pdf())