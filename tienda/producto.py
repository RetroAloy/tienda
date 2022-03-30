
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from tienda.auth import login_required
from tienda.db import get_db

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
            c.execute(
                'INSERT INTO product (productname, price, quantity, description) VALUES (%s, %s, %s, %s)',
                (productname, price, quantity, description)
            )
            db.commit()
            return redirect(url_for('producto.index'))

    return render_template('store/create.html')

@bp.route('/read', methods=['GET', 'POST'])
@login_required
def read():
    g.pagina = 'read'
    return render_template('store/read.html')

@bp.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    g.pagina = 'update'
    return render_template('store/update.html')

@bp.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    g.pagina = 'delete'
    return render_template('store/delete.html')