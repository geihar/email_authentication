import uuid

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    token = db.Column(db.String(120), index=True)
    visits = db.Column(db.Integer, default=0)

    def set_token(self):
        self.token = str(uuid.uuid4())

    def add_visits(self):
        self.visits += 1
