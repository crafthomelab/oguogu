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
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        uint256 userPrivateKey = vm.envUint("USER_PRIVATE_KEY");
        address deployer = vm.addr(deployerPrivateKey);
        address user = vm.addr(userPrivateKey);

        vm.startBroadcast(deployerPrivateKey);

        oguogu = new OGUOGU();
        testUSDT = new TestUSDT();

        testUSDT.mint(deployer, 10000e6);
        testUSDT.mint(user, 10000e6);

        bytes memory data = abi.encodeWithSignature(
            "initialize(address,address,string)",
            address(testUSDT),
            address(deployer),
            "https://assets.oguogu.me/challenges/"
        );
        ERC1967Proxy proxy = new ERC1967Proxy(address(oguogu), data);
        oguogu = OGUOGU(address(proxy));

        console.log("USDT address:", address(testUSDT));
        console.log("OGUOGU address:", address(proxy));

        vm.stopBroadcast();
    }
}
