from wtforms import Form, StringField, SelectField




class SearchForm(Form):
    connection = sqlite3.Connection('data.db')
    cursor = connection.cursor()

    cursor.execute(".tables")
    tables = cursor.fetchall()
    
    choices = [('cs61a', 'cs61a'), ('cs70', 'cs70')]
    select = SelectField('Search Through Class:', choices=choices)
    search = StringField('')
