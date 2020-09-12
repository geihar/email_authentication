import uuid

from flask import Flask, session, escape, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)



@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'


@app.route('/<username>')
def authentication(username):
    session['username'] = username
    return redirect(url_for('index'))


@app.route('/analytics')
def analytics():
    return 'Hello World!'


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __init__(self, id, email):
        self.id = id
        self.email = email
        self.token = str(uuid.uuid4())



if __name__ == '__main__':
    app.run()
