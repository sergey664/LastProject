from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FileField, SubmitField
from wtforms.validators import DataRequired


class AuthorForm(FlaskForm):
    title = StringField("Название", validators=[DataRequired()])
    year = IntegerField("Год написания", validators=[DataRequired()])
    description = StringField("Описание")
    file = FileField("Файл", validators=[DataRequired()])
    submit = SubmitField('Добавить')
