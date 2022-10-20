from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'EVAS',
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine()
db.init_app(app)
