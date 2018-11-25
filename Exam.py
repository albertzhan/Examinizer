import PyPDF2
import sqlite3
import requests

db = sqlite3.Connection("pdfRead")
db.execute("CREATE TABLE exams(txt, link, term, instructor, type;")

class Exam:
    def __init__(self, instructor, term, exam_type, pdf_exam, pdf_solution, course = "CS61a"):
        self.instructor = instructor
        self.term = term
        self.exam_type = exam_type
        self.pdf_exam = pdf_exam #these are links to the pdf
        self.pdf_solution = pdf_solution
        self.course = course
        self.text = []

        pdfFileObj = requests.get(self.pdf_exam)
        self.pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        self.num_pages = self.pdfReader.numPages
        self.get_text()

        db.execute("INSERT INTO exams SELECT self.text, self.pdf_exam, self.term, self.instructor, self.exam_type;")
        db.commit()

    def get_text(self):
    	page = 0
    	while page < self.num_pages:
    		self.text[page] = self.pdfReader.getPage(page).extractText()
    		page += 1

    def search_string(self, str):
    	page = 0
        containing_pages = ''
        while page < self.num_pages:
            if str in self.text[page]:
                containing_pages += ' {},'.format(page)
            page += 1
        if not containing_pages:
            return '{} not found'.format(str)
        return 'Page' + containing_pages[:-1]


