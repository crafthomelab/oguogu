// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console} from "forge-std/Test.sol";
import {TestUSDT} from "src/misc/TestToken.sol";

contract TestTokenTest is Test {
    TestUSDT public testUSDT;

    function setUp() public {
        testUSDT = new TestUSDT();
    }

    function test_mint() public {
        address user = address(0x1);
        vm.prank(user);

        testUSDT.mint(user, 5e6);

        assertEq(testUSDT.balanceOf(user), 5e6);
    }
}
