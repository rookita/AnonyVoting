# from base64 import encode
# from ctypes import resize
# import imp
import json
# from inspect import signature
# from logging import NOTSET
# from operator import ipow
# from re import I
import traceback
# from cryptography.hazmat import backends
from flask import request, render_template, session, flash, url_for,jsonify
# from sqlalchemy.orm import query
# from werkzeug.utils import redirect
from user import valid_login
from __init__ import app
from client_config import client_config
from blockchain import call_contract, create_account, signin_account, call_contract2
from models import Contract,db,User
from eth_utils.address import to_checksum_address
from voteUtils import (
    get_now,
    get_time_now,
    addr_vaild,
    get_hash,
    get_ballots,
    # get_vote_info,
    get_vote_addr,
    get_vote_id_list,
    # get_vote_info_candidate,
    time_decoder,
    time_encoder,
    trans_list,
    trans_str,
    getVoteWeList,
    getVoteWePara,
    getVoterWe,
    if_We_PK,
    getWeBallot,
    setCounter,
    getCounter,
    if_Allshare,
    setCounterPK
)
from voteavecUtils import(
    getVoteAvcList,
    getVoterAvc,
    getVoteAvcPara,
    getAvcBallot,
    getavcPK,
    setavcPK,
    if_avc_kshare,
    get_vote_info_candidate
)

# # 选择ID 加入投票获取
# @app.route("/voter/join_vote", methods=["GET", "POST"])
# def join_vote():
#     data = request.get_data()
#     js = json.loads(data)
#     username = js.get("name", 0)
#     password = js.get("password", 0)
#     # print(password)
#     vote_id = js.get("ID", 0)

#     _, signer = valid_login(username, password)
#     if signer is None:
#         return jsonify({"result": 'error1'})

#     vote_addr = get_vote_addr(vote_id, signer)
#     if addr_vaild(vote_addr):
#         return jsonify({"result": 'error2'})
    
#     # print("aaaaa:",get_if_vote_type(vote_id, signer))
#     if not get_if_vote_type(vote_id, signer):
#         vote_title, vote_ddl ,vote_content= get_vote_info(vote_addr, "VoteWe", signer)
#         vote_ddl=time_decoder(vote_ddl)
#         return jsonify({"result":'success',"type":'we',"ID":vote_id,"title": vote_title,'content':vote_content,'ddl':vote_ddl})

#     vote_title, vote_ddl, vote_type= get_vote_info(vote_addr, "Vote", signer)
#     vote_ddl=time_decoder(vote_ddl)
#     vote_candidateList = trans_list(get_vote_info_candidate(vote_addr, signer))
#     # print(vote_candidateList)
#     return jsonify({"result":'success',"ID":vote_id,"title": vote_title,'ddl':vote_ddl,'type': vote_type,'choice':vote_candidateList})

# # 判断uid是否在当前投票活动的合法列表里
# @app.route("/voter/if_join_vote", methods=["POST"])
# def join_vote_if():
#     data = request.get_data()
#     js = json.loads(data)
#     username = js.get("name", 0)
#     password = js.get("password", 0)
#     vote_id = js.get("ID", 0)
#     userid = js.get("uid", 0)

#     _, signer = valid_login(username, password)
#     if signer is None:
#         return jsonify({"result": 'error1'})

#     vote_addr = get_vote_addr(vote_id, signer)
#     if addr_vaild(vote_addr):
#         return jsonify({"result": 'error2'})

#     voterlist = getVoteWeList(vote_addr, signer)
#     if userid not in voterlist:
#         return jsonify({"result":'error3'})

#     Wevoter = getVoterWe(vote_addr, userid, signer)
#     # print("sdsdsdsdsdsdd",Wevoter[1],type(Wevoter))

#     if Wevoter[1] is not '0':
#         # print("existexistexistexistexistexist")
#         return jsonify({"result":'exist',"type":"we"})
    
#     Wepara = getVoteWePara(vote_addr)
#     # print("sdsdsdsdsdsdd",Wepara[0])

#     return jsonify({"result":'success', "encryption":Wepara, "addr":vote_addr,"type":"we"})

