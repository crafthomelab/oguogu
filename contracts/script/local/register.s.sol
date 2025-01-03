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
        testUSDT = TestUSDT(address(0x5FbDB2315678afecb367f032d93F642f64180aa3));
        
        vm.startBroadcast(userPrivateKey);

        testUSDT.approve(address(oguogu), 1e6);
        oguogu.depositReward(user, 1e6);
        
        oguogu.createChallenge(
            1e6,
            0x97a13132222bfbf62837aae6d3aca0d927c1e4535fbeb4935f15cbdabb376238,
            hex"19ee2a9db40504b6ba6a5175809d4e9e8e62a8d3336fb80321b58eb91210050330e46dd29dae9d5e7482526be1c4bd15cf5e9bb1c37ec5cdf8bd1be55399c1671c",
            1736434800,
            3,
            receipent
        );

        vm.stopBroadcast();
    }
}
