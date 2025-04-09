from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_repeat = PasswordField("Повторите пароль", validators=[DataRequired(), EqualTo('password', message="Пароли должны совпадать")])
    nickname = StringField("Ник", validators=[DataRequired()])
    submit = SubmitField("Зарегистрироваться")
