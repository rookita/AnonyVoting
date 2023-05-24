from base64 import encode
from ctypes import resize
import imp
import json
from inspect import signature
from logging import NOTSET
from operator import ipow
from re import I
import traceback
from cryptography.hazmat import backends
from flask import request, render_template, session, flash, url_for,jsonify
from werkzeug.utils import redirect
from user import valid_login
from __init__ import app
from client_config import client_config
from blockchain import call_contract, create_account, signin_account, call_contract2
from models import Contract,db,User
from voteUtils import (
    get_vote_type,
    getVoteWeList,
    getVoteWePara,
    getVoterWe,
    if_We_PK,
    getWeBallot,
    setCounter,
    getCounter,
    if_Allshare,
    setCounterPK,
    get_vote_addr,
    addr_vaild,
    get_wevote_info,
    time_decoder,
    trans_str
)

from voteavecUtils import(
    getVoteAvcList,
    getVoterAvc,
    getVoteAvcPara,
    getAvcBallot,
    getavcPK,
    if_avc_kshare,
    if_Avc_PK,
    get_Avcvote_info,
    get_vote_info_candidate,
    get_all_rpub,
    
)


# 判断uid是否在当前投票活动的合法列表里
@app.route("/voter/if_join_vote", methods=["POST"])
def join_vote_if():
    data = request.get_data()
    js = json.loads(data)
    username = js.get("name", 0)
    password = js.get("password", 0)
    vote_id = js.get("ID", 0)
    userid = js.get("uid", 0)

    _, signer = valid_login(username, password)
    if signer is None:
        return jsonify({"result": 'error1'})

    vote_addr = get_vote_addr(vote_id, signer)
    if addr_vaild(vote_addr):
        return jsonify({"result": 'error2'})

    if get_vote_type(vote_id, signer) == 'we':
        voterlist = getVoteWeList(vote_addr, signer)
        if userid not in voterlist: 
            return jsonify({ "result" :'error3' })

        Wevoter = getVoterWe(vote_addr, userid, signer)
        
        if Wevoter[1] is not '0':
            return jsonify({"result":'exist',"type":"we"})

        Wepara = getVoteWePara(vote_addr)
        return jsonify({"result":'success', "encryption":Wepara, "addr":vote_addr,"type":"we"})


    voterlist1 = getVoteAvcList(vote_addr, signer)
    if userid not in voterlist1:
        return jsonify({"result":'error3'})

    voter = getVoterAvc(vote_addr, userid, signer)
    if voter[1] is not '0':
        # print("existexistexistexistexistexist")
        return jsonify({"result":'exist',"type":"avec"})

    para = getVoteAvcPara(vote_addr)
    return jsonify({"result":'success', "encryption":para, "addr":vote_addr,"type":"avec"})
    


# 开始投票 判断是否合法用户、是否已经加入投票、系统公钥是否建立、判断并拒绝用户重复投票
@app.route("/voter/start_vote", methods=["POST"])
def start_vote():
    data = request.get_data()
    js = json.loads(data)
    username = js.get("name", 0)
    password = js.get("password", 0)
    vote_id = js.get("ID", 0)
    userid = js.get("uid", 0)

    _, signer = valid_login(username, password)
    if signer is None:
        return jsonify({"result": 'error1'})

    vote_addr = get_vote_addr(vote_id, signer)
    if addr_vaild(vote_addr):
        return jsonify({"result": 'error2'})

    if get_vote_type(vote_id, signer) == 'we':
        voterlist = getVoteWeList(vote_addr, signer)
        if userid not in voterlist: 
            return jsonify({ "result" :'error3' })
        
        allballot= getWeBallot(vote_addr, signer)
        for hasvote in allballot:
            if hasvote[0] == userid:
                return jsonify({"result":'hasvote'})

        Wevoter = getVoterWe(vote_addr, userid, signer)
        
        if Wevoter[1] is '0':
            return jsonify({"result":'add',"type":"we"})

        PKlist = if_We_PK(vote_addr)
        if not PKlist:
            return jsonify({"result":'wait',"type":"we"})

        PK =  getCounter(vote_addr)
        PK = PK[0]
        WevoteInfo = list(get_wevote_info(vote_addr, signer))
        WevoteInfo[1] = time_decoder(WevoteInfo[1])
        return jsonify({"result":'success',"type":"we","addr":vote_addr,"weight":Wevoter[3],"voteinfo":WevoteInfo,"PKlist":PKlist,"PK":PK})


    voterlist1 = getVoteAvcList(vote_addr, signer)
    if userid not in voterlist1:
        return jsonify({"result":'error3'})

    
    allballot= getAvcBallot(vote_addr, signer)
    for hasvote in allballot:
        if hasvote[0] == userid:
            return jsonify({"result":'hasvote'})

    voter = getVoterAvc(vote_addr, userid, signer)
    if voter[1] is '0':
        return jsonify({"result":'add',"type":"avec"})

    PKlist = if_Avc_PK(vote_addr)
    
    if len(PKlist) != len(voterlist1):
        return jsonify({"result":'wait',"type":"avec"})

    AvcvoteInfo = list(get_Avcvote_info(vote_addr, signer))
    AvcvoteInfo[1] = time_decoder(AvcvoteInfo[1])
    avcPK =  getavcPK(vote_addr)[0]

    choice = get_vote_info_candidate(vote_addr, signer)
    para = getVoteAvcPara(vote_addr)
    allrpub = get_all_rpub(vote_addr)
    print("返回格式错")
    return jsonify({"result":'success',"type":"avec","addr":vote_addr,"voteinfo":AvcvoteInfo,"PKlist":PKlist,"PK":avcPK,"choice":choice,"para":para,"rpub":allrpub})


