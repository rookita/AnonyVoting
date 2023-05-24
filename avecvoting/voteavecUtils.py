from typing import Tuple
from sqlalchemy import false, true
from blockchain import call_contract, call_contract2
from models import db, Contract
import hashlib, time, re
from blockchain import signin_account,create_account

# 获取投票者列表，判断是否有投票权限
def getVoteAvcList(vote_addr, signer):
    try:
        voter_list = call_contract(
            vote_addr, "Vote", "getVoterList", args=[], signer=signer
        )
        print("sdsdsdsdsdsdsd1111111111111111111111",voter_list,type(voter_list[0]))
        # voter_list = voter_list[0]
    # except Exception:
    #     return None
    except Exception as e:
            print("error:",e)
    return voter_list[0]

# 获取投票者
def getVoterAvc(vote_addr, uid, signer):
    try:
        voter = call_contract2(
            vote_addr, "Vote", "getVoter", args=[uid], signer=signer
        )
        # print("sdsdsdsdsdsdsd1111111111111111111111",voter)
       
    # except Exception:
    #     return None
    except Exception as e:
            print(e)
    return voter[0]

# 获取投票参数
def getVoteAvcPara(vote_addr):
    signer = create_account("USTC", 123456)
    try:
        para = call_contract2(
            vote_addr, "Vote", "getPara", args=[], signer=signer
        )
        # print("sdsdsdsdsdsdsd1111111111111111111111",We_para)
       
    # except Exception:
    #     return None
    except Exception as e:
            print(e)
    return para[0]

# 获取所有
def getAvcBallot(vote_addr, signer):
    try:
        ballot = call_contract2(
            vote_addr, "Vote", "getAllBallots", args=[], signer=signer
        )
        # print("sdsdsdsdsdsdsd1111111111111111111111",ballot)
       
    # except Exception:
    #     return None
    except Exception as e:
            print(e)
    return ballot[0]

# 计算并返回all公钥PK
def if_Avc_PK(vote_addr):
    signer = create_account("USTC", 123456)
    try:
        all_epub = call_contract(
            vote_addr, "Vote", "getAllEpub", args=[], signer=signer
        )
        # print("sdsdsdsdsdsdsd1111111111111111111111",all_voters[0])
    except Exception as e:
            print(e)
    
    # if '0' in all_epub[0]:
    #     return False

    return all_epub[0]

# 获取所有的环签名公钥
def get_all_rpub(vote_addr):

    signer = create_account("USTC", 123456)
    try:
        all_spub = call_contract(
            vote_addr, "Vote", "getAllSpub", args=[], signer=signer
        )
        # print("sdsdsdsdsdsdsd1111111111111111111111",all_voters[0])
    except Exception as e:
            print(e)
    
    # if '0' in all_epub[0]:
    #     return False

    return all_spub[0]

#公钥PK
def setavcPK(vote_addr,pk):
    signer = create_account("USTC", 123456)
    try:
        call_contract(
            vote_addr, "Vote", "setPK", args=[pk], signer=signer
        )
    except Exception as e:
            print(e)

#返回公钥PK
def getavcPK(vote_addr):
    signer = create_account("USTC", 123456)
    try:
        PK1 = call_contract(
            vote_addr, "Vote", "getPK", args=[], signer=signer
        )
    except Exception as e:
            print(e)
    return PK1

# 判断是否满足门限
def if_avc_kshare(vote_addr,signer):
    try:
        all_share = call_contract(
            vote_addr, "Vote", "getAllShare", args=[], signer=signer
        )
        # print("sdsdsdsdsdsdsd1111111111111111111111",all_voters[0])
    except Exception as e:
            print(e)

    para = getVoteAvcPara(vote_addr)
    k = para[4]
    # kshare = []
    # for i in allshare[0]:
    #     if i is not '0':
    #         kshare.append(i)
    if len(all_share[0]) < k:
        return False
    return all_share[0]

# 返回投票基本信息
def get_Avcvote_info(vote_addr,signer):
    try:
        vote_title, vote_ddl, vote_type = call_contract(
        vote_addr, "Vote", "getVoteInfo", args=[], signer=signer
        )
    except Exception as e:
        print(e)
    return vote_title, vote_ddl, vote_type

# 返回投票选项
# 获取投票信息,返回字符串类型candidate
def get_vote_info_candidate(vote_addr, signer):
    try:
        vote_candidate_list = call_contract(
            vote_addr, "Vote", "getVoteCandidate", args=[], signer=signer
        )
        # print(vote_candidate_list)
        # print(type(vote_candidate_list))
        # vote_candidate_list = vote_candidate_list[0]
        # print(vote_candidate_list)
        # print(type(vote_candidate_list))
        # list_to_str = trans_str(vote_candidate_list)
    except Exception:
        return None
    return vote_candidate_list[0]