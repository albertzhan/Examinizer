from flask import Flask, flash, render_template, request, redirect
from app import app
from forms import SearchForm

@app.route('/', methods=['GET'])
def index():
    search = SearchForm(request.form)
    if request.method =='POST':
        return search_results(search)
    return render_template('index.html', form=search)

@app.route('/results')
def search_results(search):
    results = []

    search_string=search.data['search']

    if search.data['search'] == '':
        qry = 
        results = qry.all()

    if not results:
        flash('No Exams Found!')
        return redirect('/')

    else:
        table = Results(results)
        table.border = True
        return render_template('results.html', results=results)
    



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
