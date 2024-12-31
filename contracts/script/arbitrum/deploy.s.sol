// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import {Script, console} from "forge-std/Script.sol";
import {OGUOGU} from "../../src/OGUOGU.sol";
import {UUPSUpgradeable} from "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import {ERC1967Proxy} from "@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol";

contract DeployScript is Script {
    OGUOGU public oguogu;

    function setUp() public {}

    function run() public {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        address deployer = vm.addr(deployerPrivateKey);
        address usdt = 0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9;

        vm.startBroadcast(deployerPrivateKey);
        oguogu = new OGUOGU();

        // 초기화 데이터 준비
        bytes memory data = abi.encodeWithSignature("initialize(address,address)", usdt, address(deployer));

        // 프록시 계약 배포
        ERC1967Proxy proxy = new ERC1967Proxy(address(oguogu), data);

        // 프록시 주소를 OGUOGU 타입으로 캐스팅
        oguogu = OGUOGU(address(proxy));

        vm.stopBroadcast();
    }
}