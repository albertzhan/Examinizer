from flask import Flask, flash, render_template, request, redirect
from app import app
from forms import SearchForm
from tables import Results
from exam import *
import sqlite3


@app.route('/', methods=['GET', 'POST'])
def index():
    search = SearchForm(request.form)
    if request.method =='POST':
        return search_results(search)
    return render_template('index.html', form=search)

@app.route('/results')
def search_results(search):
    results = null
    tempdb = sqlite3.Connection('results.db')
    
    search_input = search.data['search']
    
    if search_input:
        tempdb.execute("SELECT * FROM exams WHERE 
        term LIKE (%?%) OR
        type LIKE (%?%) OR
        instructor LIKE (%?%);
        ", search_input)
        results = tempdb.fetchall()
        
    if not results:
        flash('No Exams Found!')
        return redirect('/')
    
    else:
        #Display Results
        return render_template('results.html', results=results)
    



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
