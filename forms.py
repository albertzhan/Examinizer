from wtforms import Form, StringField, SelectField
import sqlite3



class SearchForm(Form):
    connection = sqlite3.Connection('data.db')
    cursor = connection.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    courses = cursor.fetchall()
    
    choices = [(course, course) for course in courses]
    select = SelectField('Search Through Class:', choices=choices)
    search = StringField('')
