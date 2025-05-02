from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FileField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    title = StringField("Название", validators=[DataRequired()])
    year = IntegerField("Год написания", validators=[DataRequired()])
    description = StringField("Описание")
    authors = SelectMultipleField("Авторы", coerce=int)
    genres = SelectMultipleField("Жанры", coerce=int)
    file = FileField("Файл", validators=[DataRequired()])
    submit = SubmitField('Добавить')
