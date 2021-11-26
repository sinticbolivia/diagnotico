from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db
from datetime import date
from flaskr.common import database as dbfunctions

def create(data):
	today = date.today()
	db = get_db()
	
	data['creation_date'] = today.strftime("%Y-%m-%d %H:%M:%S")
	
	query = dbfunctions.prepareInsert('tratamientos', data)
	print(query)
	
	try:
		db.execute(query, list(data.values()))
		db.commit()
	except:
		db.rollback()

def update(id, data):
	db = get_db()
	query = dbfunctions.prepareUpdate('tratamientos', data)
	print(query, list(data.values()) + [id])
	
	try:
		db.execute(query, list(data.values()) + [id])
		db.commit()
	except:
		db.rollback()
	
def obtener(id):
	db = get_db()
	query = 'SELECT * FROM tratamientos WHERE id = {0}'.format(id)
	return db.execute(query).fetchone()
	
	
def listar():
	db = get_db();
	
	query = 'SELECT * FROM tratamientos ORDER BY id DESC'
	return db.execute(query).fetchall()
	
def delete(id):
	db = get_db();
	query = 'DELETE FROM tratamientos WHERE id = ?'
	db.execute(query, (id,))
	db.commit()

def search(keyword):
	try:
		db = get_db()
		query = "SELECT * FROM tratamientos " \
			"WHERE (nombre LIKE '%?%') ".replace('?', keyword)
		print(query)
		return db.execute(query).fetchall()
		
	except:
		print('Search error')
		db.rollback()
