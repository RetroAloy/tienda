import functools
from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)
from tienda.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        rol      = request.form['complete-select']
        db, c = get_db()
        c.execute(
            'SELECT * FROM rol;'
        )
        g.roles = c.fetchall()
        error = None
        c.execute(
            'SELECT id FROM user WHERE username = %s', (username, )
        )
        if not username:
            error = 'Username es requerido'
        if not password:
            error = 'Password es requerido'
        if not rol:
            error = 'Rol es requerido'
        elif c.fetchone() is not None:
            error = 'Usuario {} se encuentra registrado.'.format(username)

        if error is not None:
            flash(error)
        if error is None:
            c.execute(
                'INSERT INTO user (username, password, rol_id) VALUES (%s, %s, %s)',
                (username, generate_password_hash(password), rol)
            )
            db.commit()
            return redirect(url_for('auth.login'))
    if request.method == 'GET':
        db, c = get_db()
        c.execute(
            'SELECT * FROM rol;'
        )
        g.roles = c.fetchall()

    g.pagina = "register"
    return render_template('auth/register.html')

@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'SELECT * FROM user WHERE username = %s', (username,)
        )
        user = c.fetchone()

        if user is None:
            error = 'Usuario y/o contraseña inválida'
        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o contraseña inválida'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('producto.index'))
        
        flash(error)
    g.pagina = 'login'
    return render_template('auth/login.html')

@bp.route('/validacion', methods=['GET', 'POST'])
def validacion():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'SELECT * FROM user WHERE username = %s', (username,)
        )
        user = c.fetchone()
        if username == 'Admin' and password == '1234':
            session.clear()
            return redirect(url_for('auth.register'))
        if user is None:
            error = 'Usuario y/o contraseña inválida'
        elif not check_password_hash(user['password'], password):
            error = 'Usuario y/o contraseña inválida'
        if error is None:
            session.clear()
            return redirect(url_for('auth.register'))

        flash(error)
    g.pagina = 'register'

    return render_template('auth/validacion_registro.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            'SELECT * FROM user WHERE id = %s', (user_id, )
        )
        g.user = c.fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))