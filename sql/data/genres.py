from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class GenreForm(FlaskForm):
    name = StringField('Название жанра', validators=[DataRequired()])
    submit = SubmitField('Добавить')