/* Autogenerated file. Do not edit manually. */
/* tslint:disable */
/* eslint-disable */
import {
  Contract,
  ContractFactory,
  ContractTransactionResponse,
  Interface,
} from "ethers";
import type { Signer, ContractDeployTransaction, ContractRunner } from "ethers";
import type { NonPayableOverrides } from "../common";
import type { OGUOGU, OGUOGUInterface } from "../OGUOGU";

const _abi = [
  {
    type: "function",
    name: "approve",
    inputs: [
      {
        name: "to",
        type: "address",
        internalType: "address",
      },
      {
        name: "tokenId",
        type: "uint256",
        internalType: "uint256",
      },
    ],
    outputs: [],
    stateMutability: "nonpayable",
  },
  {
    type: "function",
    name: "balanceOf",
    inputs: [
      {
        name: "owner",
        type: "address",
        internalType: "address",
      },
    ],
    outputs: [
      {
        name: "",
        type: "uint256",
        internalType: "uint256",
      },
    ],
    stateMutability: "view",
  },
  {
    type: "function",
    name: "completeChallenge",
    inputs: [
      {
        name: "tokenId",
        type: "uint256",
        internalType: "uint256",
      },
    ],
    outputs: [],
    stateMutability: "nonpayable",
  },
  {
    type: "function",
    name: "createChallenge",
    inputs: [
      {
        name: "reward",
        type: "uint256",
        internalType: "uint256",
      },
      {
        name: "challengeHash",
        type: "bytes32",
        internalType: "bytes32",
      },
      {
        name: "dueDate",
        type: "uint256",
        internalType: "uint256",
      },
      {
        name: "minimumProofCount",
        type: "uint64",
        internalType: "uint64",
      },
      {
        name: "receipent",
        type: "address",
        internalType: "address",
      },
    ],
    outputs: [
      {
        name: "",
        type: "uint256",
        internalType: "uint256",
      },
    ],
    stateMutability: "nonpayable",
  },
  {
    type: "function",
    name: "depositReward",
    inputs: [
      {
        name: "challenger",
        type: "address",
        internalType: "address",
      },
      {
        name: "amount",
        type: "uint256",
        internalType: "uint256",
      },
    ],
    outputs: [],
    stateMutability: "nonpayable",
  },
  {
    type: "function",
    name: "getApproved",
    inputs: [
      {
        name: "tokenId",
        type: "uint256",
        internalType: "uint256",
      },
    ],
    outputs: [
      {
        name: "",
        type: "address",
        internalType: "address",
      },
    ],
    stateMutability: "view",
  },
  {
    type: "function",
    name: "getChallenge",
    inputs: [
      {
        name: "tokenId",
        type: "uint256",
        internalType: "uint256",
      },
    ],
    outputs: [
      {
        name: "",
        type: "uint256",
        internalType: "uint256",
      },
      {
        name: "",
        type: "bytes32",
        internalType: "bytes32",
      },
      {
        name: "",
        type: "uint256",
        internalType: "uint256",
      },
      {
        name: "",
        type: "uint64",
        internalType: "uint64",
      },
      {
        name: "",
        type: "address",
        internalType: "address",
      },
      {
        name: "",
        type: "bytes32[]",
        internalType: "bytes32[]",
      },
      {
        name: "",
        type: "bool",
        internalType: "bool",
      },
    ],
    stateMutability: "view",
  },
  {
    type: "function",
    name: "getChallengeStatus",
    inputs: [
      {
        name: "tokenId",
        type: "uint256",
        internalType: "uint256",
      },
    ],
    outputs: [
      {
        name: "",
        type: "uint8",
        internalType: "enum OGUOGU.ChallengeStatus",
      },
    ],
    stateMutability: "view",
  },
  {
    type: "function",
    name: "initialize",
    inputs: [
      {
        name: "_rewardToken",
        type: "address",
        internalType: "address",
      },
      {
        name: "_operator",
        type: "address",
        internalType: "address",
      },
    ],
    outputs: [],
    stateMutability: "nonpayable",
  },
  {
    type: "function",
    name: "isApprovedForAll",
    inputs: [
      {
        name: "owner",
        type: "address",
        internalType: "address",
      },
      {
        name: "operator",
        type: "address",
        internalType: "address",
      },
    ],
    outputs: [
      {
        name: "",
        type: "bool",
        internalType: "bool",
      },
    ],
    stateMutability: "view",
  },
  {
    type: "function",
    name: "name",
    inputs: [],
    outputs: [
      {
        name: "",
        type: "string",
        internalType: "string",
      },
    ],
    stateMutability: "view",
  },
  {
    type: "function",
    name: "owner",
    inputs: [],
    outputs: [
      {
        name: "",
        type: "address",
        internalType: "address",
      },
    ],
    stateMutability: "view",
  },
  {
    type: "function",
    name: "ownerOf",
    inputs: [
      {
        name: "tokenId",
        type: "uint256",
        internalType: "uint256",
      },
    ],
    outputs: [
      {
        name: "",
        type: "address",
        internalType: "address",
      },
    ],
    stateMutability: "view",
  },
  {
    type: "function",
    name: "renounceOwnership",
    inputs: [],
    outputs: [],
    stateMutability: "nonpayable",
  },
  {
    type: "function",
    name: "rewardToken",
    inputs: [],
    outputs: [
      {
        name: "",
        type: "address",
        internalType: "contract IERC20",
      },
    ],
    stateMutability: "view",
  },
  {
    type: "function",
    name: "safeTransferFrom",
    inputs: [
      {
        name: "from",
        type: "address",
        internalType: "address",
      },
      {
        name: "to",
        type: "address",
        internalType: "address",
      },
      {
        name: "tokenId",
        type: "uint256",
        internalType: "uint256",
      },
    ],
    outputs: [],
    stateMutability: "nonpayable",
  },
  {
    type: "function",
    name: "safeTransferFrom",
    inputs: [
      {
        name: "from",
        type: "address",
        internalType: "address",
      },
      {
        name: "to",
        type: "address",
        internalType: "address",
      },
      {
        name: "tokenId",
        type: "uint256",
        internalType: "uint256",
      },
      {
        name: "data",
        type: "bytes",
        internalType: "bytes",
      },
    ],
    outputs: [],
    stateMutability: "nonpayable",
  },
  {
    type: "function",
    name: "setApprovalForAll",
    inputs: [
      {
        name: "operator",
        type: "address",
        internalType: "address",
      },
      {
        name: "approved",
        type: "bool",
        internalType: "bool",
      },
    ],
    outputs: [],
    stateMutability: "nonpayable",
  },
  {
    type: "function",
    name: "submitProof",
    inputs: [
      {
        name: "tokenId",
        type: "uint256",
        internalType: "uint256",
      },
      {
        name: "proofHash",
        type: "bytes32",
        internalType: "bytes32",
      },
      {
        name: "proofSignature",
        type: "bytes",
        internalType: "bytes",
      },
    ],
    outputs: [],
    stateMutability: "nonpayable",
  },
  {
    type: "function",
    name: "supportsInterface",
    inputs: [
      {
        name: "interfaceId",
        type: "bytes4",
        internalType: "bytes4",
      },
    ],
    outputs: [
      {
        name: "",
        type: "bool",
        internalType: "bool",
      },
    ],
    stateMutability: "view",
  },
  {
    type: "function",
    name: "symbol",
    inputs: [],
    outputs: [
      {
        name: "",
        type: "string",
        internalType: "string",
      },
    ],
    stateMutability: "view",
  },
  {
    type: "function",
    name: "tokenURI",
    inputs: [
      {
        name: "tokenId",
        type: "uint256",
        internalType: "uint256",
      },
    ],
    outputs: [
      {
        name: "",
        type: "string",
        internalType: "string",
      },
    ],
    stateMutability: "view",
  },
  {
    type: "function",
    name: "transferFrom",
    inputs: [
      {
        name: "from",
        type: "address",
        internalType: "address",
      },
      {
        name: "to",
        type: "address",
        internalType: "address",
      },
      {
        name: "tokenId",
        type: "uint256",
        internalType: "uint256",
      },
    ],
    outputs: [],
    stateMutability: "nonpayable",
  },
  {
    type: "function",
    name: "transferOwnership",
    inputs: [
      {
        name: "newOwner",
        type: "address",
        internalType: "address",
      },
    ],
    outputs: [],
    stateMutability: "nonpayable",
  },
  {
    type: "function",
    name: "userAllocatedRewards",
    inputs: [
      {
        name: "",
        type: "address",
        internalType: "address",
      },
    ],
    outputs: [
      {
        name: "",
        type: "uint256",
        internalType: "uint256",
      },
    ],
    stateMutability: "view",
  },
  {
    type: "function",
    name: "userReserves",
    inputs: [
      {
        name: "",
        type: "address",
        internalType: "address",
      },
    ],
    outputs: [
      {
        name: "",
        type: "uint256",
        internalType: "uint256",
      },
    ],
    stateMutability: "view",
  },
  {
    type: "event",
    name: "Approval",
    inputs: [
      {
        name: "owner",
        type: "address",
        indexed: true,
        internalType: "address",
      },
      {
        name: "approved",
        type: "address",
        indexed: true,
        internalType: "address",
      },
      {
        name: "tokenId",
        type: "uint256",
        indexed: true,
        internalType: "uint256",
      },
    ],
    anonymous: false,
  },
  {
    type: "event",
    name: "ApprovalForAll",
    inputs: [
      {
        name: "owner",
        type: "address",
        indexed: true,
        internalType: "address",
      },
      {
        name: "operator",
        type: "address",
        indexed: true,
        internalType: "address",
      },
      {
        name: "approved",
        type: "bool",
        indexed: false,
        internalType: "bool",
      },
    ],
    anonymous: false,
  },
  {
    type: "event",
    name: "BatchMetadataUpdate",
    inputs: [
      {
        name: "_fromTokenId",
        type: "uint256",
        indexed: false,
        internalType: "uint256",
      },
      {
        name: "_toTokenId",
        type: "uint256",
        indexed: false,
        internalType: "uint256",
      },
    ],
    anonymous: false,
  },
  {
    type: "event",
    name: "ChallengeCompleted",
    inputs: [
      {
        name: "tokenId",
        type: "uint256",
        indexed: true,
        internalType: "uint256",
      },
      {
        name: "status",
        type: "uint8",
        indexed: false,
        internalType: "enum OGUOGU.ChallengeStatus",
      },
    ],
    anonymous: false,
  },
  {
    type: "event",
    name: "ChallengeCreated",
    inputs: [
      {
        name: "tokenId",
        type: "uint256",
        indexed: true,
        internalType: "uint256",
      },
    ],
    anonymous: false,
  },
  {
    type: "event",
    name: "DepositReward",
    inputs: [
      {
        name: "challenger",
        type: "address",
        indexed: true,
        internalType: "address",
      },
      {
        name: "amount",
        type: "uint256",
        indexed: false,
        internalType: "uint256",
      },
    ],
    anonymous: false,
  },
  {
    type: "event",
    name: "Initialized",
    inputs: [
      {
        name: "version",
        type: "uint64",
        indexed: false,
        internalType: "uint64",
      },
    ],
    anonymous: false,
  },
  {
    type: "event",
    name: "MetadataUpdate",
    inputs: [
      {
        name: "_tokenId",
        type: "uint256",
        indexed: false,
        internalType: "uint256",
      },
    ],
    anonymous: false,
  },
  {
    type: "event",
    name: "OwnershipTransferred",
    inputs: [
      {
        name: "previousOwner",
        type: "address",
        indexed: true,
        internalType: "address",
      },
      {
        name: "newOwner",
        type: "address",
        indexed: true,
        internalType: "address",
      },
    ],
    anonymous: false,
  },
  {
    type: "event",
    name: "SubmitProof",
    inputs: [
      {
        name: "tokenId",
        type: "uint256",
        indexed: true,
        internalType: "uint256",
      },
      {
        name: "proofHash",
        type: "bytes32",
        indexed: false,
        internalType: "bytes32",
      },
    ],
    anonymous: false,
  },
  {
    type: "event",
    name: "Transfer",
    inputs: [
      {
        name: "from",
        type: "address",
        indexed: true,
        internalType: "address",
      },
      {
        name: "to",
        type: "address",
        indexed: true,
        internalType: "address",
      },
      {
        name: "tokenId",
        type: "uint256",
        indexed: true,
        internalType: "uint256",
      },
    ],
    anonymous: false,
  },
  {
    type: "error",
    name: "ECDSAInvalidSignature",
    inputs: [],
  },
  {
    type: "error",
    name: "ECDSAInvalidSignatureLength",
    inputs: [
      {
        name: "length",
        type: "uint256",
        internalType: "uint256",
      },
    ],
  },
  {
    type: "error",
    name: "ECDSAInvalidSignatureS",
    inputs: [
      {
        name: "s",
        type: "bytes32",
        internalType: "bytes32",
      },
    ],
  },
  {
    type: "error",
    name: "ERC721IncorrectOwner",
    inputs: [
      {
        name: "sender",
        type: "address",
        internalType: "address",
      },
      {
        name: "tokenId",
        type: "uint256",
        internalType: "uint256",
      },
      {
        name: "owner",
        type: "address",
        internalType: "address",
      },
    ],
  },
  {
    type: "error",
    name: "ERC721InsufficientApproval",
    inputs: [
      {
        name: "operator",
        type: "address",
        internalType: "address",
      },
      {
        name: "tokenId",
        type: "uint256",
        internalType: "uint256",
      },
    ],
  },
  {
    type: "error",
    name: "ERC721InvalidApprover",
    inputs: [
      {
        name: "approver",
        type: "address",
        internalType: "address",
      },
    ],
  },
  {
    type: "error",
    name: "ERC721InvalidOperator",
    inputs: [
      {
        name: "operator",
        type: "address",
        internalType: "address",
      },
    ],
  },
  {
    type: "error",
    name: "ERC721InvalidOwner",
    inputs: [
      {
        name: "owner",
        type: "address",
        internalType: "address",
      },
    ],
  },
  {
    type: "error",
    name: "ERC721InvalidReceiver",
    inputs: [
      {
        name: "receiver",
        type: "address",
        internalType: "address",
      },
    ],
  },
  {
    type: "error",
    name: "ERC721InvalidSender",
    inputs: [
      {
        name: "sender",
        type: "address",
        internalType: "address",
      },
    ],
  },
  {
    type: "error",
    name: "ERC721NonexistentToken",
    inputs: [
      {
        name: "tokenId",
        type: "uint256",
        internalType: "uint256",
      },
    ],
  },
  {
    type: "error",
    name: "InvalidInitialization",
    inputs: [],
  },
  {
    type: "error",
    name: "NotInitializing",
    inputs: [],
  },
  {
    type: "error",
    name: "OwnableInvalidOwner",
    inputs: [
      {
        name: "owner",
        type: "address",
        internalType: "address",
      },
    ],
  },
  {
    type: "error",
    name: "OwnableUnauthorizedAccount",
    inputs: [
      {
        name: "account",
        type: "address",
        internalType: "address",
      },
    ],
  },
] as const;