@app.route("/voteravc/avc_upload_pk", methods=["POST"])
def avc_upload_pk():
    data = request.get_data()
    js = json.loads(data)
    username = js.get("name", 0)
    password = js.get("password", 0)
    vote_addr = js.get("voteaddr", 0)
    userid = js.get("uid", 0)
    rpub = js.get("rpub", 0)
    # spub = trans_str(spub)
    epub = js.get("epub", 0)

    print("dsdsdsdsdsdmiyao sm sds",rpub,epub)

    _, signer = valid_login(username, password)
    if signer is None:
        return jsonify({"result": 'error1'})

    try:
        call_contract(
                vote_addr,"Vote","updatepubkey", args=[userid, rpub, epub], signer=signer
            )
    except Exception as e:
        print(e)
        return jsonify({"result": 'error2'})

    # 公钥写入数据库
    # user = User.query.filter(User.username == username).first()
    # if user:
    #     # print("zheshidasidhaosdhoasds:",spub,type(spub),userid)
    #     try:
    #         user.We_sign_pubs=spub
    #         user.We_enc_pubs=epub
    #         db.session.commit()
    #     except Exception as e:
    #         traceback.print_exc()
    #         db.session.rollback()

    return jsonify({"result":'success',"vote":"avec"})

# 注意wasm调用
@app.route("/voteravc/upload_avcPK", methods=["POST"])
def upload_avcPK():
    data = request.get_data()
    js = json.loads(data)
    PK = js.get("PK", 0)
    vote_addr = js.get("addr", 0)
    setavcPK(vote_addr,PK)
    return jsonify({"result":'success',"vote":"avec"})


# # 开始投票 判断是否合法用户、是否已经加入投票、系统公钥是否建立、判断并拒绝用户重复投票
# @app.route("/voter/start_vote", methods=["POST"])
# def start_vote():
#     data = request.get_data()
#     js = json.loads(data)
#     username = js.get("name", 0)
#     password = js.get("password", 0)
#     vote_id = js.get("ID", 0)
#     userid = js.get("uid", 0)

#     _, signer = valid_login(username, password)
#     if signer is None:
#         return jsonify({"result": 'error1'})

#     vote_addr = get_vote_addr(vote_id, signer)
#     if addr_vaild(vote_addr):
#         return jsonify({"result": 'error2'})

#     voterlist = getVoteWeList(vote_addr, signer)

#     if userid not in voterlist:
#         return jsonify({"result":'error3'})

#     allballot= getWeBallot(vote_addr, signer)
#     for hasvote in allballot:
#         if hasvote[0] == userid:
#             return jsonify({"result":'hasvote'})

    
#     Wevoter = getVoterWe(vote_addr, userid, signer)
#     # print("sdsdsdsdsdsdd",Wevoter[1],type(Wevoter))

#     if Wevoter[1] is '0':
#         return jsonify({"result":'add',"type":"we"})

#     PKlist = if_We_PK(vote_addr)

#     # Wevoter = getVoterWe(vote_addr, userid, signer)
#     # print("sdsdsdsdsdsdd",PK)

#     if not PKlist:
#         return jsonify({"result":'wait',"type":"we"})

#     PK =  getCounter(vote_addr)
#     PK = PK[0]
#     # if hasvote:
#     #     return jsonify({"result":'hasvote'})

#     WevoteInfo = list(get_vote_info(vote_addr,"VoteWe",signer))
#     WevoteInfo[1] = time_decoder(WevoteInfo[1])
#     # Wepara = getVoteWePara(vote_addr, signer)
#     # print("sdsdsdsdsdsdd",Wepara[0])

#     # Wepara = getVoteWePara(vote_addr, signer)
#     return jsonify({"result":'success',"type":"we","addr":vote_addr,"weight":Wevoter[3],"voteinfo":WevoteInfo,"PKlist":PKlist,"PK":PK})


# @app.route("/voter/upload_wePK", methods=["POST"])
# def upload_wePK():
#     data = request.get_data()
#     js = json.loads(data)
#     PK = js.get("PK", 0)
#     vote_addr = js.get("addr", 0)
#     setCounterPK(vote_addr,PK,'0','0')
#     return jsonify({"result":'success',"vote":"we"})

# 灵活投票
@app.route("/voteravc/add_avc_ballot", methods=["GET", "POST"])
def add_avcballot():
    data = request.get_data()
    js = json.loads(data)
    username = js.get("name", 0)
    password = js.get("password", 0)
    userid = js.get("uid", 0)

    _, signer = valid_login(username, password)
    # vote_candidate = trans_list(voter.current_vote_candidate)
    if signer is None:
        return jsonify({"result": 'error1'})

    vote_addr = js.get("addr", 0)
    if addr_vaild(vote_addr):
        return jsonify({"result": 'error2'})

    ballot_str = js.get("ballotstr")
    # print("sda:",type(ballot_str))
    # print("zhuanhuan:",ballot_str)
    signature = js.get("signature")
    

    try:
        call_contract(
            vote_addr,"Vote","addBallot", args=[ballot_str, signature, userid], signer=signer
            )
    except Exception as e:
        print(e)
        return jsonify({"result": 'error3'})

    return jsonify({"result": 'success',"addr":vote_addr})

