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
        //0xd6f34075965Ae85763829850E222Fea6d70C075E;
        // address user = 0x70997970C51812dc3A010C7d01b50e0d17dc79C8;
        address user = 0xd6f34075965Ae85763829850E222Fea6d70C075E;

        uint256 deployerPrivateKey = 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80;
        address deployer = vm.addr(deployerPrivateKey);
        oguogu = OGUOGU(address(0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0));
        testUSDT = TestUSDT(address(0x5FbDB2315678afecb367f032d93F642f64180aa3));

        vm.startBroadcast(deployerPrivateKey);

        payable(user).transfer(100e18);

        testUSDT.mint(user, 1000e6);
        // testUSDT.approve(address(oguogu), 100e6);
        // oguogu.depositReward(user, 100e6);

        vm.stopBroadcast();
    }
}