const _bytecode =
  "0x6080604052348015600e575f5ffd5b506127d38061001c5f395ff3fe608060405234801561000f575f5ffd5b5060043610610187575f3560e01c8063715018a6116100d9578063a22cb46511610093578063c87b56dd1161006e578063c87b56dd146103ab578063e985e9c5146103be578063f2fde38b146103d1578063f7c618c1146103e4575f5ffd5b8063a22cb46514610372578063a7817bbc14610385578063b88d4fde14610398575f5ffd5b8063715018a6146102e05780637db4e28f146102e8578063832c8bc6146102fb5780638da5cb5b1461031b57806391469fbe1461034b57806395d89b411461036a575f5ffd5b806323b872dd1161014457806342842e0e1161011f57806342842e0e14610294578063485cc955146102a75780636352211e146102ba57806370a08231146102cd575f5ffd5b806323b872dd1461025b57806338a511861461026e5780633dd68feb14610281575f5ffd5b806301ffc9a71461018b57806306fdde03146101b3578063081812fc146101c8578063095ea7b3146101f35780630d08e181146102085780631bdd4b7414610235575b5f5ffd5b61019e610199366004612139565b6103f6565b60405190151581526020015b60405180910390f35b6101bb610447565b6040516101aa9190612182565b6101db6101d6366004612194565b6104e8565b6040516001600160a01b0390911681526020016101aa565b6102066102013660046121c6565b6104fc565b005b6102276102163660046121ee565b60016020525f908152604090205481565b6040519081526020016101aa565b610248610243366004612194565b61050b565b6040516101aa9796959493929190612207565b610206610269366004612292565b610611565b61022761027c3660046122cc565b61069f565b61020661028f3660046123c2565b610984565b6102066102a2366004612292565b610bd2565b6102066102b536600461240d565b610bf1565b6101db6102c8366004612194565b610e07565b6102276102db3660046121ee565b610e11565b610206610e69565b6102066102f63660046121c6565b610e7c565b61030e610309366004612194565b611035565b6040516101aa9190612452565b7f9016d09d72d40fdae2fd8ceac6b6234c7706214fd39c1cd1e609a0528c199300546001600160a01b03166101db565b6102276103593660046121ee565b60026020525f908152604090205481565b6101bb611137565b610206610380366004612485565b611175565b610206610393366004612194565b611180565b6102066103a63660046124ba565b61148a565b6101bb6103b9366004612194565b6114a2565b61019e6103cc36600461240d565b611507565b6102066103df3660046121ee565b611553565b5f546101db906001600160a01b031681565b5f6001600160e01b031982166380ac58cd60e01b148061042657506001600160e01b03198216635b5e139f60e01b145b8061044157506301ffc9a760e01b6001600160e01b03198316145b92915050565b5f5160206127575f395f51905f5280546060919081906104669061251d565b80601f01602080910402602001604051908101604052809291908181526020018280546104929061251d565b80156104dd5780601f106104b4576101008083540402835291602001916104dd565b820191905f5260205f20905b8154815290600101906020018083116104c057829003601f168201915b505050505091505090565b5f6104f282611590565b50610441826115c7565b610507828233611600565b5050565b5f818152600460208181526040808420815160e0810183528154815260018201548185015260028201548184015260038201546001600160401b038116606080840191909152600160401b9091046001600160a01b031660808301529482018054845181870281018701909552808552879687968796879692958795869591949360a086019392908301828280156105c057602002820191905f5260205f20905b8154815260200190600101908083116105ac575b50505091835250506005919091015460ff16151560209182015281519082015160408301516060840151608085015160a086015160c090960151949f939e50919c509a509850919650945092505050565b6001600160a01b03821661063f57604051633250574960e11b81525f60048201526024015b60405180910390fd5b5f61064b83833361160d565b9050836001600160a01b0316816001600160a01b031614610699576040516364283d7b60e01b81526001600160a01b0380861660048301526024820184905282166044820152606401610636565b50505050565b5f6001600160a01b0382166106f65760405162461bcd60e51b815260206004820152601960248201527f496e76616c696420726563656970656e742061646472657373000000000000006044820152606401610636565b5f86116107365760405162461bcd60e51b815260206004820152600e60248201526d125b9d985b1a59081c995dd85c9960921b6044820152606401610636565b4284116107785760405162461bcd60e51b815260206004820152601060248201526f496e76616c696420647565206461746560801b6044820152606401610636565b5f836001600160401b0316116107d05760405162461bcd60e51b815260206004820152601b60248201527f496e76616c6964206d696e696d756d2070726f6f6620636f756e7400000000006044820152606401610636565b335f90815260026020526040812080548892906107ee908490612569565b9091555050335f9081526001602090815260408083205460029092529091205411156108535760405162461bcd60e51b8152602060048201526014602482015273496e73756666696369656e742062616c616e636560601b6044820152606401610636565b6040805160e08101825287815260208082018881528284018881526001600160401b03888116606086019081526001600160a01b038981166080880190815288515f8082528189018b5260a08a0191825260c08a018190526003805482526004808b529b9091208a5181559751600189015595516002880155925194860180549151959094166001600160e01b031990911617600160401b949091169390930292909217905551805193949193610912939285019291909101906120c7565b5060c091909101516005909101805460ff191691151591909117905560035461093c90339061170f565b6003546040517ffe366ed42e96da2650dfa7208b48ca7c04cf8da8d873216fca4d90f487784e40905f90a260038054905f6109768361257c565b909155509695505050505050565b61098c611728565b5f83815260046020526040902060030154600160401b90046001600160a01b03166109ed5760405162461bcd60e51b8152602060048201526011602482015270496e76616c6964206368616c6c656e676560781b6044820152606401610636565b5f6109f784611035565b6002811115610a0857610a0861243e565b14610a4e5760405162461bcd60e51b815260206004820152601660248201527518da185b1b195b99d9481a5cc818dbdb5c1b195d195960521b6044820152606401610636565b610a61610a5a84610e07565b8383611783565b610aa15760405162461bcd60e51b8152602060048201526011602482015270496e76616c6964207369676e617475726560781b6044820152606401610636565b5f5b5f8481526004602081905260409091200154811015610b40578260045f8681526020019081526020015f206004018281548110610ae257610ae2612594565b905f5260205f20015403610b385760405162461bcd60e51b815260206004820152601760248201527f50726f6f6620616c7265616479207375626d69747465640000000000000000006044820152606401610636565b600101610aa3565b505f8381526004602081815260408084209092018054600181018255908452928190209092018490555183815284917f0680b9fc3b5ee96077ab1587e03ade3667c7bd59d137f843a0723b76fd5e4fcf910160405180910390a26040518381527ff8e1a15aba9398e019f0b49df1a4fde98ee17ae345cb5f6b5e2c27f5033e8ce79060200160405180910390a1505050565b610bec83838360405180602001604052805f81525061148a565b505050565b7ff0c57e16840df040f15088dc2f81fe391c3923bec73e23a9662efc9c229c6a008054600160401b810460ff1615906001600160401b03165f81158015610c355750825b90505f826001600160401b03166001148015610c505750303b155b905081158015610c5e575080155b15610c7c5760405163f92ee8a960e01b815260040160405180910390fd5b845467ffffffffffffffff191660011785558315610ca657845460ff60401b1916600160401b1785555b6001600160a01b038716610cf45760405162461bcd60e51b8152602060048201526015602482015274496e76616c696420746f6b656e206164647265737360581b6044820152606401610636565b6001600160a01b038616610d4a5760405162461bcd60e51b815260206004820152601860248201527f496e76616c6964206f70657261746f72206164647265737300000000000000006044820152606401610636565b5f80546001600160a01b0319166001600160a01b0389161790556001600355610d72866117d8565b610db8604051806040016040528060068152602001654f47554f475560d01b815250604051806040016040528060068152602001654f47554f475560d01b8152506117e9565b8315610dfe57845460ff60401b19168555604051600181527fc7f505b2f371ae2175ee4913f4499e1f2633a7b5936321eed1cdaeb6115181d29060200160405180910390a15b50505050505050565b5f61044182611590565b5f5f5160206127575f395f51905f526001600160a01b038316610e49576040516322718ad960e21b81525f6004820152602401610636565b6001600160a01b039092165f908152600390920160205250604090205490565b610e71611728565b610e7a5f6117fb565b565b6001600160a01b038216610ed25760405162461bcd60e51b815260206004820152601a60248201527f496e76616c6964206368616c6c656e67657220616464726573730000000000006044820152606401610636565b5f8111610f125760405162461bcd60e51b815260206004820152600e60248201526d125b9d985b1a5908185b5bdd5b9d60921b6044820152606401610636565b5f546040516323b872dd60e01b8152336004820152306024820152604481018390526001600160a01b03909116906323b872dd906064016020604051808303815f875af1158015610f65573d5f5f3e3d5ffd5b505050506040513d601f19601f82011682018060405250810190610f8991906125a8565b610fc75760405162461bcd60e51b815260206004820152600f60248201526e151c985b9cd9995c8819985a5b1959608a1b6044820152606401610636565b6001600160a01b0382165f9081526001602052604081208054839290610fee908490612569565b90915550506040518181526001600160a01b038316907f4f7fd5c9e17300a4800fd572ea53fc291e2ee7470d73346d16b357faee4e72109060200160405180910390a25050565b5f818152600460208181526040808420815160e0810183528154815260018201548185015260028201548184015260038201546001600160401b0381166060830152600160401b90046001600160a01b031660808201529381018054835181860281018601909452808452869594929360a0860193909291908301828280156110db57602002820191905f5260205f20905b8154815260200190600101908083116110c7575b50505091835250506005919091015460ff161515602090910152606081015160a0820151519192506001600160401b03161161111a5750600192915050565b428160400151101561112f5750600292915050565b505f92915050565b7f80bb2b638cc20bc4d0a60d66940f3ab4a00c1d7b313497ca82fb0b4ab007930180546060915f5160206127575f395f51905f52916104669061251d565b61050733838361186b565b5f61118a82611035565b5f838152600460208181526040808420815160e0810183528154815260018201548185015260028201548184015260038201546001600160401b0381166060830152600160401b90046001600160a01b03166080820152938101805483518186028101860190945280845296975094959394909360a086019383018282801561123057602002820191905f5260205f20905b81548152602001906001019080831161121c575b50505091835250506005919091015460ff16151560209091015290505f82600281111561125f5761125f61243e565b036112ac5760405162461bcd60e51b815260206004820152601760248201527f4368616c6c656e6765206973206e6f7420636c6f7365640000000000000000006044820152606401610636565b8060c00151156112fe5760405162461bcd60e51b815260206004820152601b60248201527f4368616c6c656e676520697320616c726561647920636c6f73656400000000006044820152606401610636565b5f61130884610e07565b5f858152600460209081526040808320600501805460ff1916600117905585516001600160a01b038516845260029092528220805493945090929091906113509084906125c3565b92505081905550837f7347f19be7808fa9f926930c5e109c7c36565c300146fcdab43435bc9bb93a6c846040516113879190612452565b60405180910390a26040518481527ff8e1a15aba9398e019f0b49df1a4fde98ee17ae345cb5f6b5e2c27f5033e8ce79060200160405180910390a160018360028111156113d6576113d661243e565b03610699575f546080830151835160405163a9059cbb60e01b81526001600160a01b039283166004820152602481019190915291169063a9059cbb906044016020604051808303815f875af1158015611431573d5f5f3e3d5ffd5b505050506040513d601f19601f8201168201806040525081019061145591906125a8565b5081516001600160a01b0382165f908152600160205260408120805490919061147f9084906125c3565b909155505050505050565b611495848484610611565b610699338585858561191a565b60606114ad82611590565b505f6114b7611a42565b90505f8151116114d55760405180602001604052805f815250611500565b806114df84611a62565b6040516020016114f09291906125ed565b6040516020818303038152906040525b9392505050565b6001600160a01b039182165f9081527f80bb2b638cc20bc4d0a60d66940f3ab4a00c1d7b313497ca82fb0b4ab00793056020908152604080832093909416825291909152205460ff1690565b61155b611728565b6001600160a01b03811661158457604051631e4fbdf760e01b81525f6004820152602401610636565b61158d816117fb565b50565b5f5f61159b83611af1565b90506001600160a01b03811661044157604051637e27328960e01b815260048101849052602401610636565b5f9081527f80bb2b638cc20bc4d0a60d66940f3ab4a00c1d7b313497ca82fb0b4ab007930460205260409020546001600160a01b031690565b610bec8383836001611b2a565b5f5f5160206127575f395f51905f528161162685611af1565b90506001600160a01b0384161561164257611642818587611c3d565b6001600160a01b0381161561167e5761165d5f865f5f611b2a565b6001600160a01b0381165f908152600383016020526040902080545f190190555b6001600160a01b038616156116ae576001600160a01b0386165f9081526003830160205260409020805460010190555b5f85815260028301602052604080822080546001600160a01b0319166001600160a01b038a811691821790925591518893918516917fddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef91a495945050505050565b610507828260405180602001604052805f815250611ca1565b3361175a7f9016d09d72d40fdae2fd8ceac6b6234c7706214fd39c1cd1e609a0528c199300546001600160a01b031690565b6001600160a01b031614610e7a5760405163118cdaa760e01b8152336004820152602401610636565b7f19457468657265756d205369676e6564204d6573736167653a0a3332000000005f908152601c839052603c81206001600160a01b0385166117c58285611cb8565b6001600160a01b03161495945050505050565b6117e0611ce0565b61158d81611d29565b6117f1611ce0565b6105078282611d31565b7f9016d09d72d40fdae2fd8ceac6b6234c7706214fd39c1cd1e609a0528c19930080546001600160a01b031981166001600160a01b03848116918217845560405192169182907f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0905f90a3505050565b5f5160206127575f395f51905f526001600160a01b0383166118ab57604051630b61174360e31b81526001600160a01b0384166004820152602401610636565b6001600160a01b038481165f818152600584016020908152604080832094881680845294825291829020805460ff191687151590811790915591519182527f17307eab39ab6107e8899845ad3d59bd9653f200f220920489ca2b5937696c31910160405180910390a350505050565b6001600160a01b0383163b15611a3b57604051630a85bd0160e11b81526001600160a01b0384169063150b7a029061195c908890889087908790600401612601565b6020604051808303815f875af1925050508015611996575060408051601f3d908101601f191682019092526119939181019061263d565b60015b6119fd573d8080156119c3576040519150601f19603f3d011682016040523d82523d5f602084013e6119c8565b606091505b5080515f036119f557604051633250574960e11b81526001600160a01b0385166004820152602401610636565b805181602001fd5b6001600160e01b03198116630a85bd0160e11b14611a3957604051633250574960e11b81526001600160a01b0385166004820152602401610636565b505b5050505050565b606060405180606001604052806027815260200161277760279139905090565b60605f611a6e83611d61565b60010190505f816001600160401b03811115611a8c57611a8c612325565b6040519080825280601f01601f191660200182016040528015611ab6576020820181803683370190505b5090508181016020015b5f19016f181899199a1a9b1b9c1cb0b131b232b360811b600a86061a8153600a8504945084611ac057509392505050565b5f9081527f80bb2b638cc20bc4d0a60d66940f3ab4a00c1d7b313497ca82fb0b4ab007930260205260409020546001600160a01b031690565b5f5160206127575f395f51905f528180611b4c57506001600160a01b03831615155b15611c0d575f611b5b85611590565b90506001600160a01b03841615801590611b875750836001600160a01b0316816001600160a01b031614155b8015611b9a5750611b988185611507565b155b15611bc35760405163a9fbf51f60e01b81526001600160a01b0385166004820152602401610636565b8215611c0b5784866001600160a01b0316826001600160a01b03167f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b92560405160405180910390a45b505b5f93845260040160205250506040902080546001600160a01b0319166001600160a01b0392909216919091179055565b611c48838383611e38565b610bec576001600160a01b038316611c7657604051637e27328960e01b815260048101829052602401610636565b60405163177e802f60e01b81526001600160a01b038316600482015260248101829052604401610636565b611cab8383611e9d565b610bec335f85858561191a565b5f5f5f5f611cc68686611efe565b925092509250611cd68282611f47565b5090949350505050565b7ff0c57e16840df040f15088dc2f81fe391c3923bec73e23a9662efc9c229c6a0054600160401b900460ff16610e7a57604051631afcd79f60e31b815260040160405180910390fd5b61155b611ce0565b611d39611ce0565b5f5160206127575f395f51905f5280611d52848261269c565b5060018101610699838261269c565b5f8072184f03e93ff9f4daa797ed6e38ed64bf6a1f0160401b8310611d9f5772184f03e93ff9f4daa797ed6e38ed64bf6a1f0160401b830492506040015b6d04ee2d6d415b85acef81000000008310611dcb576d04ee2d6d415b85acef8100000000830492506020015b662386f26fc100008310611de957662386f26fc10000830492506010015b6305f5e1008310611e01576305f5e100830492506008015b6127108310611e1557612710830492506004015b60648310611e27576064830492506002015b600a83106104415760010192915050565b5f6001600160a01b03831615801590611e955750826001600160a01b0316846001600160a01b03161480611e715750611e718484611507565b80611e955750826001600160a01b0316611e8a836115c7565b6001600160a01b0316145b949350505050565b6001600160a01b038216611ec657604051633250574960e11b81525f6004820152602401610636565b5f611ed283835f61160d565b90506001600160a01b03811615610bec576040516339e3563760e11b81525f6004820152602401610636565b5f5f5f8351604103611f35576020840151604085015160608601515f1a611f2788828585611fff565b955095509550505050611f40565b505081515f91506002905b9250925092565b5f826003811115611f5a57611f5a61243e565b03611f63575050565b6001826003811115611f7757611f7761243e565b03611f955760405163f645eedf60e01b815260040160405180910390fd5b6002826003811115611fa957611fa961243e565b03611fca5760405163fce698f760e01b815260048101829052602401610636565b6003826003811115611fde57611fde61243e565b03610507576040516335e2f38360e21b815260048101829052602401610636565b5f80807f7fffffffffffffffffffffffffffffff5d576e7357a4501ddfe92f46681b20a084111561203857505f915060039050826120bd565b604080515f808252602082018084528a905260ff891692820192909252606081018790526080810186905260019060a0016020604051602081039080840390855afa158015612089573d5f5f3e3d5ffd5b5050604051601f1901519150506001600160a01b0381166120b457505f9250600191508290506120bd565b92505f91508190505b9450945094915050565b828054828255905f5260205f20908101928215612100579160200282015b828111156121005782518255916020019190600101906120e5565b5061210c929150612110565b5090565b5b8082111561210c575f8155600101612111565b6001600160e01b03198116811461158d575f5ffd5b5f60208284031215612149575f5ffd5b813561150081612124565b5f81518084528060208401602086015e5f602082860101526020601f19601f83011685010191505092915050565b602081525f6115006020830184612154565b5f602082840312156121a4575f5ffd5b5035919050565b80356001600160a01b03811681146121c1575f5ffd5b919050565b5f5f604083850312156121d7575f5ffd5b6121e0836121ab565b946020939093013593505050565b5f602082840312156121fe575f5ffd5b611500826121ab565b8781526020808201889052604082018790526001600160401b03861660608301526001600160a01b038516608083015260e060a0830181905284519083018190525f91850190610100840190835b81811015612273578351835260209384019390920191600101612255565b505084151560c085015291506122869050565b98975050505050505050565b5f5f5f606084860312156122a4575f5ffd5b6122ad846121ab565b92506122bb602085016121ab565b929592945050506040919091013590565b5f5f5f5f5f60a086880312156122e0575f5ffd5b85359450602086013593506040860135925060608601356001600160401b038116811461230b575f5ffd5b9150612319608087016121ab565b90509295509295909350565b634e487b7160e01b5f52604160045260245ffd5b5f82601f830112612348575f5ffd5b81356001600160401b0381111561236157612361612325565b604051601f8201601f19908116603f011681016001600160401b038111828210171561238f5761238f612325565b6040528181528382016020018510156123a6575f5ffd5b816020850160208301375f918101602001919091529392505050565b5f5f5f606084860312156123d4575f5ffd5b833592506020840135915060408401356001600160401b038111156123f7575f5ffd5b61240386828701612339565b9150509250925092565b5f5f6040838503121561241e575f5ffd5b612427836121ab565b9150612435602084016121ab565b90509250929050565b634e487b7160e01b5f52602160045260245ffd5b602081016003831061247257634e487b7160e01b5f52602160045260245ffd5b91905290565b801515811461158d575f5ffd5b5f5f60408385031215612496575f5ffd5b61249f836121ab565b915060208301356124af81612478565b809150509250929050565b5f5f5f5f608085870312156124cd575f5ffd5b6124d6856121ab565b93506124e4602086016121ab565b92506040850135915060608501356001600160401b03811115612505575f5ffd5b61251187828801612339565b91505092959194509250565b600181811c9082168061253157607f821691505b60208210810361254f57634e487b7160e01b5f52602260045260245ffd5b50919050565b634e487b7160e01b5f52601160045260245ffd5b8082018082111561044157610441612555565b5f6001820161258d5761258d612555565b5060010190565b634e487b7160e01b5f52603260045260245ffd5b5f602082840312156125b8575f5ffd5b815161150081612478565b8181038181111561044157610441612555565b5f81518060208401855e5f93019283525090919050565b5f611e956125fb83866125d6565b846125d6565b6001600160a01b03858116825284166020820152604081018390526080606082018190525f9061263390830184612154565b9695505050505050565b5f6020828403121561264d575f5ffd5b815161150081612124565b601f821115610bec57805f5260205f20601f840160051c8101602085101561267d5750805b601f840160051c820191505b81811015611a3b575f8155600101612689565b81516001600160401b038111156126b5576126b5612325565b6126c9816126c3845461251d565b84612658565b6020601f8211600181146126fb575f83156126e45750848201515b5f19600385901b1c1916600184901b178455611a3b565b5f84815260208120601f198516915b8281101561272a578785015182556020948501946001909201910161270a565b508482101561274757868401515f19600387901b60f8161c191681555b50505050600190811b0190555056fe80bb2b638cc20bc4d0a60d66940f3ab4a00c1d7b313497ca82fb0b4ab007930068747470733a2f2f7265736f75726365732e6f67756f67752e6d652f6368616c6c656e6765732fa2646970667358221220b682be4b2227ae8784bf943a325289d777147f3195e48b168091c3fe1f7baf5564736f6c634300081c0033";

