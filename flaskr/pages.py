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

bp = Blueprint('pages', __name__)

@bp.route('/paginas/informacion-general')
@login_required
def informacion():
	
	return render_template('informacion-general.html')
