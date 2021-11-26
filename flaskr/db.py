import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.common import database as dbfunctions
from datetime import date

def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row
		
	return g.db
	
def close_db(e=None):
	db = g.pop('db', None)
	if db is not None:
		db.close()


def init_db():
	db = get_db()
	
	with current_app.open_resource('database.sql') as f:
		db.executescript(f.read().decode('utf8'))
	today = date.today()
	
	data = {
		'usuario': 'admin',
		'pwd': generate_password_hash('admin'),
		'nombres': 'Admin',
		'apellidos': 'Admin',
		'email': 'admin@mailinator.com',
		'creation_date': today.strftime("%Y-%m-%d %H:%M:%S")
	}
	'''
	query = 'INSERT INTO usuarios({0}) VALUES({1})'.format(
		','.join(data.keys()),
		
	)
	'''
	checkQuery = "SELECT id FROM usuarios where usuario = 'admin'";
	if db.execute(checkQuery).fetchone() is None:
		query = dbfunctions.prepareInsert('usuarios', data)
		db.execute(query, list(data.values()))
		db.commit()
	
@click.command('init-db')
@with_appcontext
def init_db_command():
	init_db()
	click.echo('Base de datos inicializada con exito!!!')
	
def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)
