from flask import current_app, g
import json

def register(app):

	@app.template_filter()
	def json_decode(_str_):
		if _str_ is None or not _str_:
			return None
			
		print('JSON FILTER:', _str_)
		return json.loads(_str_)
