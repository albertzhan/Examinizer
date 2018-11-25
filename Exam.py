import PyPDF2
import requests

class Exam:
    def __init__(self, instructor, term, exam_type, pdf_exam, pdf_solution, course = "CS61a"):
        self.instructor = instructor
        self.term = term
        self.exam_type = exam_type
        self.pdf_exam = pdf_exam #these are links to the pdf
        self.pdf_solution = pdf_solution
        self.course = course
        self.content = ''

        pdfFileObj = requests.get(self.pdf_exam)
        self.pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        self.num_pages = self.pdfReader.numPages
        self.get_text()


    def get_text(self):
    	self.page1_text = self.pdfReader.getPage(0).extractText()
    	page = 1
    	while page < num_pages:
    		self.content += self.pdfReader.getPage(page).extractText()
    		page += 1

    def search_string(self, str):
    	return str in self.content