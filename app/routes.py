from flask import render_template, flash, redirect, url_for, request
from flask_login import logout_user, current_user, login_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, ItemAddForm, ItemEditForm, OrderAddForm
from app.models import User, Item, Order
from datetime import datetime
from babel.dates import format_date


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuario ou senha invalidos')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Voce foi cadastrado com sucesso')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/item_add', methods=['GET', 'POST'])
@login_required
def item_add():
    form = ItemAddForm()
    if form.validate_on_submit():
        item = Item()
        item.set_name(form.name.data)
        item.set_unit(form.unit.data)
        item.set_quantity(form.quantity.data)
        item.set_room(form.room.data)
        db.session.add(item)
        db.session.commit()
        flash('Item cadastrado com sucesso')
        return redirect(url_for('item_list'))
    return render_template('item/add.html', title='Cadastrar item', form=form)


@app.route('/item_list')
@login_required
def item_list():
    items = Item.query.order_by(Item.name.asc())
    return render_template('item/list.html', title='Listar itens', items=items)


@app.route('/item_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def item_delete(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item excluido com sucesso.')
    return redirect(url_for('item_list'))


@app.route('/item_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def item_edit(id):
    item = Item()
    form = ItemEditForm()
    item = Item.query.get_or_404(id)
    if form.validate_on_submit():
        item.set_name(form.name.data)
        item.set_unit(form.unit.data)
        item.set_quantity(form.quantity.data)
        item.set_room(form.room.data)
        db.session.add(item)
        db.session.commit()
        flash('Item alterado com sucesso.')
        return redirect(url_for('item_list'))
    elif request.method == 'GET':
        form.name.data = item.name
        form.quantity.data = item.quantity
        form.unit.data = item.unit
        form.room.data = item.room
    return render_template('item/edit.html', title='Editar item', form=form)


@app.route('/item_orders/<int:id>', methods=['GET', 'POST'])
@login_required
def item_orders(id):
    item = Item.query.get_or_404(id)
    orders = Order.query.filter_by(item_name=item.name)
    return render_template('order/list.html', title='Pedidos relacionados',
        orders=orders)


@app.route('/item_dec/<int:id>', methods=['GET', 'POST'])
@login_required
def item_dec(id):
    item = Item.query.get_or_404(id)
    item.decrease_quantity(1) # decrementa quantidade em uma unidade
    db.session.add(item)
    db.session.commit()
    flash('Item decrementado com sucesso.')
    return redirect(url_for('item_list'))


@app.route('/order_add/<int:id>', methods=['GET', 'POST'])
@login_required
def order_add(id):
    form = OrderAddForm()
    item = Item.query.get_or_404(id)
    if form.validate_on_submit():
        if form.quantity.data > item.quantity:
            flash('ERRO: a quantidade desejada eh maior que a disponivel')
        else:
            item.decrease_quantity(form.quantity.data)
            db.session.add(item)
            order = Order()
            order.set_item_name(item.name)
            order.set_orderer(form.orderer.data)
            order.set_date(form.date.data)
            order.set_quantity(form.quantity.data)
            order.set_addit_info(form.addit_info.data)
            db.session.add(order)
            db.session.commit()
            flash('Pedido cadastrado com sucesso.')
        return redirect(url_for('item_list'))
    elif request.method == 'GET':
        form.date.data = format_date(datetime.now(), 'dd/MM/yy')
        form.item_name.data = item.name
        form.curr_quantity.data = item.quantity
    return render_template('order/add.html', title='Cadastrar pedido', form=form)


@app.route('/order_list')
@login_required
def order_list():
    orders = Order.query.order_by(Order.date.desc())
    return render_template('order/list.html', title='Listar pedidos', orders=orders)


@app.route('/order_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def order_delete(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    flash('Pedido excluido com sucesso.')
    return redirect(url_for('order_list'))
