# -*- coding: utf-8 -*-
import functools
from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
import json
from flaskr.common import database as dbfunctions

bp = Blueprint('auth', __name__)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		g.user = dbfunctions.parseRecord(get_db().execute(
			'SELECT * FROM usuarios WHERE id = ?', (user_id,)
		).fetchone())

@bp.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['usuario']
		password = request.form['pwd']
		db = get_db()
		error = None
		user = db.execute(
			'SELECT * FROM usuarios WHERE usuario = ?', (username,)
		).fetchone()

		if user is None:
			error = 'Nombre usuario incorrecto.'
		elif not check_password_hash(user['pwd'], password):
			error = 'Contrasena incorrecta.'

		if error is None:
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('index'))

		flash(error)
		return redirect(url_for('auth.login'))

	return render_template('login.html')

@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))
