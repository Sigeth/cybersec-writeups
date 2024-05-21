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

contract_address = "0x646Ef1C6bA295fbfc2a78E96e2612FAfD7a1772d"
contract_abi = [
        {
            "inputs": [],
            "stateMutability": "nonpayable",
            "type": "constructor"
        },
        {
            "inputs": [],
            "name": "Keccak2__InvalidHash",
            "type": "error"
        },
        {
            "inputs": [],
            "name": "Keccak2__NotOwner",
            "type": "error"
        },
        {
            "inputs": [
                {
                    "internalType": "uint256",
                    "name": "secretNumber",
                    "type": "uint256"
                }
            ],
            "name": "changeOwner",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "getOwner",
            "outputs": [
                {
                    "internalType": "address",
                    "name": "",
                    "type": "address"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "getSecret",
            "outputs": [
                {
                    "internalType": "string",
                    "name": "",
                    "type": "string"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        }
    ]

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

found_secret_number = 8967850079341
transaction = contract.functions.changeOwner(found_secret_number).build_transaction({
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


print(f"Contract's owner : {contract.functions.getOwner().call()}")
