// SPDX-License-Identifier: MIT
// ==============================================================================
// Author: Pranjal Yadav
// Email: 2k24.cs1l.2410719@gmail.com
// Phone: +91919920362
// GitHub: https://github.com/pranjal2410719
// LinkedIn: https://www.linkedin.com/in/-pranjal22/
// ==============================================================================
pragma solidity ^0.8.0;

contract MediBellRegistry {
    address public owner;

    struct RoundInfo {
        uint256 round;
        string cid;
        uint256 accuracy; // Store accuracy as scaled integer (e.g. 94.27% -> 9427)
        uint256 timestamp;
    }

    mapping(uint256 => RoundInfo) public rounds;
    uint256[] public roundNumbers;

    event RoundRegistered(
        uint256 indexed round,
        string cid,
        uint256 accuracy,
        uint256 timestamp
    );

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function registerRound(
        uint256 _round,
        string memory _cid,
        uint256 _accuracy
    ) public onlyOwner {
        require(rounds[_round].timestamp == 0, "Round already registered");

        rounds[_round] = RoundInfo({
            round: _round,
            cid: _cid,
            accuracy: _accuracy,
            timestamp: block.timestamp
        });
        roundNumbers.push(_round);

        emit RoundRegistered(_round, _cid, _accuracy, block.timestamp);
    }

    function getRoundCount() public view returns (uint256) {
        return roundNumbers.length;
    }

    function getRound(uint256 _round) public view returns (
        uint256 round,
        string memory cid,
        uint256 accuracy,
        uint256 timestamp
    ) {
        RoundInfo memory info = rounds[_round];
        return (info.round, info.cid, info.accuracy, info.timestamp);
    }
}
