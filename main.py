from flask import Flask, flash, render_template, request, redirect
from forms import SearchForm
from app import app
import sqlite3

from scraper import *

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

        cursor.execute("SELECT * FROM exams WHERE term LIKE ? OR txt LIKE ? OR instructor LIKE ? OR type LIKE ?;", ['%' + search_input + '%'] * 4)

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
