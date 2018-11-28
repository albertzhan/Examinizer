import PyPDF2
import sqlite3
import requests

db = sqlite3.Connection("data.db")
#db.execute("CREATE TABLE exams(txt, page, exam_or_sol, link, term, instructor, type);")

class Exam:
    def __init__(self, instructor, term, exam_type, pdf_exam, pdf_solution, course = "CS61a"):
        self.instructor = instructor
        self.term = term
        self.exam_type = exam_type
        self.pdf_exam = pdf_exam #these are links to the pdf
        self.pdf_solution = pdf_solution
        self.exam_source = "./tmp/"+''.join(self.term.split(" ")) + 'exam.pdf'
        self.sol_source = "./tmp/"+''.join(self.term.split(" ")) + 'sol.pdf'
        self.course = course

        if self.pdf_exam != "https://tbp.berkeley.edu":
            pdfexamres = requests.get(self.pdf_exam, stream=True)

            #print(pdfexam.content)
            with open(self.exam_source, 'wb') as fd:
                fd.write(pdfexamres.content)
            fd.close()


        if self.pdf_solution != "https://tbp.berkeley.edu":
            pdfsolres = requests.get(self.pdf_solution)
            with open(self.sol_source,'wb') as fd:
                fd.write(pdfsolres.content)
            fd.close()

    def store_text(self, db):
        page = 0
        if self.pdf_exam != "https://tbp.berkeley.edu":
            pdfExamReader = PyPDF2.PdfFileReader(self.exam_source)
            #exam_num_pages = pdfExamReader.num_pages
            for i in range (3): #TODO: @Andy fix this, i don't remember how this works
                exam_txt = pdfExamReader.getPage(page).extractText()
                print("INSERT INTO exams VALUES {0} {1} {2} {3} {4} {5} {6};".format(exam_txt, page, self.pdf_exam, 'exam', self.term, self.instructor, self.exam_type))
                #db.execute("INSERT INTO exams VALUES {}, {}, {}, {}, {}, {};".format(exam_txt, page, self.pdf_exam, 'exam', self.term, self.instructor, self.exam_type))
                page += 1
        if self.pdf_solution != "https://tbp.berkeley.edu":
            page = 0
            pdfSolReader = PyPDF2.PdfFileReader(self.sol_source)
            #sol_num_pages = pdfSolReader.num_pages
            for i in range (3):
                sol_txt = pdfSolReader.getPage(page).extractText()
                print("INSERT INTO exams VALUES {0} {1} {2} {3} {4} {5} {6};".format(sol_txt, page, self.pdf_exam, 'sol', self.term, self.instructor, self.exam_type))
                #db.execute("INSERT INTO exams VALUES {} {} {} {} {} {};".format(sol_txt, page, self.pdf_exam, 'sol', self.term, self.instructor, self.exam_type))
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
