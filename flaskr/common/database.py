# from flaskr.db import get_db
from datetime import date

def parseRecord(record):
	if record is None:
		return None
		
	obj = {}
	for key in record.keys():
		if type(record[key]) is date:
			obj[key] = record[key].strftime('%Y-%m-%d %H:%M:%S')
		else:
			obj[key] = record[key]
		
	return obj
	
def validateData(_str_):
	if not _str_:
		return "''"
		
	if _str_.isdigit():
		return str(int(_str_))
		
	if _str_.isdecimal():
		return str(float(_str_))
		
	return "'{0}'".format(_str_)
	
def prepareData(data):
	preparedData = {}
	
	for key in data:
		preparedData[key] = validateData(data[key])
	
	return preparedData

def prepareInsert(table, data):
	if data is None:
		return None
		
	columns = ','.join( list(data.keys()) )
	values = list(data.values())
	holders = []
	
	for key in data.keys():
		if key == 'id':
			continue
		holders.append('?')
	if data.get('id') is not None:
		del data['id']
	
	query = 'INSERT INTO {0}({1}) VALUES({2})'.format(table, columns, ','.join(holders))

	return query

def prepareUpdate(table, data):
	cols = []
	# values = []
	for key in data.keys():
		if key == 'id':
			continue
		cols.append('{0} = ?'.format(key))
		# values.append(data[key])
		
	if data.get('id') is not None:
		del data['id']
	
	query = 'UPDATE {0} SET {1} WHERE id = ?'.format(table, ','.join(cols))
	
	return query
