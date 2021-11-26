# -*- coding: utf-8 -*-
import json
from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from werkzeug.security import check_password_hash, generate_password_hash
import base64
import json

from flaskr.db import get_db
from flaskr.authentication import login_required
from flaskr.models import pacientes
from flaskr.models import tratamientos as tratamientosmodel
from flaskr.models import diagnosticos as diagnosticosmodel
from flaskr.common import database as databasecommon



bp = Blueprint('pacientes', __name__)

@bp.route('/')
@login_required
def index():
	keyword = request.args.get('keyword')
	_pacientes_ = None
	print(keyword)
	if keyword is not None and keyword:
		print('Buscando', keyword)
		_pacientes_ = pacientes.search(keyword)
	else:
		_pacientes_ = pacientes.listar()
	header_path = 'Pacientes'
	
	return render_template('pacientes.html', 
		pacientes=_pacientes_, keyword=keyword if keyword is not None else '',
		header_path = header_path
	)

@bp.route('/pacientes/nuevo', methods=('GET', 'POST'))
@login_required
def nuevo():
	if request.method == 'POST':
		if request.form.get('id') is None:
			pacientes.create(request.form.copy() )
		else:
			pacientes.update(int(request.form.get('id')), request.form.copy() )
			
		flash('Paciente guardado correctamente', 'success')
		return redirect(url_for('pacientes.index'))
	
	
	return render_template('nuevo-paciente.html', header_path='Nuevo Paciente')

@bp.route('/pacientes/editar/<id>')
@login_required
def editar(id):
	paciente = pacientes.obtener(id)
	if paciente is None:
		flash('El paciente no existe', 'error')
		return redirect(url_for('pacientes.index'))
	paciente['fecha_nacimiento'] = paciente['fecha_nacimiento'].replace(' 00:00:00', '')
	return render_template('nuevo-paciente.html', paciente=paciente)
		
@bp.route('/pacientes/<id>/simulacion')
@login_required
def simulacion(id):
	sintomas = pacientes.sintomas()
	paciente = pacientes.obtener(id)
	resultados = pacientes.resultados()
	
	return render_template('simulador.html', sintomas = sintomas, paciente=paciente, resultados=resultados, json=json)
	
@bp.route('/pacientes/<id>/diagnosticos/nuevo', methods=['POST'])
@login_required
def nuevoDiagnotico(id):
	# print(request.form)
	paciente = pacientes.obtener(id)
	tratamientos = tratamientosmodel.listar()
	resultado_raw = base64.b64decode(request.form['resultado']).decode('ascii')
	resultado = json.loads(resultado_raw)
	resultado64 = request.form['resultado']
	
	return render_template('nuevo-diagnostico.html', 
		paciente=paciente, 
		resultado=resultado, 
		tratamientos=tratamientos,
		resultado64=resultado64
	)

@bp.route('/pacientes/<id>/diagnosticos/', methods=['POST'])
@login_required
def crearDiagnostico(id):
	data = dict(zip(request.form.keys(), request.form.values()))
	print(data)
	data['resultado'] = base64.b64decode(data['resultado']).decode('ascii')
	
	diagnosticosmodel.create(data)
	flash('Diagnostico guardado correctament', 'success')
	
	return redirect(url_for('diagnosticos.index'))
