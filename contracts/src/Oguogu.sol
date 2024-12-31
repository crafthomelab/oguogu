// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/token/ERC721/ERC721Upgradeable.sol";
import "@openzeppelin/contracts/interfaces/IERC20.sol";
import "@openzeppelin/contracts/interfaces/IERC4906.sol";
import {ECDSA} from "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";
import {MessageHashUtils} from "@openzeppelin/contracts/utils/cryptography/MessageHashUtils.sol";
import {Strings} from "@openzeppelin/contracts/utils/Strings.sol";

/**
 * @title OGUOGU, 일상의 작은 도전 프로젝트
 * @author craftsangjae
 * @notice
 * 어린 시절, 우리가 숙제를 해오거나 착한 일을 할 때, 어른은 우리에게 칭찬해 줍니다.
 * 어른이 된 지금, 우리에게도 어린 시절 받았던 칭찬과 격려는 필요합니다.
 *
 * 어른은 아침에 일찍 일어났다고, 운동하러 나갔다고, 책을 읽었다고, 영어 공부했다고
 * 이런 사소한 것으로 칭찬받기는 쉽지 않습니다. 매번 해내겠다며 마음 먹지만, 우린 일상의 바쁨 때문에
 * 해내지 못할 때가 많죠.
 *
 * 하지만, 하루하루 쌓아올린 작은 성취들이 우리를 더 나은 사람으로 만들어 줘요.
 * OGUOGU는 우리를 칭찬해주며, 해내었던 작은 성취에 보상해주는 시스템입니다.
 *
 * OGUOGU는 하루하루 작은 성취들을 쌓아나갈 수 있도록, 그리고 그것을 기록할 수 있도록 장려합니다.
 */
