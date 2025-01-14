// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import {Script, console} from "forge-std/Script.sol";
import {OGUOGU} from "src/Oguogu.sol";
import {UUPSUpgradeable} from "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";
import {TestUSDT} from "src/misc/TestToken.sol";
import {Multicall3} from "src/multicall3.sol";

contract DeployScript is Script {
    OGUOGU public oguogu;
    TestUSDT public testUSDT;
    Multicall3 public multicall3;


    function setUp() public {}

    function run() public {
        uint256 deployerPrivateKey = 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80;
        address deployer = vm.addr(deployerPrivateKey);

        vm.startBroadcast(deployerPrivateKey);
        testUSDT = new TestUSDT();

        oguogu = new OGUOGU();

        bytes memory data = abi.encodeWithSignature("initialize(address,address)", address(testUSDT), address(deployer));
        ERC1967Proxy proxy = new ERC1967Proxy(address(oguogu), data);
        multicall3 = new Multicall3();

        oguogu = OGUOGU(address(proxy));

        console.log("USDT address:", address(testUSDT));
        console.log("OGUOGU address:", address(proxy));
        console.log("Multicall3 address:", address(multicall3));
        
        vm.stopBroadcast();
    }
}
