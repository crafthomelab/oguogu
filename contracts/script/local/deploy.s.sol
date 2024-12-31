// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import {Script, console} from "forge-std/Script.sol";
import {OGUOGU} from "../../src/OGUOGU.sol";
import {UUPSUpgradeable} from "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";
import {TestUSDT} from "../../src/misc/TestToken.sol";

contract DeployScript is Script {
    OGUOGU public oguogu;
    TestUSDT public testUSDT;

    function setUp() public {}

    function run() public {
        uint256 deployerPrivateKey = 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80;
        uint256 userPrivateKey = 0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d;
        address deployer = vm.addr(deployerPrivateKey);
        address user = vm.addr(userPrivateKey);
        
        vm.startBroadcast(deployerPrivateKey);
        testUSDT = new TestUSDT();

        testUSDT.mint(deployer, 100e6);
        testUSDT.mint(user, 100e6);

        oguogu = new OGUOGU();

        bytes memory data = abi.encodeWithSignature(
            "initialize(address,address)", 
            address(testUSDT), 
            address(deployer)
        );
        ERC1967Proxy proxy = new ERC1967Proxy(address(oguogu), data);

        oguogu = OGUOGU(address(proxy));

        vm.stopBroadcast();
    }
}
