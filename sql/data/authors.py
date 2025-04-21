from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired


class AuthorForm(FlaskForm):
    name = StringField('ФИО автора', validators=[DataRequired()])
    birthday = DateField('День рождения', validators=[DataRequired()])
    submit = SubmitField('Добавить')
