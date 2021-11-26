from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db
from datetime import date
from flaskr.common import database as databasecommon

def create(data):
	today = date.today()
	db = get_db()
	
	data['creation_date'] = today.strftime("%Y-%m-%d %H:%M:%S")
	query = databasecommon.prepareInsert('pacientes', data)
	print(query)
	
	try:
		db.execute(query, list(data.values()))
		db.commit()
	except:
		db.rollback()

def update(id, _data_):

	data = _data_ # databasecommon.prepareData(_data_)
	
	query = databasecommon.prepareUpdate('pacientes', data)
	print(query)
	
	try:
		db = get_db()
		db.execute(query, list(data.values()) + [id])
		db.commit()
	except:
		db.rollback()
		
def obtener(id):
	db = get_db()
	query = 'SELECT * FROM pacientes WHERE id = {0}'.format(id)
	record = db.execute(query).fetchone()
	if record is None:
		return None
	
	return databasecommon.parseRecord(record)
	
def listar():
	db = get_db();
	
	query = 'SELECT * FROM pacientes ORDER BY id DESC'
	return db.execute(query).fetchall()

def delete(id):
	try:
		db = get_db()
		query = 'DELETE FROM diagnosticos WHERE paciente_id = {0}'.format(id)
		db.execute(query)
		query = 'DELETE FROM pacientes WHERE id = {0}'.format(id)
		db.execute(query)
		db.commit()
	except:
		db.rollback()
		
def search(keyword):
	try:
		db = get_db()
		query = "SELECT * FROM pacientes " \
			"WHERE (nombres LIKE '%?%' OR apellido_paterno LIKE '%?%' OR apellido_materno LIKE '%?%' OR historial LIKE '%?%') ".replace('?', keyword)
		print(query)
		return db.execute(query).fetchall()
		
	except:
		print('Search error')
		
def sintomas():
	return [
		{'id': 1, 'nombre': 'Congestion nasal'},
		{'id': 2, 'nombre': 'Estornudos'},
		{'id': 3, 'nombre': 'Rinorea Clara y el purito'},
		{'id': 4, 'nombre': 'Nasofaringueo y ocular'},
		{'id': 5, 'nombre': 'Resfrio Persistente'},
		{'id': 6, 'nombre': 'Sinusitis Cronica'},
		{'id': 7, 'nombre': 'Sinusitis Cronica 2'},
		{'id': 8, 'nombre': 'Prupito en los oidos'},
		{'id': 9, 'nombre': 'Lagrimeo en los ojos'},
		{'id': 10, 'nombre': 'Secrecion nasal'},
		{'id': 11, 'nombre': 'Sueño'},
		{'id': 12, 'nombre': 'Obstruccion nasal'},
		{'id': 13, 'nombre': 'Dolores de oido y sefalea'},
		{'id': 14, 'nombre': 'Alteracion del olfato y gusto'},
	]
	
def resultados():
	return [
		{'ids': [1,	2, 3, 4, 6, 8, 9, 12],'resultado': 'resultado 1'},
		{'ids': [1,	2, 3, 4, 6, 7, 9, 10, 11, 12],'resultado': 'resultado 2'},
		{'ids': [2, 3, 6, 7, 8, 10],'resultado': 'resultado 3'},
		{'ids': [1, 3, 4, 5, 7, 9, 12],'resultado': 'resultado 4'}, #
		{'ids': [1,	3, 4, 6, 8, 12],'resultado': 'resultado 5'}, #
		{'ids': [2, 3, 4, 8, 10, 11, 12],'resultado': 'resultado 6'},
		{'ids': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],'resultado': 'resultado 7'},
		{'ids': [1, 3, 4, 9, 12],'resultado': 'resultado 8'},
		{'ids': [1,	7, 12],'resultado': 'resultado 9'},
		{'ids': [1,	3, 12],'resultado': 'resultado 10'},
		{'ids': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],'resultado': 'resultado 11'},
		{'ids': [11, 12],'resultado': 'resultado 12'},
		{'ids': [1, 4, 10, 12, 13],'resultado': 'resultado 13'},
		{'ids': [4, 9, 12, 13],'resultado': 'resultado 14'},
		{'ids': [1, 7, 8, 10, 11, 12, 13],'resultado': 'resultado n'},
	]
