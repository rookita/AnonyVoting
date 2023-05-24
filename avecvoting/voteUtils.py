from typing import Tuple

from sqlalchemy import false, true
from blockchain import call_contract, call_contract2
from models import db, Contract
import hashlib, time, re
from blockchain import signin_account,create_account


# 判断时间格式合法
def time_vaild_format(_time):
    try:
        time.strptime(_time, "%Y-%m-%d %H:%M:%S")
        pass
    except Exception as e:
        return True


# 判断返回空地址合约
def addr_vaild(_addr):
    if "0x0000000000000000000000000000000000000000" == _addr:
        return True
    else:
        return False


# 获取现在时间的时间戳
def get_time_now():
    now_time_stamp = time_encoder(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    )
    return now_time_stamp


# 解析str时间 生成时间戳
def time_encoder(_time):
    time_array = time.strptime(_time, "%Y-%m-%d %H:%M:%S")
    other_style_time = int(time.mktime(time_array))
    return other_style_time


# 转为str时间
def time_decoder(time_stamp):
    time_array = time.localtime(time_stamp)
    other_style_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return other_style_time


def get_hash(str):
    md5 = hashlib.md5()
    md5.update(str.encode("utf-8"))
    return md5.hexdigest()


def get_now(vote_addr, signer):
    try:
        res = call_contract2(vote_addr, "Vote", "getNow", args=[], signer=signer)
    except Exception:
        return None
    return res


# 获取选票
def get_ballots(vote_addr, name, signer):
    # print("the vote addr is ", vote_addr)
    try:
        res = call_contract2(vote_addr, name, "getBallots", args=[], signer=signer)
        print("fanhuizhi:",res)
        ballot = res[0]
        print("xaunpiao",ballot)
    except Exception:
        return None
    return ballot


# 获取发起的投票地址
def get_vote_addr(vote_id, signer):
    management_addr = (
        db.session.query(Contract).filter(Contract.name == "Management").first().addr
    )
    try:
        vote_addr = call_contract(
            management_addr, "Management", "getVoteAddr", args=[vote_id], signer=signer
        )
        vote_addr = vote_addr[0]
    except Exception:
        return None
    return vote_addr


# 获取投票所有id
def get_vote_id_list(signer):
    management_addr = (
        db.session.query(Contract).filter(Contract.name == "Management").first().addr
    )
    try:
        vote_id_list = call_contract(
            management_addr, "Management", "getVoteList", args=[], signer=signer
        )
        vote_id_list = vote_id_list[0]
        # list_to_str = trans_str(vote_id_list)
    except Exception:
        return None
    return vote_id_list


# 判断id是否为avec
def get_vote_type(vote_id,signer):
    management_addr = (
        db.session.query(Contract).filter(Contract.name == "Management").first().addr
    )
    try:
        vote_type = call_contract(
            management_addr, "Management", "getVoteType", args=[vote_id], signer=signer
        )
    except Exception as e:
        print(e)

    return vote_type[0]

# 获取id_list判断id是否在list中
def get_if_vote_id_list(signer):
    management_addr = (
        db.session.query(Contract).filter(Contract.name == "Management").first().addr
    )
    try:
        vote_id_list = call_contract(
            management_addr, "Management", "getVoteList", args=[], signer=signer
        )
        vote_id_list = vote_id_list[0]
    except Exception:
        return None
    return vote_id_list


# # 获取投票信息
# def get_vote_info(vote_addr, name, signer):
#     if name == 'Vote':
#         try:
#             vote_title, vote_ddl, vote_type = call_contract(
#             vote_addr, name, "getVoteInfo", args=[], signer=signer
#         )
#         except Exception as e:
#             print(e)
#         return vote_title, vote_ddl,  vote_type

#     try:
#         vote_title, vote_ddl, vote_content = call_contract(
#             vote_addr, name, "getVoteInfo", args=[], signer=signer
#         )
#     except Exception as e:
#         print(e)
#     return vote_title, vote_ddl, vote_content

# 获取权重投票信息
def get_wevote_info(vote_addr,signer):
    try:
        vote_title, vote_ddl, vote_content = call_contract(
        vote_addr, "VoteWe", "getVoteInfo", args=[], signer=signer
        )
    except Exception as e:
        print(e)
    return vote_title, vote_ddl, vote_content



