from wtforms import Form, StringField, SelectField

class SearchForm(Form):
    choices = [('CS61a', 'CS61a'), ('CS70', 'CS70')]
    select = SelectField('Search Through Class:', choices=choices)
    search = StringField('')
