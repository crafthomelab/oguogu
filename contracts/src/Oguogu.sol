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
    string private _url;

    struct UserBalance {
        uint128 reserve;
        uint128 allocatedRewards;
        uint128 accumulatedReserves;
        uint64 withdrawableUnlockTime;
    }

    mapping(address => UserBalance) private _userBalances;

    mapping(uint256 => Challenge) private _challenges;
    mapping(bytes32 => address) private _challengeHashes;

    enum ChallengeType {
        PHOTOS,
        URL
    }

    struct Challenge {
        bytes32 challengeHash; // challenge hash
        bytes32[] activityHashes; // activity hashes
        uint128 reward; // reward amount
        uint64 startDate; // challenge start date
        uint64 endDate; // challenge end date
        ChallengeType challengeType; // challenge type
        uint32 nonce; // nonce
        uint8 minimumActivityCount; // minimum activity count
        bool isClosed; // Challenge closure status
    }

    enum ChallengeStatus {
        OPEN,
        SUCCESS,
        FAILED
    }

    event DepositReward(address indexed challenger, uint128 amount);
    event WithdrawReward(address indexed challenger, uint128 amount);

    event ChallengeCreated(uint256 indexed tokenId, address indexed challenger, bytes32 challengeHash);
    event SubmitActivity(
        uint256 indexed tokenId, address indexed challenger, bytes32 challengeHash, bytes32 activityHash
    );

    event ChallengeCompleted(
        uint256 indexed tokenId, address indexed challenger, ChallengeStatus status, uint128 paymentReward
    );

    function initialize(address _rewardToken, address _operator, string memory _baseURI) public initializer {
        /**
         * @param _rewardToken The address of the reward token.
         * @param _operator The address of the challenge creator or owner, who has the authority to submit activities.
         */
        require(_rewardToken != address(0), "Invalid token address");
        require(_operator != address(0), "Invalid operator address");

        rewardToken = IERC20(_rewardToken);
        _challengeId = 1;
        _url = _baseURI;

        __Ownable_init(_operator);
        __ERC721_init("OGUOGU", "OGUOGU");
    }

    function _baseURI() internal view override returns (string memory) {
        return _url;
    }

    function depositReward(address challenger, uint128 amount) external {
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

        UserBalance storage userBalance = _userBalances[challenger];

        userBalance.reserve += amount;
        userBalance.accumulatedReserves += amount;
        if (challenger == msg.sender) {
            userBalance.withdrawableUnlockTime = uint64(block.timestamp + 28 days);
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

        UserBalance storage userBalance = _userBalances[challenger];
        uint128 amount = userBalance.reserve - userBalance.allocatedRewards;
        require(amount > 0, "Invalid amount");
        require(userBalance.withdrawableUnlockTime <= block.timestamp, "Withdrawal not yet available");

        userBalance.reserve -= amount;
        rewardToken.transfer(receiver, amount);

        emit WithdrawReward(challenger, amount);
    }

    function createChallenge(
        string memory title,
        uint128 reward,
        ChallengeType challengeType,
        bytes memory challengeSignature,
        uint64 startDate,
        uint64 endDate,
        uint32 nonce,
        uint8 minimumActivityCount
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
        require(minimumActivityCount > 0, "Invalid minimum activity count");

        bytes32 challengeHash = calculateChallengeHash(
            title, reward, challengeType, msg.sender, startDate, endDate, nonce, minimumActivityCount
        );
        require(_challengeHashes[challengeHash] == address(0), "Challenge already exists");
        require(verifySignature(owner(), challengeHash, challengeSignature), "Invalid signature");

        _challengeHashes[challengeHash] = msg.sender;

        UserBalance storage userBalance = _userBalances[msg.sender];
        userBalance.allocatedRewards += reward;
        require(userBalance.allocatedRewards <= userBalance.reserve, "Insufficient balance");

        _challenges[_challengeId] = Challenge(
            challengeHash,
            new bytes32[](0),
            reward,
            startDate,
            endDate,
            challengeType,
            nonce,
            minimumActivityCount,
            false
        );

        _safeMint(msg.sender, _challengeId);
        emit ChallengeCreated(_challengeId, msg.sender, challengeHash);
        return _challengeId++;
    }

    function submitActivity(uint256 tokenId, bytes32 activityHash, bytes memory activitySignature) external onlyOwner {
        /**
         * @notice Submits activity for a challenge.
         *
         * @dev This function can only be called by the OGUOGU contract owner.
         *      The `activitySignature` is crucial as it verifies that the activity was generated
         *      by the challenge creator, ensuring the authenticity of the submission.
         *
         * @param tokenId The ID of the challenge.
         * @param activityHash The hash of the activity.
         * @param activitySignature The signature of the activity generated by the challenge creator.
         */
        require(getChallengeStatus(tokenId) == ChallengeStatus.OPEN, "challenge is completed");
        require(verifySignature(ownerOf(tokenId), activityHash, activitySignature), "Invalid signature");

        for (uint256 i = 0; i < _challenges[tokenId].activityHashes.length; i++) {
            // duplicate activity submission check
            if (_challenges[tokenId].activityHashes[i] == activityHash) {
                revert("Activity already submitted");
            }
        }

        _challenges[tokenId].activityHashes.push(activityHash);

        emit SubmitActivity(tokenId, ownerOf(tokenId), _challenges[tokenId].challengeHash, activityHash);
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
        UserBalance storage userBalance = _userBalances[challenger];
        userBalance.allocatedRewards -= uint128(challenge.reward);

        uint128 paymentReward = 0;
        if (status == ChallengeStatus.SUCCESS) {
            paymentReward = pickPaymentReward(challenge.reward);
            rewardToken.transfer(receipent, paymentReward);

            userBalance.reserve -= uint128(paymentReward);
        } else {
            userBalance.withdrawableUnlockTime += 7 days;
        }

        emit ChallengeCompleted(tokenId, challenger, status, paymentReward);
        emit MetadataUpdate(tokenId);
    }

    function getChallengeStatus(uint256 tokenId) public view returns (ChallengeStatus) {
        Challenge memory challenge = _challenges[tokenId];

        if (challenge.activityHashes.length >= challenge.minimumActivityCount) {
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
            bytes32[] memory, // activity hashes
            uint256, // reward amount
            uint256, // challenge start date
            uint256, // challenge end date
            uint64, // minimum activity count
            bool // challenge closure status
        )
    {
        Challenge memory challenge = _challenges[tokenId];
        return (
            challenge.challengeHash,
            challenge.activityHashes,
            challenge.reward,
            challenge.startDate,
            challenge.endDate,
            challenge.minimumActivityCount,
            challenge.isClosed
        );
    }

    function verifySignature(address _signer, bytes32 hash, bytes memory signature) internal pure returns (bool) {
        bytes32 signedHash = hash.toEthSignedMessageHash();
        return signedHash.recover(signature) == _signer;
    }

    function pickPaymentReward(uint128 reward) private view returns (uint128) {
        return reward * pickRandomValue() / 100;
    }

    function pickRandomValue() private view returns (uint128) {
        /**
         * Generates a random value using blockhash and block.coinbase.
         * This is to reduce the possibility of manipulation by the operator.
         */
        return uint128(uint256(keccak256(abi.encodePacked(blockhash(block.number - 1), block.coinbase))) % 100);
    }

    function userReserves(address challenger) external view returns (uint256) {
        return _userBalances[challenger].reserve;
    }

    function userAllocatedRewards(address challenger) external view returns (uint256) {
        return _userBalances[challenger].allocatedRewards;
    }

    function withdrawableUnlockTime(address challenger) external view returns (uint256) {
        return _userBalances[challenger].withdrawableUnlockTime;
    }

    function challengeHashes(bytes32 challengeHash) external view returns (address) {
        return _challengeHashes[challengeHash];
    }

    function userAccumulatedReserves(address challenger) external view returns (uint256) {
        return _userBalances[challenger].accumulatedReserves;
    }

    function calculateChallengeHash(
        string memory title,
        uint256 reward,
        ChallengeType challengeType,
        address challenger,
        uint64 startDate,
        uint64 endDate,
        uint32 nonce,
        uint8 minimumActivityCount
    ) public pure returns (bytes32) {
        return keccak256(
            abi.encodePacked(title, reward, challengeType, challenger, startDate, endDate, nonce, minimumActivityCount)
        );
    }
}
