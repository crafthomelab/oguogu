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
        address deployer = vm.addr(deployerPrivateKey);
        address user = vm.addr(userPrivateKey);
        oguogu = OGUOGU(address(0xDc64a140Aa3E981100a9becA4E685f962f0cF6C9));
        testUSDT = TestUSDT(address(0x5FbDB2315678afecb367f032d93F642f64180aa3));

        vm.startBroadcast(deployerPrivateKey);

        testUSDT.mint(deployer, 100e6);
        testUSDT.mint(user, 100e6);

        testUSDT.approve(address(oguogu), 100e6);
        oguogu.depositReward(user, 100e6);

        vm.stopBroadcast();
    }
}
