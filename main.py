from scraper import *

from flask import Flask, flash, render_template, request, redirect
from forms import SearchForm
from app import app
import sqlite3
#from urllib import request
@app.route('/', methods=['GET', 'POST'], endpoint='index')
def index():
    search = SearchForm(request.form)
    if request.method =='POST':
        return search_results(search)
    print("got a guy looking for exams")
    return render_template('index.html', form=search)

@app.route('/results', endpoint='search_results')
def search_results(search):
    results = []

    connection = sqlite3.Connection('data.db')
    cursor = connection.cursor()

    # Retrieve the form input
    select_input = search.data['select']
    search_input = search.data['search']


    # Query through importeddata using form input and store in results
    if search_input:
        print("SELECT * FROM ? WHERE term LIKE ? OR txt LIKE ? OR instructor LIKE ? OR type LIKE ?;", [select_input]+['%' + search_input + '%'] * 4)

        cursor.execute("SELECT * FROM ? WHERE term LIKE ? OR txt LIKE ? OR instructor LIKE ? OR type LIKE ?;", [select_input]+['%' + search_input + '%'] * 4)

        results = cursor.fetchall()



    if not results:
        flash('No Exams Found!')
        return redirect('/')

    else:
        # Display Results
        return render_template('results.html', results=results)

@app.route('/new_course', endpoint='new_class')
def new_class():
    return render_template('new_course.html')

@app.route('/new_course/<topic>/<course>')
def add_class(topic,course):
    my_url = "https://tbp.berkeley.edu/courses/"+topic+"/"+course+"/"
    print(my_url)
    db = sqlite3.Connection("data.db")
    print("CREATE TABLE %s (txt, page, link, exam_or_sol, term, instructor, type);"%(topic+course))
    db.execute("CREATE TABLE %s (txt, page, link, exam_or_sol, term, instructor, type);"%(topic+course))

    for k in get_info(my_url):
        k.store_text(db)
    db.close()
    return render_template('index.html', form=search)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)
