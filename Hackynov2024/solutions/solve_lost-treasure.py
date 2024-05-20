from web3 import Web3, Account
import json
from time import sleep

priv_key = ""
infuraAPIKey = ""
with open("../config.json", "r") as f:
    config = json.loads(f.read())
    priv_key = config["eth_priv_key"]
    infuraAPIKey = config["infura_apikey"]


w3 = Web3(Web3.HTTPProvider(f"https://sepolia.infura.io/v3/{infuraAPIKey}"))
print(f'Connected to network with ID : {w3.net.version}')

account = Account.from_key(priv_key)
print(f'Loaded account {account.address}')

balance = w3.eth.get_balance(account.address)
print(f'Current account balance : {w3.from_wei(balance, "ether")} ETH')

contract_address = "0x6c73dF1F981C02177D2CB75134121B3392A03cE3"
contract_abi = [
        {
            "inputs": [],
            "name": "getChestPosition",
            "outputs": [
                {
                    "internalType": "string[]",
                    "name": "",
                    "type": "string[]"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "getSubmarinePosition",
            "outputs": [
                {
                    "internalType": "string[]",
                    "name": "",
                    "type": "string[]"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "goBackward",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "goForward",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "goLeft",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "goRight",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "resetPosition",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "undoMoving",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        }
    ]

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

sub_pos = contract.functions.getSubmarinePosition().call()
chest_pos = contract.functions.getChestPosition().call()

for pos in chest_pos:
    print(pos)
    contractFunc = None
    match pos:
        case "devant":
            contractFunc = contract.functions.goForward()
        case "derriere":
            contractFunc = contract.functions.goBackward()
        case "droite":
            contractFunc = contract.functions.goRight()
        case "gauche":
            contractFunc = contract.functions.goLeft()
    
    transaction = contractFunc.build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 100000,
        'gasPrice': w3.to_wei('40', 'gwei'),
    })
    
    signed_txn = w3.eth.account.sign_transaction(transaction, priv_key)
    
    sent_transaction = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    
    print(f"Send transaction {sent_transaction.hex()}")
    
    sleep(30)
    
    transaction_receipt = w3.eth.get_transaction_receipt(sent_transaction)
    print(f"Transaction receipt: {transaction_receipt}")

sub_pos = contract.functions.getSubmarinePosition().call()
chest_pos = contract.functions.getChestPosition().call()

print(f"Sub position: {sub_pos}\nChest position: {chest_pos}")
