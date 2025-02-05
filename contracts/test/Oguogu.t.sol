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
        oguogu.initialize(address(testUSDT), operator, "");

        testUSDT.mint(user0, 10000e6);
        testUSDT.mint(operator, 100e6);

        vm.warp(1735657200); // 2025-01-01 00:00:00
    }

    function depositReward(address owner, address user, uint128 amount) public {
        vm.startPrank(owner);
        testUSDT.approve(address(oguogu), amount);
        oguogu.depositReward(address(user), amount);
        vm.stopPrank();
    }

    function test_self_depositReward() public {
        depositReward(user0, user0, 10e6);

        assertEq(oguogu.userReserves(user0), 10e6);
        assertEq(oguogu.userAllocatedRewards(user0), 0);
    }

    function test_operator_depositReward() public {
        depositReward(operator, user0, 10e6);

        assertEq(testUSDT.balanceOf(address(operator)), 90e6);
        assertEq(oguogu.userReserves(user0), 10e6);
        assertEq(oguogu.userAllocatedRewards(user0), 0);
    }

    function test_self_createChallenge() public {
        depositReward(user0, user0, 10e6);

        vm.startPrank(user0);
        bytes32 chHash = oguogu.calculateChallengeHash(
            "challenge",
            10e6,
            OGUOGU.ChallengeType.PHOTOS,
            user0,
            uint64(block.timestamp),
            uint64(block.timestamp + 1 days),
            1,
            10
        );
        bytes memory challengeSignature = generateSignature(0x1, chHash);
        uint256 challengeId = oguogu.createChallenge(
            "challenge",
            10e6,
            OGUOGU.ChallengeType.PHOTOS,
            challengeSignature,
            uint64(block.timestamp),
            uint64(block.timestamp + 1 days),
            1,
            10
        );
        vm.stopPrank();

        assertEq(oguogu.balanceOf(user0), 1);
        assertEq(oguogu.userReserves(user0), 10e6);
        assertEq(oguogu.userAllocatedRewards(user0), 10e6);

        (
            bytes32 challengeHash,
            bytes32[] memory activityHashes,
            uint256 reward,
            uint256 startDate,
            uint256 endDate,
            uint64 minimumActivityCount,
            bool isClosed
        ) = oguogu.getChallenge(challengeId);

        assertEq(reward, 10e6);
        assertEq(challengeHash, chHash);
        assertEq(startDate, block.timestamp);
        assertEq(endDate, block.timestamp + 1 days);
        assertEq(minimumActivityCount, 10);
        assertEq(activityHashes.length, 0);
        assertEq(isClosed, false);

        assertEq(challengeId, 1);
    }

    function test_block_duplicated_createChallenge() public {
        depositReward(user0, user0, 10e6);

        vm.startPrank(user0);
        bytes32 chHash = oguogu.calculateChallengeHash(
            "challenge",
            10e6,
            OGUOGU.ChallengeType.PHOTOS,
            user0,
            uint64(block.timestamp),
            uint64(block.timestamp + 1 days),
            1,
            10
        );
        bytes memory challengeSignature = generateSignature(0x1, chHash);

        oguogu.createChallenge(
            "challenge",
            10e6,
            OGUOGU.ChallengeType.PHOTOS,
            challengeSignature,
            uint64(block.timestamp),
            uint64(block.timestamp + 1 days),
            1,
            10
        );
        vm.expectRevert("Challenge already exists");
        oguogu.createChallenge(
            "challenge",
            10e6,
            OGUOGU.ChallengeType.PHOTOS,
            challengeSignature,
            uint64(block.timestamp),
            uint64(block.timestamp + 1 days),
            1,
            10
        );
    }

    function test_block_already_passed_createChallenge() public {
        depositReward(user0, user0, 10e6);

        bytes32 chHash = oguogu.calculateChallengeHash(
            "challenge",
            10e6,
            OGUOGU.ChallengeType.PHOTOS,
            user0,
            uint64(block.timestamp - 2 days),
            uint64(block.timestamp - 1 days),
            1,
            10
        );
        vm.expectRevert("Invalid end date");
        bytes memory challengeSignature = generateSignature(0x1, chHash);
        oguogu.createChallenge(
            "challenge",
            10e6,
            OGUOGU.ChallengeType.PHOTOS,
            challengeSignature,
            uint64(block.timestamp - 2 days),
            uint64(block.timestamp - 1 days),
            1,
            10
        );
    }

    function test_submitActivity() public {
        depositReward(user0, user0, 10e6);

        vm.startPrank(user0);
        bytes32 chHash = oguogu.calculateChallengeHash(
            "challenge",
            10e6,
            OGUOGU.ChallengeType.PHOTOS,
            user0,
            uint64(block.timestamp),
            uint64(block.timestamp + 1 days),
            1,
            10
        );
        bytes memory challengeSignature = generateSignature(0x1, chHash);
        oguogu.createChallenge(
            "challenge",
            10e6,
            OGUOGU.ChallengeType.PHOTOS,
            challengeSignature,
            uint64(block.timestamp),
            uint64(block.timestamp + 1 days),
            1,
            10
        );

        vm.stopPrank();

        bytes32 activityHash = bytes32(uint256(12223));
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(0x2, activityHash.toEthSignedMessageHash());
        bytes memory activitySignature = abi.encodePacked(r, s, v);

        vm.startPrank(operator);
        oguogu.submitActivity(1, activityHash, activitySignature);
        vm.stopPrank();
    }

    function test_block_double_submitActivity() public {
        depositReward(user0, user0, 10e6);

        vm.startPrank(user0);
        bytes32 chHash = oguogu.calculateChallengeHash(
            "challenge",
            10e6,
            OGUOGU.ChallengeType.PHOTOS,
            user0,
            uint64(block.timestamp),
            uint64(block.timestamp + 1 days),
            1,
            10
        );
        bytes memory challengeSignature = generateSignature(0x1, chHash);
        uint256 challengeId = oguogu.createChallenge(
            "challenge",
            10e6,
            OGUOGU.ChallengeType.PHOTOS,
            challengeSignature,
            uint64(block.timestamp),
            uint64(block.timestamp + 1 days),
            1,
            10
        );
        vm.stopPrank();

        bytes32 activityHash = bytes32(uint256(12223));
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(0x2, activityHash.toEthSignedMessageHash());
        bytes memory activitySignature = abi.encodePacked(r, s, v);

        vm.startPrank(operator);
        oguogu.submitActivity(challengeId, activityHash, activitySignature);
        vm.expectRevert("Activity already submitted");
        oguogu.submitActivity(challengeId, activityHash, activitySignature);
        vm.stopPrank();
    }

    function test_block_submitActivity_after_duedate() public {
        depositReward(user0, user0, 10e6);

        vm.startPrank(user0);
        bytes32 chHash = oguogu.calculateChallengeHash(
            "challenge",
            10e6,
            OGUOGU.ChallengeType.PHOTOS,
            user0,
            uint64(block.timestamp),
            uint64(block.timestamp + 1 days),
            1,
            10
        );
        bytes memory challengeSignature = generateSignature(0x1, chHash);
        uint256 challengeId = oguogu.createChallenge(
            "challenge",
            10e6,
            OGUOGU.ChallengeType.PHOTOS,
            challengeSignature,
            uint64(block.timestamp),
            uint64(block.timestamp + 1 days),
            1,
            10
        );

        vm.stopPrank();
        vm.warp(block.timestamp + 1 days + 1 seconds);

        bytes32 activityHash = bytes32(uint256(12223));
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(0x2, activityHash.toEthSignedMessageHash());
        bytes memory activitySignature = abi.encodePacked(r, s, v);

        vm.startPrank(operator);
        vm.expectRevert("challenge is completed");
        oguogu.submitActivity(challengeId, activityHash, activitySignature);
        vm.stopPrank();
    }

    function test_completeChallenge() public {
        depositReward(user0, user0, 10e6);

        vm.startPrank(user0);
        bytes32 chHash = oguogu.calculateChallengeHash(
            "challenge",
            10e6,
            OGUOGU.ChallengeType.PHOTOS,
            user0,
            uint64(block.timestamp),
            uint64(block.timestamp + 1 days),
            1,
            1
        );
        bytes memory challengeSignature = generateSignature(0x1, chHash);
        uint256 challengeId = oguogu.createChallenge(
            "challenge",
            10e6,
            OGUOGU.ChallengeType.PHOTOS,
            challengeSignature,
            uint64(block.timestamp),
            uint64(block.timestamp + 1 days),
            1,
            1
        );

        vm.stopPrank();

        bytes32 activityHash = bytes32(uint256(12223));
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(0x2, activityHash.toEthSignedMessageHash());
        bytes memory activitySignature = abi.encodePacked(r, s, v);

        vm.startPrank(operator);
        oguogu.submitActivity(challengeId, activityHash, activitySignature);
        vm.stopPrank();

        vm.startPrank(user0);
        oguogu.completeChallenge(user1, challengeId);
        assertLe(testUSDT.balanceOf(user1), 10e6);
        assertGt(testUSDT.balanceOf(user1), 0);
        vm.stopPrank();
    }

    function test_block_double_completeChallenge() public {
        depositReward(user0, user0, 10e6);

        vm.startPrank(user0);
        bytes32 chHash = oguogu.calculateChallengeHash(
            "challenge",
            10e6,
            OGUOGU.ChallengeType.PHOTOS,
            user0,
            uint64(block.timestamp),
            uint64(block.timestamp + 1 days),
            1,
            1
        );
        bytes memory challengeSignature = generateSignature(0x1, chHash);
        uint256 challengeId = oguogu.createChallenge(
            "challenge",
            10e6,
            OGUOGU.ChallengeType.PHOTOS,
            challengeSignature,
            uint64(block.timestamp),
            uint64(block.timestamp + 1 days),
            1,
            1
        );

        vm.stopPrank();

        bytes32 activityHash = bytes32(uint256(12223));
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(0x2, activityHash.toEthSignedMessageHash());
        bytes memory activitySignature = abi.encodePacked(r, s, v);

        vm.startPrank(operator);
        oguogu.submitActivity(challengeId, activityHash, activitySignature);
        vm.stopPrank();

        vm.startPrank(user0);
        oguogu.completeChallenge(user0, challengeId);
        vm.expectRevert("Challenge is already closed");
        oguogu.completeChallenge(user0, challengeId);
        vm.stopPrank();
    }

    function generateSignature(uint256 signer, bytes32 hash) private pure returns (bytes memory) {
        (uint8 v, bytes32 r, bytes32 s) = vm.sign(signer, hash.toEthSignedMessageHash());
        return abi.encodePacked(r, s, v);
    }
}
