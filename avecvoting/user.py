from lib2to3.pgen2 import token
from __init__ import app
from flask import jsonify,request,session
from models import db, User
from blockchain import signin_account,create_account
from voteUtils import get_hash
import json
import traceback


def valid_login(username, password):
    manager = User.query.filter(User.username == username).first()
    if manager is None:
        return None, None
    if password != manager.password:
        return None, None
    signer = signin_account(username, password)
    if signer is None:
        return None, None
    else:
        return manager, signer

@app.route('/login', methods=["GET","POST"])
def login():
    data = request.get_data()
    # print(data,type(data))
    js = json.loads(data)
    # print(js,type(js))
    name = js.get("name", 0)
    password = js.get("password", 0)
    # print(name,type(name))
# 查询数据库
    user = User.query.filter(User.username == name).first()
    if user is None:
        return jsonify({"result": 'none'})
    if password != user.password:
        return jsonify({"result": 'fail'})
    uid = user.userid
    signer = signin_account(name, password)
    # test = create_account(name,password)
    print("siger::::::::",type(signer))

    # print("test:::::::::",test)
    if signer is None:
        return jsonify({"result": 'error'})
    else:
        # session["username"] = name 
        # session["password"] = password
        # print(session.get("username"))
        return jsonify({"result": 'success',"token":"token","uid":uid})

    
@app.route('/register', methods=["GET","POST"])
def register():
    data = request.get_data()
    # print(data)
    js = json.loads(data)
    id = js.get("uid", 0)
    name = js.get("name", 0)
    password = js.get("password",0)

    user = User.query.filter(User.username == name).first()
    if user:
        return jsonify({"result": 'exist'})
    else:
        try:
            signer = create_account(name, password)
            print("test:::::::::",signer)
            user = User(userid=id ,username=name, password=password)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            traceback.print_exc()
            db.session.rollback()
        return jsonify({"result": 'success'})

