# models.py
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
