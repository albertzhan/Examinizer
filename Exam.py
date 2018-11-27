import PyPDF2
import sqlite3
import requests

db = sqlite3.Connection("data.db")
db.execute("CREATE TABLE exams(txt, page, exam_or_sol, link, term, instructor, type);")

class Exam:
    def __init__(self, instructor, term, exam_type, pdf_exam, pdf_solution, course = "CS61a"):
        self.instructor = instructor
        self.term = term
        self.exam_type = exam_type
        self.pdf_exam = pdf_exam #these are links to the pdf
        self.pdf_solution = pdf_solution
        self.course = course

        pdfFileExamObj = requests.get(self.pdf_exam)
        pdfFileSolObj = requests.get(self.pdf_solution)
        self.pdfExamReader = PyPDF2.PdfFileReader(pdfFileExamObj)
        self.pdfSolReader = PyPDF2.PdfFileReader(pdfFileSolObj)
        self.exam_num_pages = self.pdfExamReader.numPages
        self.sol_num_pages = self.pdfSolReader.numPages
        

    def get_text(self, db):
    	page = 0
    	while page < self.exam_num_pages:
    		exam_txt = self.pdfExamReader.getPage(page).extractText()
            db.execute("INSERT INTO exams VALUES (?, ?, ?, ?, ?, ?);" (exam_txt, page, self.pdf_exam, 'exam', self.term, self.instructor, self.exam_type))
    		page += 1

        page = 0
        while page < self.sol_num_pages:
            sol_txt = self.pdfSolReader.getPage(page).extractText()
            db.execute("INSERT INTO exams VALUES (?, ?, ?, ?, ?, ?);" (sol_txt, page, self.pdf_exam, 'sol', self.term, self.instructor, self.exam_type))
            page += 1

        db.commit()

    """
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

"""

