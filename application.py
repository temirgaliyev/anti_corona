from flask import Flask
import flask_excel as excel

from main.controllers import main
from api.controllers import api

from data.models import db
from utils.csv2dict import convert


application = Flask(__name__)
application.config['UPLOADS'] = '/uploads'
application.config['JSON_AS_ASCII'] = False
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(application)
with application.app_context():
    db.create_all()

excel.init_excel(application)

application.register_blueprint(main, url_prefix='/')
application.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
	application.run(debug=True) 