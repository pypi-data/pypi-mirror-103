CNS_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "GetAllContracts",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "string",
                "name": "name",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "version",
                "type": "string"
            }
        ],
        "name": "GetContractAddress",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "address",
                "name": "addr",
                "type": "address"
            }
        ],
        "name": "GetContractsByAddr",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "address",
                "name": "addr",
                "type": "address"
            }
        ],
        "name": "GetContractsByOwner",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "string",
                "name": "name",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "version",
                "type": "string"
            },
            {
                "internalType": "address",
                "name": "addr",
                "type": "address"
            }
        ],
        "name": "Register",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "string",
                "name": "name",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "version",
                "type": "string"
            }
        ],
        "name": "Unregister",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

LEDGER_MANAGER_ABI = [
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "string",
                "name": "ledgerJson",
                "type": "string"
            }
        ],
        "name": "CreateLedger",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "GetAllLedgers",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "string",
                "name": "ledgerName",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "nodeID",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "blsPubKey",
                "type": "string"
            }
        ],
        "name": "JoinLedger",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "string",
                "name": "nodeID",
                "type": "string"
            }
        ],
        "name": "JoinedLedgers",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "string",
                "name": "ledgerName",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "nodeID",
                "type": "string"
            }
        ],
        "name": "QuitLedger",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "string",
                "name": "ledgerName",
                "type": "string"
            }
        ],
        "name": "TerminateLedger",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

LEDGER_NODE_MANAGER_ABI = [
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "string",
                "name": "pubKey",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "blsPubKey",
                "type": "string"
            }
        ],
        "name": "Add",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "addr",
                "type": "address"
            }
        ],
        "name": "GrantPerm",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "List",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "string",
                "name": "pubKey",
                "type": "string"
            }
        ],
        "name": "Remove",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "addr",
                "type": "address"
            }
        ],
        "name": "RevokePerm",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "string",
                "name": "pubKey",
                "type": "string"
            },
            {
                "internalType": "uint8",
                "name": "nodeType",
                "type": "uint8"
            }
        ],
        "name": "UpdateNodeType",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

NODE_MANAGER_ABI = [
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "string",
                "name": "name",
                "type": "string"
            },
            {
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "internalType": "string",
                "name": "desc",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "publicKey",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "blsPubKey",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "hostAddress",
                "type": "string"
            },
            {
                "internalType": "uint16",
                "name": "rpcPort",
                "type": "uint16"
            },
            {
                "internalType": "uint16",
                "name": "p2pPort",
                "type": "uint16"
            }
        ],
        "name": "Add",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "string",
                "name": "name",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "desc",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "publicKey",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "blsPubKey",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "hostAddress",
                "type": "string"
            },
            {
                "internalType": "uint16",
                "name": "rpcPort",
                "type": "uint16"
            },
            {
                "internalType": "uint16",
                "name": "p2pPort",
                "type": "uint16"
            }
        ],
        "name": "Apply",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "string",
                "name": "name",
                "type": "string"
            },
            {
                "internalType": "uint8",
                "name": "auditStat",
                "type": "uint8"
            },
            {
                "internalType": "string",
                "name": "auditReason",
                "type": "string"
            }
        ],
        "name": "Audit",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "string",
                "name": "name",
                "type": "string"
            }
        ],
        "name": "Delete",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "string",
                "name": "name",
                "type": "string"
            }
        ],
        "name": "Disable",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "string",
                "name": "name",
                "type": "string"
            }
        ],
        "name": "Enable",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "string",
                "name": "name",
                "type": "string"
            }
        ],
        "name": "GetByName",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "string",
                "name": "publicKey",
                "type": "string"
            }
        ],
        "name": "GetByPublicKey",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "ListAll",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "string",
                "name": "hostAddress",
                "type": "string"
            }
        ],
        "name": "ListByHostAddress",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "address",
                "name": "owner",
                "type": "address"
            }
        ],
        "name": "ListByOwner",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "uint8",
                "name": "status",
                "type": "uint8"
            }
        ],
        "name": "ListByStat",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "uint8",
                "name": "nodeType",
                "type": "uint8"
            }
        ],
        "name": "ListByType",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "string",
                "name": "name",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "hostAddress",
                "type": "string"
            },
            {
                "internalType": "uint16",
                "name": "rpcPort",
                "type": "uint16"
            },
            {
                "internalType": "uint16",
                "name": "p2pPort",
                "type": "uint16"
            },
            {
                "internalType": "string",
                "name": "desc",
                "type": "string"
            }
        ],
        "name": "Update",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "string",
                "name": "name",
                "type": "string"
            },
            {
                "internalType": "uint8",
                "name": "nodeType",
                "type": "uint8"
            }
        ],
        "name": "UpdateType",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

