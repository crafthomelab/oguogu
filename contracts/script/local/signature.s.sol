// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import {Script, console} from "forge-std/Script.sol";
import {OGUOGU} from "src/Oguogu.sol";
import {UUPSUpgradeable} from "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";
import {TestUSDT} from "src/misc/TestToken.sol";

contract DeployScript is Script {
    OGUOGU public oguogu;
    TestUSDT public testUSDT;

    function setUp() public {}

    function run() public {
        uint256 deployerPrivateKey = 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80;
        uint256 userPrivateKey = 0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d;

        // EIP-191 prefix
        string memory message = "hello";
        bytes memory messageBytes = abi.encodePacked(message);
        bytes memory prefix = "\x19Ethereum Signed Message:\n";
        bytes memory prefixedMessage = abi.encodePacked(prefix, uintToStr(messageBytes.length), messageBytes);

        // Hash the prefixed message
        bytes32 messageHash = keccak256(prefixedMessage);

        // Sign the message hash
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(userPrivateKey, messageHash);
        bytes memory signature = abi.encodePacked(r, s, v);

        console.logBytes(signature);
    }

    // Helper function to convert uint to string
    function uintToStr(uint256 v) internal pure returns (string memory str) {
        if (v == 0) {
            return "0";
        }
        uint256 j = v;
        uint256 len;
        while (j != 0) {
            len++;
            j /= 10;
        }
        bytes memory bstr = new bytes(len);
        uint256 k = len;
        while (v != 0) {
            k = k - 1;
            uint8 temp = (48 + uint8(v - v / 10 * 10));
            bytes1 b1 = bytes1(temp);
            bstr[k] = b1;
            v /= 10;
        }
        str = string(bstr);
    }
}
