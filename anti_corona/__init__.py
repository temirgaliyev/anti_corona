from flask import Flask
import flask_excel as excel

from anti_corona.main.controllers import main
from anti_corona.data.models import db
from anti_corona.utils.csv2dict import convert


app = Flask(__name__)
app.config['UPLOADS'] = '/uploads'
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

excel.init_excel(app)

app.register_blueprint(main, url_prefix='/')
