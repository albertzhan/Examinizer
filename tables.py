from flask_table import Table, Col

class Results(Table):
    instructor = Col('Instructors')
    typee = Col('Type')
    term = Col('Term')
    exam = Col('Exam')
    solution = Col('Solution')

    
