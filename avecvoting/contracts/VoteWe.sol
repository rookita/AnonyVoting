pragma solidity ^0.4.25;
pragma experimental ABIEncoderV2;

contract VoteWe {
    struct ballot {
        string uid;
        string spub;
        uint8 weight;
        string ballotStr;
        string signature;
    }
    
    struct Voter{
        string uid;
        string spub;    //签名公钥
        string epub;    //加密公钥
        uint8 weight; 
        string share;   //C1 ^ x
    }
    
    struct Counter{
        string PK;
        string C1;
        string C2;
    }


    string P;
    string Q;
    string G;
    Counter counter;
    string PK;
    int256 res;
    string[] voterlist;
    string[] allShare;
    Voter[] voters;
    mapping(string => uint256) findVoter;
    string voteTitle;
    string voteContent;
    uint256 voteDDL;
    address manager;

    constructor() public {
        manager = msg.sender;
    }

    modifier onlyManager() {
        require(tx.origin == manager, "Only Manager can call this function !");
        _;
    }

    modifier beforeDeadline() {
        require(now < voteDDL * 1000, "Fail! Out of time!");
        _;
    }

    function getManager() public view returns (address) {
        return manager;
    }

    function setVoterInfo(string memory uid, string memory spub, string memory epub, uint8 weight,string share) public onlyManager{
        voters.push(Voter(uid, spub, epub, weight,share));
        findVoter[uid] = voters.length - 1;
        voterlist.push(uid);
    }

    function updatepubkey(string uid, string spub, string epub) public{
        voters[findVoter[uid]].spub = spub;
        voters[findVoter[uid]].epub = epub;
    }

    function setShare(string uid, string share) public {
        voters[findVoter[uid]].share = share;
        allShare.push(share);
    }

    function setPara(string _P, string _Q, string _G) public onlyManager{
        P = _P;
        Q = _Q;
        G = _G;
    }
    // pk : "12312abfcd213" unsolve
    function setCounter(string pk, string c1, string c2) public{
       counter.PK = pk;
       counter.C1 = c1;
       counter.C2 = c2;
    }

    function setRes(string res) public {
        res = res;
    }

    function setVoteInfo(string _voteTitle, uint256 _voteDDL, string _voteContent)
        public
        onlyManager
    {

        voteTitle = _voteTitle;
        voteDDL = _voteDDL;
        voteContent = _voteContent;
    }


    function getVoteInfo() public view returns (string, uint256,string) {
        return (voteTitle, voteDDL,voteContent);
    }

    ballot[] Ballots;

    function addBallot(string _ballotStr, string _signature, string uid, uint8 weight, string spub)
        public
        beforeDeadline
    {
        Ballots.push(ballot(uid ,spub, weight, _ballotStr, _signature));
    }

    function getAllBallots() public view returns (ballot[]) {
        return Ballots;
    }

    

    function getNow() public view returns (uint256) {
        return now;
    }

    function getVoter(string memory uid) public view returns(string,string,string,uint8,string){
        return (voters[findVoter[uid]].uid,voters[findVoter[uid]].spub,voters[findVoter[uid]].epub,voters[findVoter[uid]].weight,voters[findVoter[uid]].share);
    }

    function getAllVoter() public view returns(Voter[]){
        return voters;
    }
    function getPara() public view returns(string,string,string){
        return (P, Q, G);
    }
    
    function getCounter() public view returns(Counter){
        return counter;
    }


    function getShare(string uid) public view returns(string){
        return voters[findVoter[uid]].share;
    }

    function getAllShare() public view returns(string[]){
        return allShare;
    }

    function getRes() public view returns(int256){
        return res;
    }
     
    function getVoterList() public view returns (string[]){
        return voterlist;
    }
}
