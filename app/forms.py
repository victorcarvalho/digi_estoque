from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.fields.html5 import DateField
from datetime import date
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


class ItemAddForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    quantity = FloatField('Quantidade', validators=[DataRequired()])
    unit = SelectField('Unidade', choices = [('UND', 'UND'), ('CX', 'CX')])
    room = SelectField('Local', choices = [('Container 1 (Mec)', 'Container 1 (Mec)'),
        ('Container 2 (Elet)', 'Container 2 (Elet)')])
    submit = SubmitField('Cadastrar')


class ItemEditForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    quantity = FloatField('Quantidade', validators=[DataRequired()])
    unit = SelectField('Unidade', choices = [('UND', 'UND'), ('CX', 'CX')])
    room = SelectField('Local', choices = [('Container 1 (Mec)', 'Container 1 (Mec)'),
        ('Container 2 (Elet)', 'Container 2 (Elet)')])
    submit = SubmitField('Alterar')


class OrderAddForm(FlaskForm):
    item_name = StringField('Item', validators=[DataRequired()],
        render_kw={'readonly': True})
    curr_quantity = FloatField('Disponivel', validators=[DataRequired()],
        render_kw={'readonly': True})
    date = DateField('Data', validators=[DataRequired()], format='%d/%m/%Y')
    orderer = StringField('Solicitante', validators=[DataRequired()])
    quantity = FloatField('Quantidade', validators=[DataRequired()])
    addit_info = StringField('Observacao')
    submit = SubmitField('Cadastrar')
