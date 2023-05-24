from flask_sqlalchemy import SQLAlchemy

from __init__ import app

db = SQLAlchemy(app)


class Contract(db.Model):
    name = db.Column(db.String(128), primary_key=True, unique=True, nullable=False)
    addr = db.Column(db.String(1024), default="")


# 平台充当计票者发送交易
class Manager(db.Model):
    username = db.Column(db.String(128), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(128), default="")

class User(db.Model):
    userid = db.Column(db.String(128), primary_key=True, unique=True, nullable=False)
    We_sign_pubs = db.Column(db.String(128), default="")
    We_enc_pubs = db.Column(db.String(128), default="")
    username= db.Column(db.String(128), default="")
    password = db.Column(db.String(128), default="")