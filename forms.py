from wtforms import Form, StringField, SelectField
import sqlite3



class SearchForm(Form):
    connection = sqlite3.Connection('data.db')
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    courses = cursor.fetchall()

    choices = [(course[0],course[0]) for course in courses]
    print(choices)
    print("didn't print")
    select = SelectField('Search Through Class:', choices=choices)
    search = StringField('')
