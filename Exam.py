class Exam:
    def __init__(self, link, year, term, pdf_exam, pdf_solution, instructor, course = "CS61a"):
        self.link = link
        self.year = year
        self.term = term
        self.pdf_exam = pdf_exam
        self.pdf_solution = pdf_solution
        self.instructor = instructor
        self.course = course
