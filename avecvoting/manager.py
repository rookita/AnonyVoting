from base64 import decode
from crypt import methods
from enum import Flag
import imp
from re import U
import re
import time
import json
from flask import request, render_template, session, redirect, flash,jsonify
from sqlalchemy.sql.base import NO_ARG
from __init__ import app
from blockchain import (
    call_contract,
    call_contract2,
    deploy_contract,
    signin_account,
    create_account,
    counter,
)
from werkzeug.datastructures import ImmutableMultiDict
from models import Contract, User, db, Manager
from eth_utils.address import to_checksum_address
import traceback
from user import valid_login
from voteUtils import (
    addr_vaild,
    get_time_now,
    get_vote_addr,
    time_decoder,
    time_encoder,
    trans_str,
    trans_list,
    time_vaild_format,
)
import voter,user

# 生成vote_id
def generate_vote_id():
    count_str = "%03d" % next(counter)
    # today = datetime.date.today()
    # id = str(today.month) +"." + str(today.day) +"." + count_str
    id = count_str
    return id

# 创建新投票,获取前端信息，写入合约和数据库
@app.route("/manager/create", methods=["GET", "POST"])
def create():
    vote_id = generate_vote_id()
    data = request.get_data()
    js = json.loads(data)

    username = js.get("name", 0)
    password = js.get("password", 0)
    manager, signer = valid_login(username, password)
    # print(signer)
    if signer is None:
        return jsonify({"result": 'error1'})
    # 获取ddl合法性检测
    
    vote_title = js.get("title", 0)
    vote_ddl = js.get("endTime", 0)
    vote_type = js.get("type",0)
    vote_candidate_List = js.get("choice",0)

    # time_now_stamp = get_time_now()
    vote_ddl = time_encoder(vote_ddl)
    # print(time_decoder(time_now_stamp))
    # print(time_decoder(vote_ddl))
    # print(vote_ddl)

    # 部署
    try:
        new_vote_addr = deploy_contract("Vote", signer=signer)
    except Exception as e :
        print("===========")
        print(e)
        return jsonify({"result": 'error2'})

    # print("vote合约地址：",new_vote_addr)
    # print("转换后的vote合约地址：",to_checksum_address(new_vote_addr))

    # 查询Management合约地址，用于调用合约
    management_addr = (
        db.session.query(Contract).filter(Contract.name == "Management").first().addr
    )
    # 写入合约设置ddl和title
    try:
        call_contract(
            management_addr,
            "Management",
            "createVote",
            args=[vote_id, to_checksum_address(new_vote_addr), vote_title, vote_ddl, vote_type, "avc"],
            signer=signer,
        )
    except Exception:
        return jsonify({"result": 'error3'})
    # # 写入合约candidate，格式转为list
    _candidateList = trans_list(vote_candidate_List)
    try:
        call_contract(
            management_addr,
            "Management",
            "createVoteCandidate",
            args=[to_checksum_address(new_vote_addr), _candidateList],
            signer=signer,
        )
    except Exception:
        return jsonify({"result": 'error3'})

    P = js.get("P",0)
    Q = js.get("Q",0)
    G = js.get("G",0)
    n = js.get("n",0)
    k = js.get("k",0)
    voters = js.get("voters",0)
    try:
        call_contract(
            new_vote_addr,
            "Vote",
            "setPara",
            args=[P, Q, G, n, k],
            signer=signer,
        )
    except Exception:
        return jsonify({"result": 'error3'})


    for i in voters:
        try:
          call_contract(
            new_vote_addr,
            "Vote",
            "setVoterInfo",
            args=[str(i["id"]), "0", "0","0"],
            signer=signer,
        )
        except Exception:
            return jsonify({"result": 'error3'})
        # print(type(i["id"]),type(i["weight"]))
    print("应该是成功了")
    return jsonify({"result": 'success', "ID":vote_id, "addr":new_vote_addr})


@app.route("/manager/createWe", methods=["GET", "POST"])
def createWe():
    vote_id = generate_vote_id()
    data = request.get_data()
    js = json.loads(data)
    # print("ddddddd::::::",data)

    username = js.get("name", 0)
    password = js.get("password", 0)
    manager, signer = valid_login(username, password)
    # print(signer)
    if signer is None:
        return jsonify({"result": 'error1'})
    # 获取ddl合法性检测
    
    vote_title = js.get("title", 0)
    vote_content = js.get("content",0)
    vote_ddl = js.get("endTime", 0)
    P = js.get("P",0)
    Q = js.get("Q",0)
    G = js.get("G",0)
    voters = js.get("voters",0)
    print("dsdsdsdsdsdsdsds",voters,len(voters),type(voters))
    print(type(voters[0]["id"]))

    # time_now_stamp = get_time_now()
    vote_ddl = time_encoder(vote_ddl)
    # print(time_decoder(time_now_stamp))
    # print(time_decoder(vote_ddl))
    # print(vote_ddl)

    # 部署
    try:
        new_vote_addr = deploy_contract("VoteWe", signer=signer)
    except Exception as e :
        print("===========")
        print(e)
        return jsonify({"result": 'error2'})

    # print("vote合约地址：",new_vote_addr)
    # print("转换后的vote合约地址：",to_checksum_address(new_vote_addr))

    # 查询Management合约地址，用于调用合约
    management_addr = (
        db.session.query(Contract).filter(Contract.name == "Management").first().addr
    )

    # 写入合约设置ddl和title
    try:
        call_contract(
            management_addr,
            "Management",
            "createVoteWe",
            args=[vote_id, to_checksum_address(new_vote_addr), vote_title, vote_ddl, vote_content,"we"],
            signer=signer,
        )
    except Exception:
        return jsonify({"result": 'error3'})

    try:
        call_contract(
            new_vote_addr,
            "VoteWe",
            "setPara",
            args=[P, Q, G],
            signer=signer,
        )
    except Exception:
        return jsonify({"result": 'error3'})

    for i in voters:
        try:
          call_contract(
            new_vote_addr,
            "VoteWe",
            "setVoterInfo",
            args=[str(i["id"]), "0", "0", i["weight"],"0"],
            signer=signer,
        )
        except Exception:
            return jsonify({"result": 'error3'})
        # print(type(i["id"]),type(i["weight"]))

    print("应该是成功了")
    return jsonify({"result": 'success', "ID":vote_id, "addr":new_vote_addr})

