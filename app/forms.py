from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembre-se de mim')
    submit = SubmitField('Entrar')

class RegistrationForm(FlaskForm):
    username = StringField('Nome de usuario', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    password2 = PasswordField(
        'Repita a senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Cadastrar')

def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
        raise ValidationError('Por favor, use um nome de usuario diferente.')

def validate_email(self, email):
    if user is not None:
        user = User.query.filter_by(email=email.data).first()
        raise ValidationError('Por favor, use um e-mail diferente.')
