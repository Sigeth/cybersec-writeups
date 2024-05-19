// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TutoBlockchain {
    address private s_owner;

    constructor() {
        s_owner = msg.sender;
    }

    function getOwnership() external {
        s_owner = msg.sender;
    }

    function getOwner() external view returns(address) {
        return s_owner;
    }
}
