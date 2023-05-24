pragma solidity ^0.4.25;
pragma experimental ABIEncoderV2;
import "./Vote.sol";
import "./VoteWe.sol";

contract Management {
    mapping(address => string[]) voteListMap;
    mapping(string => address) voteAddrMap;
    mapping(string => string) RecordVoteType;

    function createVote(
        string _voteId,
        address _voteAddr,
        string _voteTitle,
        uint256 _voteDDL,
        string _voteType,
        string _type
    ) public {
        RecordVoteType[_voteId] = _type;
        voteAddrMap[_voteId] = _voteAddr;
        voteListMap[msg.sender].push(_voteId);
        Vote(_voteAddr).setVoteInfo(_voteTitle, _voteDDL, _voteType);
    }

    function createVoteCandidate(address _voteAddr, string[] _candidateList)
        public
    {
        Vote(_voteAddr).setVoteCandidate(_candidateList);
    }

    function createVoteWe(
        string _voteId,
        address _voteAddr,
        string _voteTitle,
        uint256 _voteDDL,
        string _voteContent,
        string _type
    ) public {
        RecordVoteType[_voteId] = _type;
        voteAddrMap[_voteId] = _voteAddr;
        voteListMap[msg.sender].push(_voteId);
        VoteWe(_voteAddr).setVoteInfo(_voteTitle, _voteDDL, _voteContent);
    }

    function getVoteAddr(string _voteId) public view returns (address) {
        return voteAddrMap[_voteId];
    }

    function getVoteList() public view returns (string[]) {
        return voteListMap[msg.sender];
    }

    function getVoteType(string _voteId) public view returns (string) {
        return RecordVoteType[_voteId];
    }
}
