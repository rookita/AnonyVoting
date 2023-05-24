pragma solidity ^0.4.25;
pragma experimental ABIEncoderV2;

contract Vote {
    struct ballot {
        string uid;
        string ballotStr;
        string signature;
    }

    struct Voter {
        string uid;
        string rpub;
        string epub;
        string share;
    }

    struct Para {
        string P;
        string Q;
        string G;
        int256 n;
        int256 k;
    }

    string[] voterlist;
    string[] allShare;
    string[] allEpub;
    string[] allSpub;
    Para para;
    Voter[] voter;
    string PK;
    mapping(string => uint256) findVoter;

    string[] candidateList;
    string voteTitle;
    uint256 voteDDL;
    string voteType;
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

    function setVoteInfo(
        string _voteTitle,
        uint256 _voteDDL,
        string _voteType
    ) public onlyManager {
        voteTitle = _voteTitle;
        voteDDL = _voteDDL;
        voteType = _voteType;
    }

    function setVoteCandidate(string[] _candidateList) public onlyManager {
        candidateList = _candidateList;
    }

    function setVoterInfo(
        string memory uid,
        string memory rpub,
        string memory epub,
        string share
    ) public onlyManager {
        voter.push(Voter(uid, rpub, epub, share));
        findVoter[uid] = voter.length - 1;
        voterlist.push(uid);
    }

    function updatepubkey(
        string uid,
        string rpub,
        string epub
    ) public {
        voter[findVoter[uid]].rpub = rpub;
        voter[findVoter[uid]].epub = epub;
        allEpub.push(epub);
        allSpub.push(rpub);
    }

    function setPK(string pk) public {
        PK = pk;
    }

    function setShare(string uid, string share) public {
        voter[findVoter[uid]].share = share;
        allShare.push(share);
    }

    function setPara(
        string _P,
        string _Q,
        string _G,
        int256 n,
        int256 k
    ) public onlyManager {
        para.P = _P;
        para.Q = _Q;
        para.G = _G;
        para.n = n;
        para.k = k;
        // push(Para(_P, _Q, _G, n, k));
    }

    function getVoteCandidate() public view returns (string[]) {
        return candidateList;
    }

    function getVoteInfo()
        public
        view
        returns (
            string,
            uint256,
            string
        )
    {
        return (voteTitle, voteDDL, voteType);
    }

    ballot[] Ballots;

    function addBallot(
        string _ballotStr,
        string _signature,
        string uid
    ) public beforeDeadline {
        Ballots.push(ballot(uid, _ballotStr, _signature));
    }

    function getAllBallots() public view returns (ballot[]) {
        return Ballots;
    }

    function getNow() public view returns (uint256) {
        return now;
    }

    function getAllShare() public view returns (string[]) {
        return allShare;
    }

    function getAllEpub() public view returns (string[]) {
        return allEpub;
    }

    function getAllSpub() public view returns (string[]) {
        return allSpub;
    }

    function getVoter(string memory uid) public view returns (Voter) {
        return voter[findVoter[uid]];
    }

    function getVoterList() public view returns (string[]) {
        return voterlist;
    }

    function getPara() public view returns (Para) {
        return para;
    }

    function getPK() public view returns (string) {
        return PK;
    }
}