# 恢复秘密份额，权限管理
@app.route("/voter/if_add_share", methods=["POST"])
def if_add_share():
    data = request.get_data()
    js = json.loads(data)
    username = js.get("name", 0)
    password = js.get("password", 0)
    vote_id = js.get("ID", 0)
    userid = js.get("uid", 0)

    _, signer = valid_login(username, password)
    if signer is None:
        return jsonify({"result": 'error1'})

    vote_addr = get_vote_addr(vote_id, signer)
    print(vote_addr)
    if addr_vaild(vote_addr):
        return jsonify({"result": 'error2'})
        

    if get_vote_type(vote_id, signer) == 'we':
        voterlist = getVoteWeList(vote_addr, signer)
        allballot= getWeBallot(vote_addr, signer)
        allshare = if_Allshare(vote_addr)
        WevoteInfo = list(get_wevote_info(vote_addr, signer))
        WevoteInfo[1] = time_decoder(WevoteInfo[1])

        if userid not in voterlist:
            return jsonify({"result":'success', "ballot":allballot,"voteinfo":WevoteInfo, "type":"we", "addr":vote_addr})
        
        Wevoter = getVoterWe(vote_addr, userid, signer) 
        if Wevoter[4] is '0':
            return jsonify({"result":'doshare',"type":"we","ballot":allballot,"voteinfo":WevoteInfo,"addr":vote_addr})
            
        if not allshare:
            return jsonify({"result":'wait', "type":"we"})
        return jsonify({"result":'success', "ballot":allballot,"voteinfo":WevoteInfo, "type":"we", "addr":vote_addr})


    voterlist1 = getVoteAvcList(vote_addr, signer)
    allballot= getAvcBallot(vote_addr, signer)
    print(allballot)
    choice = trans_str(get_vote_info_candidate(vote_addr, signer))

    AvcvoteInfo = list(get_Avcvote_info(vote_addr, signer))
    AvcvoteInfo[1] = time_decoder(AvcvoteInfo[1])
    if userid not in voterlist1:
        return jsonify({"result":'success', "ballot":allballot, "type":"avc", "addr":vote_addr,"voteinfo":AvcvoteInfo,"choice":choice})

    ifshare = if_avc_kshare(vote_addr, signer)
    
    # if userid not in voterlist1:
    #     return jsonify({"result":'success', "ballot":allballot, "type":"avc", "addr":vote_addr})
    
    if not ifshare:
        Avcvoter = getVoterAvc(vote_addr, userid, signer)
        epub = if_Avc_PK(vote_addr)
        if Avcvoter[3] is '0':
            return jsonify({"result":'doshare',"type":"avc","ballot":allballot,"addr":vote_addr,"epub":epub,"voteinfo":AvcvoteInfo,"choice":choice})

        return jsonify({"result":'wait',"type":"avc"})

    return jsonify({"result":'success', "ballot":allballot, "type":"avc", "addr":vote_addr,"voteinfo":AvcvoteInfo,"choice":choice})


