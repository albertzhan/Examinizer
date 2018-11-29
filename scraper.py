from urllib import request
from lxml import html

from exam import *
#this is really only necessary because I am bad at regex =(
def get_info(url_to_search):
    f = request.urlopen(url_to_search).read().strip()
    html_f = f.decode('utf8')
    sbe = html_f.split() #split_by_elem

    elements = []
    for i in range(len(sbe)):
        to_use = True
        if "<tr>" in sbe[i]:
            ins = ""
            term = ""
            exam_type = ""
            exam = "https://tbp.berkeley.edu"
            sols = "https://tbp.berkeley.edu"
            while i < len(sbe) and "</tr>" not in sbe[i] :

                if "instructor" in sbe[i]:
                    start = sbe[i].find(">")+1
                    end = sbe[i].find("<")
                    ins = sbe[i][start:end]

                if "Midterm" in sbe[i]:
                    exam_type = "Midterm " + sbe[i+1][0]
                elif "Exam" in sbe[i]:
                    exam_type = "Exam"

                if "Fall" in sbe[i]:
                    term = "Fall " + sbe[i+1][0: sbe[i+1].find("<")]
                elif "Spring" in sbe[i]:
                    term = "Spring " + sbe[i+1][0: sbe[i+1].find("<")]
                elif "Summer" in sbe[i]:
                    term = "Summer " + sbe[i+1][0: sbe[i+1].find("<")]


                if "download" in sbe[i] and "href" in sbe[i]:
                    #print(sbe[i],sbe[i+4])
                    tmp = sbe[i][ sbe[i].find('"')+1  : sbe[i][sbe[i].find('"')+1:].find('"') + sbe[i].find('"')+1 ]
                    if "Download" in sbe[i+4]:
                        to_use = False
                        break
                    elif "Exam" in sbe[i+4]:
                        exam += tmp
                    elif "Solution" in sbe[i+4]:
                        sols += tmp
                        break
                i += 1
            #some code here to deal with table rows that are not
            if to_use:
                #print(ins, term, exam_type, exam, sols)
                elements.append(Exam(ins, term, exam_type, exam, sols))
    return elements



my_url = "https://tbp.berkeley.edu/courses/cs/61a/"
db = sqlite3.Connection("data.db")
db.execute("CREATE TABLE exams(txt, page, link, exam_or_sol, term, instructor, type, course);")

for k in get_info(my_url):
    k.store_text(db)
