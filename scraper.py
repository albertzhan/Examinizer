from urllib import request
from lxml import html

my_url = "https://tbp.berkeley.edu/courses/cs/61a/"


def get_pdf_info(url_to_search):
    f = request.urlopen(url_to_search).read().strip()
    html_f = f.decode('utf8')
    sbe = html_f.split() #split_by_elem

    elements = []
    for i in range(len(sbe)):
        


get_pdf_info(my_url)
