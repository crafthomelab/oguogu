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
        bytes32 challengeHash = 0xcf164b522d38f66d2c1333e96b36828697b7a0e785de3f10adbe6060275efb5b;

        //0xd6f34075965Ae85763829850E222Fea6d70C075E;
        uint256 userPrivateKey = 0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d;
        address user = vm.addr(userPrivateKey); 

        uint256 deployerPrivateKey = 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80;
        address deployer = vm.addr(deployerPrivateKey);
        oguogu = OGUOGU(address(0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0));

        vm.startBroadcast(userPrivateKey);

        oguogu.completeChallenge(
            user, 
            1
        );
        console.logUint(uint8(oguogu.getChallengeStatus(1)));

        vm.stopBroadcast();


    }
}
