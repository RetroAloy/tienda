
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from tienda.auth import login_required
from tienda.db import get_db
import mysql.connector

bp = Blueprint('producto', __name__)

@bp.route('/')
@login_required
def index():
    db, c = get_db()
    c.execute('SELECT rolname FROM user u JOIN rol r WHERE u.rol_id = r.id AND u.id = %s;', (g.user['id'], ))
    rol = c.fetchone()
    g.pagina = 'index'
    return render_template('store/index.html', rol = rol)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    g.pagina = 'create'
    if request.method == 'POST':
        productname     = request.form['productname']
        price           = request.form['price']
        quantity        = request.form['quantity']
        description     = request.form['description']

        db, c = get_db()
        error = None

        if not productname:
            error = 'Nombre es requerido'
        if not price:
            error = 'Precio es requerido'
        if not quantity:
            error = 'Cantidad es requerida'
        if error is not None:
            flash(error)
        
        if error is None:
            try:
                c.execute(
                    'INSERT INTO product (productname, price, quantity, description) VALUES (%s, %s, %s, %s)',
                    (productname, price, quantity, description)
                )
                db.commit()
                return redirect(url_for('producto.index'))
            except mysql.connector.IntegrityError as err:
                error = 'Nombre ya existe'
                flash(error)
                return redirect(url_for('producto.create'))
                

    return render_template('store/create.html')

@bp.route('/read', methods=['GET', 'POST'])
@login_required
def read():
    g.pagina = 'read'
    if request.method == 'GET':
        db, c = get_db()
        c.execute('SELECT * FROM product')
        productos = c.fetchall()

    return render_template('store/read.html',products = productos)

@bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    g.pagina = 'update'
    db, c = get_db()
    c.execute('SELECT * FROM product')
    productos = c.fetchall()

    if request.method == 'POST':
        id = request.form['id']
        productname = request.form['productname']
        price = request.form['price']
        quantity = request.form['quantity']
        description = request.form['description']

        error = None

        c.execute(
            'SELECT * FROM product WHERE id = %s', (id, )
        )
        producto = c.fetchone()

        if not id:
            error = 'ID es requerido'
        if not productname:
            error = 'Nombre del producto es requerido'
        if not price:
            error = 'Precio es requerido'
        if not quantity:
            error = 'Cantidad es requerido'
        if not description:
            error = 'Descripción es requerido'
        elif producto is None:
            error = 'Producto con ID:{} no se encuentra registrado.'.format(id)

        if error is not None:
            flash(error)

        if error is None:
            c.execute(
                'UPDATE product SET productname = %s, price = %s, quantity = %s, description = %s WHERE id = %s', (productname, price, quantity, description, id)
            )
            db.commit()
            return redirect(url_for('producto.read'))
            
    return render_template('store/update.html', products = productos)

@bp.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    g.pagina = 'delete'
    if request.method == 'GET':
        db, c = get_db()
        c.execute('SELECT * FROM product')
        productos = c.fetchall()

    if request.method == 'POST':
        pass

    return render_template('store/delete.html', products = productos)