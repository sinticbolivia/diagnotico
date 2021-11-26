import json
from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from werkzeug.security import check_password_hash, generate_password_hash
import base64
import json
from flaskr.authentication import login_required
from flaskr.models import diagnosticos as diagnosticosmodel
from flaskr.models import pacientes as pacientesmodel
from flaskr.models import tratamientos as tratamientosmodel

bp = Blueprint('diagnosticos', __name__)

@bp.route('/diagnosticos')
@login_required
def index():
	keyword = request.args.get('keyword')
	
	diagnosticos = []
	if keyword is not None and keyword:
		diagnosticos = diagnosticosmodel.search(keyword)
	else:
		keyword = ''
		diagnosticos = diagnosticosmodel.listar()
		
	return render_template('diagnosticos.html', 
		diagnosticos=diagnosticos, 
		model=diagnosticosmodel, 
		pacientesmodel=pacientesmodel,
		tratamientosmodel=tratamientosmodel,
		keyword=keyword,
		header_path='Diagnosticos',
	)

