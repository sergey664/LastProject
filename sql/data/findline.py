from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Optional


class FindForm(FlaskForm):
    string = StringField('Поиск книг', validators=[Optional()])
    submit = SubmitField('Искать')
