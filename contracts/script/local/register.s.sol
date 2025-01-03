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
        address user = vm.addr(userPrivateKey);
        address receipent = 0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC;

        oguogu = OGUOGU(address(0xDc64a140Aa3E981100a9becA4E685f962f0cF6C9));

        vm.startBroadcast(userPrivateKey);
        oguogu.createChallenge(
            1e6,
            0x7f52a3e131e6a2195be7e3cc2c45b2a80f7f07b05e1380425892f0db175930d8,
            hex"eca376023490e92f3754c5de4c787bc72e62a83f89f433502b936b14ae6eb84743e3ae7fbe5ebd2276384baa853a346dfaa9bc941d5bcb683a95cd31bce0629a1c",
            1736434800,
            1,
            receipent
        );

        vm.stopBroadcast();
    }
}
