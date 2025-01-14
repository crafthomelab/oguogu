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
 * @title OGUOGU, A Project for Everyday Challenges
 * @author craftsangjae
 * @notice
 * In our childhood, when we completed our homework or did good deeds, adults praised us.
 * Now, as adults, we still need the praise and encouragement we received as children.
 *
 * It's not easy for adults to receive praise for waking up early, going for a workout, reading a book, or studying English.
 * We often set our minds to accomplish these tasks, but the busyness of daily life can prevent us from achieving them.
 *
 * However, the small achievements we accumulate each day make us better individuals.
 * OGUOGU is a system that praises us and rewards our small accomplishments.
 *
 * OGUOGU encourages us to build up small achievements day by day and to record them.
 */
contract OGUOGU is OwnableUpgradeable, ERC721Upgradeable, IERC4906 {
    using Strings for uint256;
    using MessageHashUtils for bytes32;
    using ECDSA for bytes32;

    IERC20 public rewardToken;
    uint256 private _challengeId;

    mapping(address => uint256) public userReserves;
    mapping(address => uint256) public userAllocatedRewards;
    mapping(address => uint256) public withdrawableUnlockTime;

    mapping(uint256 => Challenge) private _challenges;
    mapping(bytes32 => address) public challengeHashes;

    struct Challenge {
        bytes32 challengeHash; // challenge hash
        bytes32[] proofHashes; // proof hashes
        uint256 reward; // reward amount
        uint256 startDate; // challenge start date
        uint256 endDate; // challenge end date
        uint64 minimumProofCount; // minimum proof count
        bool isClosed; // Challenge closure status
    }

    enum ChallengeStatus {
        OPEN,
        SUCCESS,
        FAILED
    }

    event DepositReward(address indexed challenger, uint256 amount);
    event WithdrawReward(address indexed challenger, uint256 amount);

    event ChallengeCreated(uint256 indexed tokenId, address indexed challenger, bytes32 challengeHash);
    event SubmitProof(uint256 indexed tokenId, address indexed challenger, bytes32 challengeHash, bytes32 proofHash);

    event ChallengeCompleted(
        uint256 indexed tokenId, address indexed challenger, ChallengeStatus status, uint256 paymentReward
    );

    function initialize(address _rewardToken, address _operator) public initializer {
        /**
         * @param _rewardToken The address of the reward token.
         * @param _operator The address of the challenge creator or owner, who has the authority to submit proofs.
         */
        require(_rewardToken != address(0), "Invalid token address");
        require(_operator != address(0), "Invalid operator address");

        rewardToken = IERC20(_rewardToken);
        _challengeId = 1;

        __Ownable_init(_operator);
        __ERC721_init("OGUOGU", "OGUOGU");
    }

    function _baseURI() internal pure override returns (string memory) {
        return "https://assets.oguogu.me/challenges/";
    }

    function depositReward(address challenger, uint256 amount) external {
        /**
         * @notice Deposits reward tokens.
         *
         * @dev The challenger must approve the contract to transfer tokens on their behalf before calling this function.
         *
         * @param challenger The address of the user making the deposit. The address must be valid and cannot be the zero address.
         *
         * @require The challenger address must be valid (not the zero address).
         * @require The amount must be greater than zero.
         * @require The challenger must have approved the contract to transfer the specified amount of tokens.
         *
         * @effects Increases the user's deposit amount and sets the withdrawal unlock time to 28 days later.
         * @emit Emits a DepositReward event to record the deposited amount.
         */
        require(challenger != address(0), "Invalid challenger address");
        require(amount > 0, "Invalid amount");
        require(rewardToken.transferFrom(msg.sender, address(this), amount), "Transfer failed");

        unchecked {
            userReserves[challenger] += amount;
            if (challenger == msg.sender) {
                withdrawableUnlockTime[challenger] = block.timestamp + 28 days;
            }
        }
        emit DepositReward(challenger, amount);
    }

    function withdrawReward(address receiver) external {
        /**
         * @notice Withdraws reward tokens.
         *
         * @dev It is important to note that the `withdrawableUnlockTime` determines when withdrawals are allowed.
         *      The `withdrawableUnlockTime` is extended each time a deposit is made or when a challenge fails.
         *      Ensure that the current time is past the `withdrawableUnlockTime` before attempting a withdrawal.
         *
         * @param receiver The address of the user receiving the withdrawal.
         */
        address challenger = msg.sender;

        require(receiver != address(0), "Invalid receiver address");
        uint256 amount = userReserves[challenger] - userAllocatedRewards[challenger];
        require(amount > 0, "Invalid amount");
        require(withdrawableUnlockTime[challenger] <= block.timestamp, "Withdrawal not yet available");

        userReserves[challenger] -= amount;
        rewardToken.transfer(receiver, amount);

        emit WithdrawReward(challenger, amount);
    }

    function createChallenge(
        uint256 reward,
        bytes32 challengeHash,
        bytes memory challengeSignature,
        uint256 startDate,
        uint256 endDate,
        uint64 minimumProofCount
    ) external returns (uint256) {
        /**
         * @notice Creates a new challenge(NFT).
         * - Issues a unique NFT for each challenge.
         * - Only the challenge creator or owner can create a challenge.
         *
         * @dev The OguOgu signature is required separately to ensure that the challenge information
         *      has been provided to the OguOgu system by the participant. This guarantees the integrity
         *      and authenticity of the challenge data before it is accepted.
         *
         * @dev The challengeHash is used as the ID of the challenge in the OguOgu system. Therefore, it must be unique.
         */
        require(reward > 0, "Invalid reward");
        require(startDate < endDate, "Invalid start date");
        require(block.timestamp < endDate, "Invalid end date");
        require(minimumProofCount > 0, "Invalid minimum proof count");
        require(challengeHashes[challengeHash] == address(0), "Challenge already exists");

        challengeHashes[challengeHash] = msg.sender;

        require(verifySignature(owner(), challengeHash, challengeSignature), "Invalid signature");

        unchecked {
            userAllocatedRewards[msg.sender] += reward;
            require(userAllocatedRewards[msg.sender] <= userReserves[msg.sender], "Insufficient balance");
        }

        _challenges[_challengeId] =
            Challenge(challengeHash, new bytes32[](0), reward, startDate, endDate, minimumProofCount, false);

        _safeMint(msg.sender, _challengeId);
        emit ChallengeCreated(_challengeId, msg.sender, challengeHash);
        return _challengeId++;
    }

    function submitProof(uint256 tokenId, bytes32 proofHash, bytes memory proofSignature) external onlyOwner {
        /**
         * @notice Submits proof for a challenge.
         *
         * @dev This function can only be called by the OGUOGU contract owner.
         *      The `proofSignature` is crucial as it verifies that the proof was generated
         *      by the challenge creator, ensuring the authenticity of the submission.
         *
         * @param tokenId The ID of the challenge.
         * @param proofHash The hash of the proof.
         * @param proofSignature The signature of the proof generated by the challenge creator.
         */
        require(getChallengeStatus(tokenId) == ChallengeStatus.OPEN, "challenge is completed");
        require(verifySignature(ownerOf(tokenId), proofHash, proofSignature), "Invalid signature");

        for (uint256 i = 0; i < _challenges[tokenId].proofHashes.length; i++) {
            // duplicate proof submission check
            if (_challenges[tokenId].proofHashes[i] == proofHash) {
                revert("Proof already submitted");
            }
        }

        _challenges[tokenId].proofHashes.push(proofHash);

        emit SubmitProof(tokenId, ownerOf(tokenId), _challenges[tokenId].challengeHash, proofHash);
        emit MetadataUpdate(tokenId);
    }

    function completeChallenge(address receipent, uint256 tokenId) external {
        /**
         * @notice Completes the challenge and distributes the reward.
         *
         * @dev If the challenge fails, the reward is remained in the challenger's reserve.
         *      The recipient is set to the challenger if the caller is not the challenger.
         *
         * @param recipient The address to receive the reward
         * @param tokenId The ID of the challenge.
         */
        address challenger = ownerOf(tokenId);
        if (msg.sender != challenger) {
            receipent = challenger;
        }

        ChallengeStatus status = getChallengeStatus(tokenId);
        Challenge memory challenge = _challenges[tokenId];
        require(status != ChallengeStatus.OPEN, "Challenge is not closed");
        require(!challenge.isClosed, "Challenge is already closed");

        _challenges[tokenId].isClosed = true;
        userAllocatedRewards[challenger] -= challenge.reward;

        uint256 paymentReward = 0;
        if (status == ChallengeStatus.SUCCESS) {
            paymentReward = pickPaymentReward(challenge.reward);
            rewardToken.transfer(receipent, paymentReward);

            userReserves[challenger] -= paymentReward;
        } else {
            withdrawableUnlockTime[challenger] += 7 days;
        }

        emit ChallengeCompleted(tokenId, challenger, status, paymentReward);
        emit MetadataUpdate(tokenId);
    }

    function getChallengeStatus(uint256 tokenId) public view returns (ChallengeStatus) {
        Challenge memory challenge = _challenges[tokenId];

        if (challenge.proofHashes.length >= challenge.minimumProofCount) {
            return ChallengeStatus.SUCCESS;
        }

        if (challenge.endDate < block.timestamp) {
            return ChallengeStatus.FAILED;
        }

        return ChallengeStatus.OPEN;
    }

    function getChallenge(uint256 tokenId)
        external
        view
        returns (
            bytes32, // challenge hash
            bytes32[] memory, // proof hashes
            uint256, // reward amount
            uint256, // challenge start date
            uint256, // challenge end date
            uint64, // minimum proof count
            bool // challenge closure status
        )
    {
        Challenge memory challenge = _challenges[tokenId];
        return (
            challenge.challengeHash,
            challenge.proofHashes,
            challenge.reward,
            challenge.startDate,
            challenge.endDate,
            challenge.minimumProofCount,
            challenge.isClosed
        );
    }

    function verifySignature(address _signer, bytes32 hash, bytes memory signature) internal pure returns (bool) {
        bytes32 signedHash = hash.toEthSignedMessageHash();
        return signedHash.recover(signature) == _signer;
    }

    function pickPaymentReward(uint256 reward) private view returns (uint256) {
        return reward * pickRandomValue() / 100;
    }

    function pickRandomValue() private view returns (uint256) {
        /**
         * Generates a random value using blockhash and block.coinbase.
         * This is to reduce the possibility of manipulation by the operator.
         */
        unchecked {
            return uint256(keccak256(abi.encodePacked(blockhash(block.number - 1), block.coinbase))) % 100;
        }
    }
}
