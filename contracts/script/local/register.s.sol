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

        oguogu = OGUOGU(address(0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0));

        vm.startBroadcast(userPrivateKey);
        // console.logBytes32(
        //     oguogu.calculateChallengeHash(
        //         unicode"영어공부 앱으로 영어하기",
        //         1e6,
        //         OGUOGU.ChallengeType.PHOTOS,
        //         user,
        //         // hex"bc96086da68e417a70074d9a481bd2a838241f17e5b0243e61fee003a9ac9a3802e7b6ed47aee292ef7d770b33f51ff89f4f2793786a28c492173b541deb7ecf1b",
        //         1736926631,
        //         1737358631,
        //         10,
        //         1
        // ));


        oguogu.createChallenge(
            unicode"영어공부 앱으로 영어하기",
            1e6,
            OGUOGU.ChallengeType.PHOTOS,
            hex"bc96086da68e417a70074d9a481bd2a838241f17e5b0243e61fee003a9ac9a3802e7b6ed47aee292ef7d770b33f51ff89f4f2793786a28c492173b541deb7ecf1b",
            1736926631,
            1737358631,
            10,
            1
        );

        vm.stopBroadcast();
    }
}
