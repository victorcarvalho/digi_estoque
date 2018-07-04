from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    usuario = {'nome_usuario': 'Joaozinho'}
    itens = [
        {
            'descricao': 'arduino uno',
            'unidade': 'UND'
        },
        {
            'descricao': 'arduino mega',
            'unidade': 'UND'
        }
    ]
    return render_template('index.html', title='Home', usuario=usuario, itens=itens)


# the flask default method is only GET
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # When the browser sends the GET request to receive the web page with the form,
    # this method is going to return False. If it sends the POST request and all
    # validations pass, the method returns True.
    if form.validate_on_submit():
        flash('Login exigido para {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)