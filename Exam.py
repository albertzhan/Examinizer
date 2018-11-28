import PyPDF2
import sqlite3
import requests


class Exam:
    def __init__(self, instructor, term, exam_type, pdf_exam, pdf_solution, course = "CS61a"):
        self.instructor = instructor
        self.term = term
        self.exam_type = exam_type
        self.pdf_exam = pdf_exam
        self.pdf_solution = pdf_solution
        self.exam_source = "./tmp/"+''.join(self.term.split(" ")) + 'exam.pdf'
        self.sol_source = "./tmp/"+''.join(self.term.split(" ")) + 'sol.pdf'
        self.course = course

        if self.pdf_exam != "https://tbp.berkeley.edu":
            pdfexamres = requests.get(self.pdf_exam, stream=True)

            with open(self.exam_source, 'wb') as fd:
                fd.write(pdfexamres.content)
            fd.close()


        if self.pdf_solution != "https://tbp.berkeley.edu":
            pdfsolres = requests.get(self.pdf_solution)
            with open(self.sol_source,'wb') as fd:
                fd.write(pdfsolres.content)
            fd.close()

    def store_text(self, db):
        if self.pdf_exam != "https://tbp.berkeley.edu":
            page = 0
            pdfExamReader = PyPDF2.PdfFileReader(self.exam_source)
            exam_num_pages = pdfExamReader.getNumPages()
            while page < exam_num_pages:
                exam_txt = pdfExamReader.getPage(page).extractText()
                db.execute("INSERT INTO exams VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (exam_txt, page, self.pdf_exam, 'exam', self.term, self.instructor, self.exam_type, self.course))
                page += 1

        if self.pdf_solution != "https://tbp.berkeley.edu":
            page = 0
            pdfSolReader = PyPDF2.PdfFileReader(self.sol_source)
            sol_num_pages = pdfSolReader.getNumPages()
            while page < sol_num_pages:
                sol_txt = pdfSolReader.getPage(page).extractText()
                db.execute("INSERT INTO exams VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (sol_txt, page, self.pdf_exam, 'sol', self.term, self.instructor, self.exam_type, self.course))
                page += 1

        db.commit()



