import sqlite3
import traceback
import sys
from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db
from datetime import date
from flaskr.common import database as dbfunctions

def create(_data_):
	data = _data_ # dbfunctions.prepareData(_data_)
	
	today = date.today()
	db = get_db()
	data['creation_date'] = today.strftime("%Y-%m-%d %H:%M:%S")
	
	query = dbfunctions.prepareInsert('diagnosticos', data)
	print(query)
	
	try:
		db.execute(query, list(data.values()))
		db.commit()
	except:
		db.rollback()
		

def obtener(id):
	db = get_db()
	query = 'SELECT * FROM diagnosticos WHERE id = {0}'.format(id)
	obj = db.execute(query).fetchone()
	return dbfunctions.parseRecord(obj)	
	
	
def listar():
	db = get_db();
	
	query = 'SELECT * FROM diagnosticos ORDER BY id DESC'
	return db.execute(query).fetchall()
	
def search(keyword):
	query = "select d.id, d.paciente_id, d.tratamiento_id, d.diagnostico, d.tratamiento, d.resultado"\
			", t.nombre, p.nombres, p.apellido_paterno, p.apellido_materno, p.historial "\
			"from diagnosticos d "\
			"join pacientes p on p.id = d.paciente_id "\
			"join tratamientos t on t.id = d.tratamiento_id " \
			"WHERE 1 "\
			"AND (p.nombres LIKE '%?%' OR p.apellido_paterno LIKE '%?%' OR p.apellido_materno LIKE '%?%' OR p.historial LIKE '%?%')"
	query = query.replace('?', keyword)
	print(query)
	try:
		db = get_db()
		return db.execute(query).fetchall()
	except sqlite3.Error as er:
		print('SQLite error: %s' % (' '.join(er.args)))
		print("Exception class is: ", er.__class__)
		print('SQLite traceback: ')
		exc_type, exc_value, exc_tb = sys.exc_info()
		print(traceback.format_exception(exc_type, exc_value, exc_tb))
	except Exception as e:
		print('BUSQUEDA DIAGNOSTICO ERROR\n', e, '\n', query)
		return []

def update(id, _data_):

	data = _data_ # databasecommon.prepareData(_data_)
	
	query = dbfunctions.prepareUpdate('diagnosticos', data)
	print(query)
	
	try:
		db = get_db()
		db.execute(query, list(data.values()) + [id])
		db.commit()
	except:
		db.rollback()
