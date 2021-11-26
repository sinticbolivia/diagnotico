# -*- coding: utf-8 -*-
from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db
from flaskr.models import tratamientos
import json
from flaskr.authentication import login_required
from flaskr.common import database as databasecommon

bp = Blueprint('tratamientos', __name__)


@bp.route('/tratamientos')
@login_required
def index():
	keyword = request.args.get('keyword')
	_pacientes_ = None
	print(keyword)
	if keyword is not None and keyword:
		print('Buscando', keyword)
		_pacientes_ = tratamientos.search(keyword)
	else:
		_pacientes_ = tratamientos.listar()
	return render_template('tratamientos.html', pacientes=_pacientes_, keyword=keyword if keyword is not None else '')

@bp.route('/tratamientos/nuevo', methods=('GET', 'POST'))
@login_required
def nuevo():
	if request.method == 'POST':
		
		if request.form.get('id') is None:
			tratamientos.create(request.form.copy())
		else:
			tratamientos.update(request.form.get('id'), request.form.copy())
			
		flash('Tratamiento guardado correctamente')
		return redirect(url_for('tratamientos.index'))
	
	
	return render_template('nuevo-tratamiento.html')

@bp.route('/tratamientos/editar/<id>')
@login_required
def editar(id):
	tratamiento = tratamientos.obtener(id)
	if tratamiento is None:
		flash('Tratamiento no encontrado', 'error')
		return redirect(url_for('tratamientos.index'))
	return render_template('nuevo-tratamiento.html', tratamiento=tratamiento)
	
@bp.route('/tratamientos/borrar/<id>')
@login_required
def borrar(id):
	tratamientos.delete(id)
	flash('Tratamiento borrado correctamente')
	return redirect(url_for('tratamientos.index'))