PARAM_MANAGER_ABI = [
    {
        "constant": False,
        "inputs": [],
        "name": "DisableDeploy",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [],
        "name": "EnableDeploy",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "GetSystemParameter",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "uint64",
                "name": "blockGasLimit",
                "type": "uint64"
            }
        ],
        "name": "UpdateBlockGasLimit",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "bool",
                "name": "isProduceEmptyBlock",
                "type": "bool"
            }
        ],
        "name": "UpdateIsProduceEmptyBlock",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "bool",
                "name": "isTxUseGas",
                "type": "bool"
            }
        ],
        "name": "UpdateIsTxUseGas",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "uint64",
                "name": "blockGasLimit",
                "type": "uint64"
            },
            {
                "internalType": "uint64",
                "name": "txGasLimit",
                "type": "uint64"
            },
            {
                "internalType": "bool",
                "name": "isTxUseGas",
                "type": "bool"
            },
            {
                "internalType": "bool",
                "name": "isProduceEmptyBlock",
                "type": "bool"
            },
            {
                "internalType": "bool",
                "name": "enableDeploy",
                "type": "bool"
            }
        ],
        "name": "UpdateSystemParameter",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "uint64",
                "name": "txGasLimit",
                "type": "uint64"
            }
        ],
        "name": "UpdateTxGasLimit",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

RE_ENC_ABI = [
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "string",
                "name": "cipher",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "ownerPk1",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "reEncryptKey",
                "type": "string"
            }
        ],
        "name": "ReEncrypt",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]

USER_MANAGER_ABI = [
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "addr",
                "type": "address"
            },
            {
                "internalType": "string",
                "name": "name",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "mobile",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "email",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "desc",
                "type": "string"
            },
            {
                "internalType": "uint64",
                "name": "roles",
                "type": "uint64"
            }
        ],
        "name": "Add",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "addr",
                "type": "address"
            },
            {
                "internalType": "uint64",
                "name": "roles",
                "type": "uint64"
            }
        ],
        "name": "AddRoles",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "addr",
                "type": "address"
            },
            {
                "internalType": "uint8",
                "name": "auditStat",
                "type": "uint8"
            },
            {
                "internalType": "string",
                "name": "auditReason",
                "type": "string"
            }
        ],
        "name": "Audit",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "addr",
                "type": "address"
            }
        ],
        "name": "Delete",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "addr",
                "type": "address"
            }
        ],
        "name": "Disable",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "addr",
                "type": "address"
            }
        ],
        "name": "Enable",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "address",
                "name": "addr",
                "type": "address"
            }
        ],
        "name": "GetByAddr",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "string",
                "name": "name",
                "type": "string"
            }
        ],
        "name": "GetByName",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "address",
                "name": "addr",
                "type": "address"
            },
            {
                "internalType": "uint64",
                "name": "roles",
                "type": "uint64"
            }
        ],
        "name": "HasRoles",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "uint32",
                "name": "pageNum",
                "type": "uint32"
            },
            {
                "internalType": "uint32",
                "name": "pageSize",
                "type": "uint32"
            }
        ],
        "name": "PageAll",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "uint64",
                "name": "roles",
                "type": "uint64"
            },
            {
                "internalType": "uint32",
                "name": "pageNum",
                "type": "uint32"
            },
            {
                "internalType": "uint32",
                "name": "pageSize",
                "type": "uint32"
            }
        ],
        "name": "PageByRoles",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "internalType": "uint8",
                "name": "status",
                "type": "uint8"
            },
            {
                "internalType": "uint32",
                "name": "pageNum",
                "type": "uint32"
            },
            {
                "internalType": "uint32",
                "name": "pageSize",
                "type": "uint32"
            }
        ],
        "name": "PageByStat",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "string",
                "name": "name",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "mobile",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "email",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "desc",
                "type": "string"
            },
            {
                "internalType": "uint64",
                "name": "roles",
                "type": "uint64"
            }
        ],
        "name": "Register",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "addr",
                "type": "address"
            },
            {
                "internalType": "uint64",
                "name": "roles",
                "type": "uint64"
            }
        ],
        "name": "RemoveRoles",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "addr",
                "type": "address"
            },
            {
                "internalType": "uint64",
                "name": "roles",
                "type": "uint64"
            }
        ],
        "name": "SetRoles",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "internalType": "address",
                "name": "addr",
                "type": "address"
            },
            {
                "internalType": "string",
                "name": "mobile",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "email",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "desc",
                "type": "string"
            }
        ],
        "name": "Update",
        "outputs": [
            {
                "internalType": "int32",
                "name": "",
                "type": "int32"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