contract OGUOGU is OwnableUpgradeable, ERC721Upgradeable, IERC4906 {
    using Strings for uint256;
    using MessageHashUtils for bytes32;
    using ECDSA for bytes32;

    IERC20 public rewardToken;

    mapping(address => uint256) public userReserves;
    mapping(address => uint256) public userAllocatedRewards;

    uint256 private _challengeId;
    mapping(uint256 => Challenge) private _challenges;

    struct Challenge {
        uint256 reward; // 리워드 금액
        bytes32 challengeHash; // 챌린지 해시값(md5 해시값)
        uint256 dueDate; // 챌린지 종료 날짜
        uint64 minimumProofCount; // 최소 증명 갯수
        address receipent; // 챌린지 성공 후, 보상 받을 주소
        bytes32[] proofHashes; // 챌린지 증명 해시값들
        bool isClosed; // 챌린지 종료 여부
    }

    enum ChallengeStatus {
        OPEN,
        SUCCESS,
        FAILED
    }

    event DepositReward(address indexed challenger, uint256 amount);
    event SubmitProof(uint256 indexed tokenId, bytes32 proofHash);
    event ChallengeCreated(uint256 indexed tokenId);
    event ChallengeCompleted(uint256 indexed tokenId, ChallengeStatus status);

    function initialize(address _rewardToken, address _operator) public initializer {
        require(_rewardToken != address(0), "Invalid token address");
        require(_operator != address(0), "Invalid operator address");

        // 보상 토큰(Tether Token)
        rewardToken = IERC20(_rewardToken);
        _challengeId = 1;

        // owner : proof submit할 수 있는 권한
        __Ownable_init(_operator);
        __ERC721_init("OGUOGU", "OGUOGU");
    }

    function _baseURI() internal pure override returns (string memory) {
        return "https://resources.oguogu.me/challenges/";
    }

    function depositReward(address challenger, uint256 amount) external {
        /**
         * 보상 토큰을 예치합니다.
         *
         * @param challenger 예치한 사용자
         * @param amount 예치한 금액
         *
         */
        require(challenger != address(0), "Invalid challenger address");
        require(amount > 0, "Invalid amount");
        require(rewardToken.transferFrom(msg.sender, address(this), amount), "Transfer failed");

        userReserves[challenger] += amount;

        emit DepositReward(challenger, amount);
    }

    function createChallenge(
        uint256 reward,
        bytes32 challengeHash,
        uint256 dueDate,
        uint64 minimumProofCount,
        address receipent
    ) external returns (uint256) {
        /**
         * 신규 챌린지를 생성합니다.
         * - 챌린지 별로 고유한 NFT를 발행합니다.
         * - 챌린지 생성자 혹은 owner만 챌린지를 생성할 수 있습니다.
         */
        require(receipent != address(0), "Invalid receipent address");
        require(reward > 0, "Invalid reward");
        require(dueDate > block.timestamp, "Invalid due date");
        require(minimumProofCount > 0, "Invalid minimum proof count");

        userAllocatedRewards[msg.sender] += reward;
        require(userAllocatedRewards[msg.sender] <= userReserves[msg.sender], "Insufficient balance");

        _challenges[_challengeId] =
            Challenge(reward, challengeHash, dueDate, minimumProofCount, receipent, new bytes32[](0), false);

        _safeMint(msg.sender, _challengeId);
        emit ChallengeCreated(_challengeId);
        return _challengeId++;
    }

    function getChallengeStatus(uint256 tokenId) public view returns (ChallengeStatus) {
        /**
         * 챌린지 상태를 조회합니다
         *
         * @param tokenId 챌린지 ID
         */
        Challenge memory challenge = _challenges[tokenId];

        if (challenge.proofHashes.length >= challenge.minimumProofCount) {
            return ChallengeStatus.SUCCESS;
        }

        if (challenge.dueDate < block.timestamp) {
            return ChallengeStatus.FAILED;
        }

        return ChallengeStatus.OPEN;
    }

    function submitProof(uint256 tokenId, bytes32 proofHash, bytes memory proofSignature) external onlyOwner {
        /**
         * 챌린지 수행에 대한 증명자료를 제출합니다.
         *
         * @param tokenId 챌린지 ID
         * @param proofHash 증명 해시값
         * @param proofSignature 증명에 대한 서명
         */
        require(_challenges[tokenId].receipent != address(0), "Invalid challenge");
        require(getChallengeStatus(tokenId) == ChallengeStatus.OPEN, "challenge is completed");
        require(verifySignature(_challenges[tokenId].receipent, proofHash, proofSignature), "Invalid signature");

        for (uint256 i = 0; i < _challenges[tokenId].proofHashes.length; i++) {
            if (_challenges[tokenId].proofHashes[i] == proofHash) {
                revert("Proof already submitted");
            }
        }

        _challenges[tokenId].proofHashes.push(proofHash);

        emit SubmitProof(tokenId, proofHash);
    }

    function completeChallenge(uint256 tokenId) external {
        /**
         * 챌린지를 종료하고, 보상을 지급합니다.
         * 실패 시, 보상은 예치 보상으로 넘어갑니다.
         *
         * @param tokenId 챌린지 ID
         */
        ChallengeStatus status = getChallengeStatus(tokenId);
        Challenge memory challenge = _challenges[tokenId];
        require(status != ChallengeStatus.OPEN, "Challenge is not closed");
        require(!challenge.isClosed, "Challenge is already closed");

        _challenges[tokenId].isClosed = true;
        userAllocatedRewards[challenge.receipent] -= challenge.reward;
        emit ChallengeCompleted(tokenId, status);
        emit MetadataUpdate(tokenId);

        if (status == ChallengeStatus.SUCCESS) {
            // 챌린지 성공 시, 보상을 지급합니다.
            rewardToken.transfer(challenge.receipent, challenge.reward);
            userReserves[challenge.receipent] -= challenge.reward;
        }
    }

    function getChallenge(uint256 tokenId)
        external
        view
        returns (uint256, bytes32, uint256, uint64, address, bytes32[] memory, bool)
    {
        Challenge memory challenge = _challenges[tokenId];
        return (
            challenge.reward,
            challenge.challengeHash,
            challenge.dueDate,
            challenge.minimumProofCount,
            challenge.receipent,
            challenge.proofHashes,
            challenge.isClosed
        );
    }

    function verifySignature(address _signer, bytes32 hash, bytes memory signature) internal pure returns (bool) {
        bytes32 signedHash = hash.toEthSignedMessageHash();
        return signedHash.recover(signature) == _signer;
    }
}