type OGUOGUConstructorParams =
  | [signer?: Signer]
  | ConstructorParameters<typeof ContractFactory>;

const isSuperArgs = (
  xs: OGUOGUConstructorParams
): xs is ConstructorParameters<typeof ContractFactory> => xs.length > 1;

export class OGUOGU__factory extends ContractFactory {
  constructor(...args: OGUOGUConstructorParams) {
    if (isSuperArgs(args)) {
      super(...args);
    } else {
      super(_abi, _bytecode, args[0]);
    }
  }

  override getDeployTransaction(
    overrides?: NonPayableOverrides & { from?: string }
  ): Promise<ContractDeployTransaction> {
    return super.getDeployTransaction(overrides || {});
  }
  override deploy(overrides?: NonPayableOverrides & { from?: string }) {
    return super.deploy(overrides || {}) as Promise<
      OGUOGU & {
        deploymentTransaction(): ContractTransactionResponse;
      }
    >;
  }
  override connect(runner: ContractRunner | null): OGUOGU__factory {
    return super.connect(runner) as OGUOGU__factory;
  }

  static readonly bytecode = _bytecode;
  static readonly abi = _abi;
  static createInterface(): OGUOGUInterface {
    return new Interface(_abi) as OGUOGUInterface;
  }
  static connect(address: string, runner?: ContractRunner | null): OGUOGU {
    return new Contract(address, _abi, runner) as unknown as OGUOGU;
  }
}
