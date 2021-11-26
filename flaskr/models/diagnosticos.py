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
	return db.execute(query).fetchone()
	
	
def listar():
	db = get_db();
	
	query = 'SELECT * FROM diagnosticos ORDER BY id DESC'
	return db.execute(query).fetchall()
	
