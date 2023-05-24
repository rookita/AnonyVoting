#提供区块链上合约查询相关接口
import sys
import json
sys.path.append("/home/ubuntu/python-sdk")

from client.bcosclient import BcosClient
from blockchain import call_contract,call_contract2

contract_name = "Vote"
def check_address(address): #检查地址是否有效
    client = BcosClient()
    try:
        res = client.getCode(address)
        return True, res
    except:
        return False, None

def getVoter(address,id):
    voter = call_contract(address,contract_name,"getVoter",[id])
    voter_dic = {"uid":voter[0], "spub":voter[1], "epub":voter[2], "weight":voter[3], "share":voter[4]}
    voter_json = json.dumps(voter_dic)
    return voter_json

def getAllVoter(address):
    AllVoter = call_contract2(address,contract_name,"getAllVoter")
    voters_dic = []
    for voter in AllVoter[0]:
        voter = list(voter)
        voters_dic.append({"uid":voter[0], "spub":voter[1], "epub":voter[2], "weight":voter[3], "share":voter[4]})
    return voters_dic

def getPara(address):
    para = call_contract(address, contract_name, "getPara")
    para = list(para)
    para_dic = {"P":para[0],"Q":para[1], "G":para[2]}
    para_json = json.dumps(para_dic)
    return para_json

def getCounter(address):
    counter = call_contract2(address, contract_name, "getCounter")
    return list(counter[0])

def getShare(address,id):
    share = call_contract(address, contract_name, "getShare", [id])
    return list(share)

def getAllShare(address):
    AllShare = call_contract(address, contract_name, "getAllShare")
    return list(AllShare)

def getRes(address):
    res = call_contract(address, contract_name, "getRes")
    return res

if __name__ == "__main__":
    address = ""
    id = "B"
    success, res = check_address(address)
    #print(res)
    if success:
        voter_json = getVoter(address,id)
        #print(voter_json)
        AllVoter = getAllVoter(address)
        #print(AllVoter)
        para_json = getPara(address)
        #print(para_json)
        counter = getCounter(address)
        #print(counter)
        share = getShare(address,id)
        #print(share)
        AllShare = getAllShare(address)
        #print(AllShare)
        res = getRes(address)
        #print(res)