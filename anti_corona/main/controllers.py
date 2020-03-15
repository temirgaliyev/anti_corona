from flask import Blueprint, redirect, url_for, render_template, request

from anti_corona.data.models import Person, db
from anti_corona.utils.csv2dict import convert

from datetime import datetime
from os.path import join


main = Blueprint('main', __name__)
attributes = ['entry_date', 'flight', 'fullname', 'id_number', 
'birth_date', 'passport_number', 'citizenship', 'phone', 'before_arrival',
'region', 'residence', 'work_place', 'found', 'hospitalized', 'hospital']


langs_dict = {}
convert(langs_dict, csv_file=join('anti_corona', 'languages', 'langs.csv'))


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
			column_names = removed_empty_list[3]
			column_values = removed_empty_list[4:]

			for line in column_values:
				entry_date = datetime.strptime(str(line[1]), '%d.%m.%Y')
				flight = str(line[2])
				fullname = str(line[3])
				id_number = str(line[4])
				birth_date = datetime.strptime(line[5], '%d.%m.%Y')				
				passport_number = str(line[6])
				citizenship = str(line[7])
				phone = str(line[8])
				before_arrival = str(line[9])
				region = str(line[10])
				residence = str(line[11])
				work_place = str(line[12])
				found = line[13].lower()=='да'
				hospitalized = line[14].lower()=='да'
				hospital = str(line[15])
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
	return render_template('show.html', attr_names=get_lang('ru'), atts=attributes, persons=persons)


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