#     # vote = js.get("vote",0)
#     # if vote == 'we':
#     #     try:
#     #         call_contract(
#     #             vote_addr,"VoteWe","addBallot", args=[ballot_str, signature], signer=signer
#     #         )
#     #     except Exception as e:
#     #         print(e)
#     #         return jsonify({"result": 'error3'})
#     #     return jsonify({"result": 'success'})

#     # try:
#     #     call_contract(
#     #             vote_addr,"Vote","addBallot", args=[ballot_str, signature], signer=signer
#     #         )
#     # except Exception as e:
#     #        return jsonify({"result": 'error3'})
#     # return jsonify({"result": 'success'})

# # 恢复秘密份额，权限管理
# @app.route("/voter/if_add_share", methods=["POST"])
# def if_add_share():
#     data = request.get_data()
#     js = json.loads(data)
#     username = js.get("name", 0)
#     password = js.get("password", 0)
#     vote_id = js.get("ID", 0)
#     userid = js.get("uid", 0)

#     _, signer = valid_login(username, password)
#     if signer is None:
#         return jsonify({"result": 'error1'})

#     vote_addr = get_vote_addr(vote_id, signer)
#     if addr_vaild(vote_addr):
#         return jsonify({"result": 'error2'})

#     voterlist = getVoteWeList(vote_addr, signer)
#     allballot= getWeBallot(vote_addr, signer)
#     allshare = if_Allshare(vote_addr)

#     print("allshareallshareallshareallshareallshare:",allshare)
#     if userid in voterlist:
#         Wevoter = getVoterWe(vote_addr, userid, signer)
#         if Wevoter[4] is '0':
#             return jsonify({"result":'doshare',"type":"we","ballot":allballot,"addr":vote_addr})

#         if not allshare:
#             return jsonify({"result":'wait'})

#         return jsonify({"result":'success', "ballot":allballot, "addr":vote_addr})
        
    
#     # Wepara = getVoteWePara(vote_addr, signer)
#     # print("sdsdsdsdsdsdd",Wepara[0])
#     # allballot= getWeBallot(vote_addr, signer)

#     return jsonify({"result":'success', "ballot":allballot, "addr":vote_addr})

# # 上传share，C1，C2
@app.route("/voteravc/upload_share", methods=["POST"])
def upload_avcshare():
    data = request.get_data()
    js = json.loads(data)

    username = js.get("name", 0)
    password = js.get("password", 0)
    vote_addr = js.get("addr", 0)
    userid = js.get("uid", 0)

    share = js.get("share", 0)

    # print("sdsdsdsds",vote_addr)

    _, signer = valid_login(username, password)
    if signer is None:
        return jsonify({"result": 'error1'})

    try:
        call_contract(
                vote_addr,"Vote","setShare", args=[userid, share], signer=signer
            )
    except Exception as e:
        print(e)
        return jsonify({"result": 'error2'})

    # setCounter(vote_addr,'0',C1,C2)

    return jsonify({"result":'success',"vote":"avc"})

# # 获取结果
@app.route("/voteravc/get_avc_result", methods=["POST"])
def get_avc_result():

    data = request.get_data()
    js = json.loads(data)

    username = js.get("name", 0)
    password = js.get("password", 0)
    vote_addr = js.get("addr", 0)

    _, signer = valid_login(username, password)
    if signer is None:
        return jsonify({"result": 'error1'})

    Para = getVoteAvcPara(vote_addr)
    # C2 = getCounter(vote_addr)
    # C2 = C2[2]
    allshare = if_avc_kshare(vote_addr, signer)

    PK = getavcPK(vote_addr)

    # allballot= getAvcBallot(vote_addr, signer)
    print("allshareallshareallshareallshareallshare:",PK)
    if not allshare:
        return jsonify({"result":'wait'})

    choice = get_vote_info_candidate(vote_addr, signer)
    return jsonify({"result":'success',"vote":"avc","para":Para, "PK":PK, "allshare":allshare, "choice":choice})

