// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import {Test, console} from "forge-std/Test.sol";
import {TestUSDT} from "src/misc/TestToken.sol";
import {OGUOGU} from "src/Oguogu.sol";
import {MessageHashUtils} from "@openzeppelin/contracts/utils/cryptography/MessageHashUtils.sol";

contract OGUOGUTest is Test {
    using MessageHashUtils for bytes32;

    TestUSDT public testUSDT;
    OGUOGU public oguogu;

    address public operator = vm.addr(0x1);
    address public user0 = vm.addr(0x2);
    address public user1 = vm.addr(0x3);

    function setUp() public {
        testUSDT = new TestUSDT();
        oguogu = new OGUOGU();
        oguogu.initialize(address(testUSDT), operator);

        testUSDT.mint(user0, 100e6);
        testUSDT.mint(operator, 100e6);

        vm.warp(1735657200); // 2025-01-01 00:00:00
    }

    function test_self_depositReward() public {
        vm.startPrank(user0);
        testUSDT.approve(address(oguogu), 10e6);
        oguogu.depositReward(address(user0), 10e6);
        vm.stopPrank();

        assertEq(oguogu.userReserves(user0), 10e6);
        assertEq(oguogu.userAllocatedRewards(user0), 0);
    }

    function test_operator_depositReward() public {
        vm.stopPrank();

        vm.startPrank(operator);
        testUSDT.approve(address(oguogu), 10e6);
        oguogu.depositReward(address(user0), 10e6);
        vm.stopPrank();

        assertEq(testUSDT.balanceOf(address(operator)), 90e6);
        assertEq(oguogu.userReserves(user0), 10e6);
        assertEq(oguogu.userAllocatedRewards(user0), 0);
    }

    function test_self_createChallenge() public {
        vm.startPrank(user0);
        testUSDT.approve(address(oguogu), 10e6);
        oguogu.depositReward(address(user0), 10e6);

        bytes32 chHash = bytes32(uint256(123));
        bytes memory challengeSignature = generateSignature(0x1, chHash);
        uint256 challengeId =
            oguogu.createChallenge(10e6, chHash, challengeSignature, block.timestamp + 1 days, 10, user0);

        vm.stopPrank();

        assertEq(oguogu.balanceOf(user0), 1);
        assertEq(oguogu.userReserves(user0), 10e6);
        assertEq(oguogu.userAllocatedRewards(user0), 10e6);

        (
            uint256 reward,
            bytes32 challengeHash,
            uint256 dueDate,
            uint64 minimumProofCount,
            address receipent,
            bytes32[] memory proofHashes,
            bool isClosed
        ) = oguogu.getChallenge(challengeId);

        assertEq(reward, 10e6);
        assertEq(challengeHash, bytes32(uint256(123)));
        assertEq(dueDate, block.timestamp + 1 days);
        assertEq(minimumProofCount, 10);
        assertEq(receipent, user0);
        assertEq(proofHashes.length, 0);
        assertEq(isClosed, false);

        assertEq(challengeId, 1);
    }

    function test_block_duplicated_createChallenge() public {
        vm.startPrank(user0);
        testUSDT.approve(address(oguogu), 10e6);
        oguogu.depositReward(address(user0), 10e6);

        bytes32 chHash = bytes32(uint256(123));
        bytes memory challengeSignature = generateSignature(0x1, chHash);

        oguogu.createChallenge(10e6, chHash, challengeSignature, block.timestamp + 1 days, 10, user0);
        vm.expectRevert("Challenge already exists");
        oguogu.createChallenge(10e6, chHash, challengeSignature, block.timestamp + 1 days, 10, user0);
    }

    function test_block_already_passed_createChallenge() public {
        vm.startPrank(user0);
        testUSDT.approve(address(oguogu), 10e6);
        oguogu.depositReward(address(user0), 10e6);

        vm.expectRevert("Invalid due date");
        bytes32 chHash = bytes32(uint256(123));
        bytes memory challengeSignature = generateSignature(0x1, chHash);
        oguogu.createChallenge(10e6, chHash, challengeSignature, block.timestamp - 1 days, 10, user0);
    }

    function test_submitProof() public {
        vm.startPrank(user0);
        testUSDT.approve(address(oguogu), 10e6);
        oguogu.depositReward(address(user0), 10e6);

        bytes32 chHash = bytes32(uint256(123));
        bytes memory challengeSignature = generateSignature(0x1, chHash);
        oguogu.createChallenge(10e6, chHash, challengeSignature, block.timestamp + 1 days, 10, user0);

        vm.stopPrank();

        bytes32 proofHash = bytes32(uint256(12223));
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(0x2, proofHash.toEthSignedMessageHash());
        bytes memory proofSignature = abi.encodePacked(r, s, v);

        vm.startPrank(operator);
        oguogu.submitProof(1, proofHash, proofSignature);
        vm.stopPrank();
    }

    function test_block_double_submitProof() public {
        vm.startPrank(user0);
        testUSDT.approve(address(oguogu), 10e6);
        oguogu.depositReward(address(user0), 10e6);

        bytes32 chHash = bytes32(uint256(123));
        bytes memory challengeSignature = generateSignature(0x1, chHash);
        uint256 challengeId =
            oguogu.createChallenge(10e6, chHash, challengeSignature, block.timestamp + 1 days, 10, user0);

        vm.stopPrank();

        bytes32 proofHash = bytes32(uint256(12223));
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(0x2, proofHash.toEthSignedMessageHash());
        bytes memory proofSignature = abi.encodePacked(r, s, v);

        vm.startPrank(operator);
        oguogu.submitProof(challengeId, proofHash, proofSignature);
        vm.expectRevert("Proof already submitted");
        oguogu.submitProof(challengeId, proofHash, proofSignature);
        vm.stopPrank();
    }

    function test_block_submitProof_after_duedate() public {
        vm.startPrank(user0);
        testUSDT.approve(address(oguogu), 10e6);
        oguogu.depositReward(address(user0), 10e6);

        bytes32 chHash = bytes32(uint256(123));
        bytes memory challengeSignature = generateSignature(0x1, chHash);
        uint256 challengeId =
            oguogu.createChallenge(10e6, chHash, challengeSignature, block.timestamp + 1 days, 10, user0);

        vm.stopPrank();
        vm.warp(block.timestamp + 1 days + 1 seconds);

        bytes32 proofHash = bytes32(uint256(12223));
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(0x2, proofHash.toEthSignedMessageHash());
        bytes memory proofSignature = abi.encodePacked(r, s, v);

        vm.startPrank(operator);
        vm.expectRevert("challenge is completed");
        oguogu.submitProof(challengeId, proofHash, proofSignature);
        vm.stopPrank();
    }

    function test_completeChallenge() public {
        vm.startPrank(user0);
        testUSDT.approve(address(oguogu), 10e6);
        oguogu.depositReward(address(user0), 10e6);

        bytes32 chHash = bytes32(uint256(123));
        bytes memory challengeSignature = generateSignature(0x1, chHash);
        uint256 challengeId =
            oguogu.createChallenge(10e6, chHash, challengeSignature, block.timestamp + 1 days, 1, user1);

        vm.stopPrank();

        bytes32 proofHash = bytes32(uint256(12223));
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(0x2, proofHash.toEthSignedMessageHash());
        bytes memory proofSignature = abi.encodePacked(r, s, v);

        vm.startPrank(operator);
        oguogu.submitProof(challengeId, proofHash, proofSignature);
        vm.stopPrank();

        oguogu.completeChallenge(challengeId);
        assertLe(testUSDT.balanceOf(user1), 10e6);
        assertGt(testUSDT.balanceOf(user1), 0);
    }

    function test_block_double_completeChallenge() public {
        vm.startPrank(user0);
        testUSDT.approve(address(oguogu), 10e6);
        oguogu.depositReward(address(user0), 10e6);

        bytes32 chHash = bytes32(uint256(123));
        bytes memory challengeSignature = generateSignature(0x1, chHash);
        uint256 challengeId =
            oguogu.createChallenge(10e6, chHash, challengeSignature, block.timestamp + 1 days, 1, user1);

        vm.stopPrank();

        bytes32 proofHash = bytes32(uint256(12223));
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(0x2, proofHash.toEthSignedMessageHash());
        bytes memory proofSignature = abi.encodePacked(r, s, v);

        vm.startPrank(operator);
        oguogu.submitProof(challengeId, proofHash, proofSignature);
        vm.stopPrank();

        oguogu.completeChallenge(challengeId);
        vm.expectRevert("Challenge is already closed");
        oguogu.completeChallenge(challengeId);
    }

    function generateSignature(uint256 signer, bytes32 hash) private pure returns (bytes memory) {
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(signer, hash.toEthSignedMessageHash());
        return abi.encodePacked(r, s, v);
    }
}
