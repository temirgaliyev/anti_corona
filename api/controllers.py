from flask import Blueprint, redirect, url_for, render_template, request

from data.models import Person, db
from sqlalchemy import update


api = Blueprint('api', __name__)


@api.route("/check_found", methods=['GET', 'POST'])
def check_found():
	if request.method == "POST":
		for val in request.get_json():
			db.session.query(Person).\
				filter_by(id=val).\
				update({"found": True})
		db.session.commit()
		return "ok"
	else:
		return 'wrong_method'


@api.route("/uncheck_found", methods=['GET', 'POST'])
def uncheck_found():
	if request.method == "POST":
		for val in request.get_json():
			db.session.query(Person).\
				filter_by(id=val).\
				update({"found": False})
		db.session.commit()
		return "ok"
	else:
		return 'wrong_method'


@api.route("/check_hospitalized", methods=['GET', 'POST'])
def check_hospitalized():
	if request.method == "POST":
		for val in request.get_json():
			db.session.query(Person).\
				filter_by(id=val).\
				update({"hospitalized": True})
		db.session.commit()
		return "ok"
	else:
		return 'wrong_method'


@api.route("/uncheck_hospitalized", methods=['GET', 'POST'])
def uncheck_hospitalized():
	if request.method == "POST":
		for val in request.get_json():
			db.session.query(Person).\
				filter_by(id=val).\
				update({"hospitalized": False})
		db.session.commit()
		return "ok"
	else:
		return 'wrong_method'


@api.route("/add_hospital", methods=['GET', 'POST'])
def add_hospital():
	if request.method == "POST":
		val, hospital = request.get_json()
		
		db.session.query(Person).\
			filter_by(id=val).\
			update({"hospital": hospital})
		db.session.commit()
		
		return "ok"
	else:
		return 'wrong_method'
