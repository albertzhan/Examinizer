from scraper import *
from wtforms import Form, StringField, SelectField

from flask import Flask, flash, render_template, request, redirect
from forms import SearchForm
from app import app

import sqlite3

#from urllib import request
@app.route('/', methods=['GET', 'POST'])
def index():
    search = SearchForm(request.form)


    connection = sqlite3.Connection('data.db')
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    courses = cursor.fetchall()

    choices = [(course[0],course[0]) for course in courses]
    print(choices)
    SearchForm.select = SelectField(choices=choices)
    cursor.close()
    connection.close()

    if request.method =='POST':
        return search_results(search)
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
        print("SELECT * FROM %s WHERE term LIKE ? OR txt LIKE ? OR instructor LIKE ? OR type LIKE ?;"%(select_input))
        cursor.execute("SELECT * FROM %s WHERE term LIKE ? OR txt LIKE ? OR instructor LIKE ? OR type LIKE ?;"%(select_input), ['%' + search_input + '%'] * 4)

        results = cursor.fetchall()

    cursor.close()
    connection.close()

    if not results:
        flash('No Exams Found!')
        return redirect('/')

    else:
        # Display Results
        return render_template('results.html', results=results, searched=search_input)


@app.route('/new_course/<topic>/<course>')
def add_class(topic,course):
    my_url = "https://tbp.berkeley.edu/courses/"+topic+"/"+course+"/"
    print(my_url)

    connection = sqlite3.Connection('data.db')
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    courses = cursor.fetchall()

    choices = [course[0] for course in courses]
    if topic+course in choices:
        return "You already have that class"
    else:
        db = sqlite3.Connection("data.db")
        print("CREATE TABLE %s (txt, page, link, exam_or_sol, term, instructor, type);"%(topic+course))
        db.execute("CREATE TABLE %s (txt, page, link, exam_or_sol, term, instructor, type);"%(topic+course))

        exams = get_info(my_url)
        for k in exams:
            k.store_text(db)
        for k in exams:
            k.remove_pdf()
        db.close()

        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=80)