# list转化str
def trans_str(_list):
    list_str = ""
    list_str = ",".join([str(x) for x in _list])
    return list_str


# str转化list
def trans_list(_str):
    _list = []
    _list = [str(x) for x in (_str.split(","))]
    return _list

# 获取投票者列表，判断是否有投票权限
def getVoteWeList(vote_addr, signer):
    print(vote_addr)
    try:
        voter_list = call_contract2(
            vote_addr, "VoteWe", "getVoterList", args=[], signer=signer
        )
        # print("sdsdsdsdsdsdsd1111111111111111111111",voter_list,type(voter_list[0]))
    # except Exception:
    #     return None
    except Exception as e:
            print(e)
    print("投票者列表",voter_list)
    return voter_list[0]

# 返回(P Q G)
def getVoteWePara(vote_addr):
    signer = create_account("USTC", 123456)
    try:
        We_para = call_contract2(
            vote_addr, "VoteWe", "getPara", args=[], signer=signer
        )
        # print("sdsdsdsdsdsdsd1111111111111111111111",We_para)
       
    # except Exception:
    #     return None
    except Exception as e:
            print(e)
    return We_para

# 返回权重投票者信息
def getVoterWe(vote_addr, uid, signer):
    try:
        voter = call_contract(
            vote_addr, "VoteWe", "getVoter", args=[uid], signer=signer
        )
        # print("sdsdsdsdsdsdsd1111111111111111111111",voter)
       
    # except Exception:
    #     return None
    except Exception as e:
            print(e)
    return voter

# 计算并返回合公钥PK
def if_We_PK(vote_addr):
    signer = create_account("USTC", 123456)
    try:
        all_voters = call_contract2(
            vote_addr, "VoteWe", "getAllVoter", args=[], signer=signer
        )
        print("sdsdsdsdsdsdsd1111111111111111111111",all_voters[0])
    except Exception as e:
            print(e)
    
    elgamal_pubs = []
    for i in all_voters[0]:
        if i[1] is '0':
            # print("sdsdsdsdsdsdsd1111111111111111111111",i[1])
            return False
        else:
            elgamal_pubs.append(i[2])
    return elgamal_pubs

def getWeBallot(vote_addr, signer):
    try:
        ballot = call_contract2(
            vote_addr, "VoteWe", "getAllBallots", args=[], signer=signer
        )
        # print("sdsdsdsdsdsdsd1111111111111111111111",ballot)
       
    # except Exception:
    #     return None
    except Exception as e:
            print(e)
    return ballot[0]

def setCounter(vote_addr,pk,c1,c2):
    signer = create_account("USTC", 123456)
    try:
        call_contract(
            vote_addr, "VoteWe", "setCounter", args=[pk, c1, c2], signer=signer
        )
        # print("sdsdsdsdsdsdsd1111111111111111111111",counter[0])
    except Exception as e:
            print(e)

def getCounter(vote_addr):
    signer = create_account("USTC", 123456)
    try:
        counter = call_contract2(
            vote_addr, "VoteWe", "getCounter", args=[], signer=signer
        )
        # print("sdsdsdsdsdsdsd1111111111111111111111",counter[0])
    except Exception as e:
            print(e)
    return counter[0]

def if_Allshare(vote_addr):
    signer = create_account("USTC", 123456)
    try:
        all_voters = call_contract2(
            vote_addr, "VoteWe", "getAllVoter", args=[], signer=signer
        )
        # print("sdsdsdsdsdsdsd1111111111111111111111",all_voters[0])
    except Exception as e:
            print(e)
    
    for i in all_voters[0]:
        print("sdsdsdsdsdsdsd",type(i[4]))
        if i[4] == '0':
           
            # print("sdsdsdsdsdsdsd1111111111111111111111",i[1])
            return False
    
    try:
        allshare = call_contract2(
            vote_addr, "VoteWe", "getAllShare", args=[], signer=signer
        )
        print("wwwwwwwwwwwwww",allshare)
    except Exception as e:
        print(e)
    
    return allshare[0]

def setCounterPK(vote_addr,pk,c1,c2):
    signer = create_account("USTC", 123456)
    try:
        call_contract(
            vote_addr, "VoteWe", "setCounter", args=[pk, c1, c2], signer=signer
        )
        # print("sdsdsdsdsdsdsd1111111111111111111111",counter[0])
    except Exception as e:
            print(e)

