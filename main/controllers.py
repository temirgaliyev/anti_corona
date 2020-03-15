from flask import Blueprint, redirect, url_for, render_template, request

from data.models import Person, db
from utils.csv2dict import convert
from constants import attributes as attrs

from datetime import datetime
from os.path import join


main = Blueprint('main', __name__)


langs_dict = {}
convert(langs_dict, csv_file=join('languages', 'langs.csv'))


def get_lang(locale='ru'):
	return langs_dict[f"LANG_{locale.upper()}"]


@main.route("")
def home():
	return render_template('index.html', content=['tim', 'joe', 'bill'])


@main.route("/upload", methods=["GET", "POST"])
def upload():
	if request.method == "POST":
		if request.files:
			raw_list = request.get_array(field_name='excel')
			removed_empty_list = [line for line in raw_list if sum(len(str(elem)) for elem in line)>10]

			column_names = [get_lang('ru')[attr] for attr in attrs]
			first_row = 0
			first_column = 0
			while first_row < len(removed_empty_list):
				try:
					# print(removed_empty_list[first_row][first_column])
					tmp_date = datetime.strptime(str(removed_empty_list[first_row][first_column]), '%d.%m.%Y')
					break
				except Exception as e:
					if first_column == 0:
						first_column = 1
					else:
						first_row += 1
						first_column = 0

			column_values = removed_empty_list[first_row:]

			for line in column_values:
				entry_date = datetime.strptime(str(line[first_column]), '%d.%m.%Y')
				flight = str(line[first_column+1])
				fullname = str(line[first_column+2])
				id_number = str(line[first_column+3])
				birth_date = datetime.strptime(line[first_column+4], '%d.%m.%Y')				
				passport_number = str(line[first_column+5])
				citizenship = str(line[first_column+6])
				phone = str(line[first_column+7])
				before_arrival = str(line[first_column+8])
				region = str(line[first_column+9])
				residence = str(line[first_column+10])
				work_place = str(line[first_column+11])
				found = line[first_column+12].lower()=='да'
				hospitalized = line[first_column+13].lower()=='да'
				hospital = str(line[first_column+14])
				person = Person(entry_date=entry_date, flight=flight, fullname=fullname, id_number=id_number,
					passport_number=passport_number, birth_date=birth_date, citizenship=citizenship, phone=phone,
					before_arrival=before_arrival, region=region, residence=residence, work_place=work_place, 
					found=found, hospitalized=hospitalized, hospital=hospital)

				db.session.add(person)
			
			db.session.commit()
			return render_template("upload_result.html", column_names=column_names, column_values=column_values)


	return render_template('upload.html', lang=get_lang('ru'))


@main.route("/show")
def show():
	persons = Person.query.all()
	return render_template('show.html', attr_names=get_lang('ru'), attrs=attrs, persons=persons)


@main.route("/add", methods=["GET", "POST"])
def add():

	if request.method == "POST":
		entry_date = datetime.strptime(request.form.get('entry_date'), '%Y-%m-%d')
		flight = str(request.form.get('flight'))
		fullname = str(request.form.get('fullname'))
		id_number = str(request.form.get('id_number'))
		birth_date = datetime.strptime(request.form.get('birth_date'), '%Y-%m-%d')				
		passport_number = str(request.form.get('passport_number'))
		citizenship = str(request.form.get('citizenship'))
		phone = str(request.form.get('phone'))
		before_arrival = str(request.form.get('before_arrival'))
		region = str(request.form.get('region'))
		residence = str(request.form.get('residence'))
		work_place = str(request.form.get('work_place'))
		found = request.form.get('found_yes') == 'on'
		hospitalized = request.form.get('hospitalized_yes') == 'on'
		hospital = str(request.form.get('hospital'))

		person = Person(entry_date=entry_date, flight=flight, fullname=fullname, id_number=id_number,
			passport_number=passport_number, birth_date=birth_date, citizenship=citizenship, phone=phone,
			before_arrival=before_arrival, region=region, residence=residence, work_place=work_place, 
			found=found, hospitalized=hospitalized, hospital=hospital)

		db.session.add(person)
		db.session.commit()

	return render_template('add.html')
