# blockchain/deploy.py
import os
import sys
import time
import json
import socket
import subprocess
from web3 import Web3

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def start_ganache():
    if not is_port_open(8545):
        print("[DEPLOY] Ganache is not running. Starting a local Ganache development node...")
        subprocess.Popen(
            ["npx", "ganache", "--host", "127.0.0.1", "--port", "8545"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        for _ in range(15):
            time.sleep(1)
            if is_port_open(8545):
                print("[DEPLOY] Ganache started successfully on http://127.0.0.1:8545.")
                break
    else:
        print("[DEPLOY] Ganache is already running on http://127.0.0.1:8545.")

def deploy_contract():
    start_ganache()
    
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    if not w3.is_connected():
        raise ConnectionError("Failed to connect to Ganache blockchain.")
        
    print("[DEPLOY] Connected to Ganache.")
    
    # Load ABI and BIN
    abi_path = os.path.join(os.path.dirname(__file__), "abi", "MediBellRegistry.json")
    bin_path = os.path.join(os.path.dirname(__file__), "abi", "MediBellRegistry.bin")
    
    if not os.path.exists(abi_path) or not os.path.exists(bin_path):
        raise FileNotFoundError("Compiled contract files (ABI/BIN) not found. Run solc compilation first.")
        
    with open(abi_path, "r") as f:
        abi = json.load(f)
        
    with open(bin_path, "r") as f:
        bytecode = f.read().strip()
        
    # First Ganache account is deployer
    deployer_account = w3.eth.accounts[0]
    print(f"[DEPLOY] Deployer Account Address: {deployer_account}")
    
    # Instantiate contract factory
    MediBellRegistry = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    # Deploy contract
    print("[DEPLOY] Sending contract deployment transaction...")
    tx_hash = MediBellRegistry.constructor().transact({'from': deployer_account})
    
    # Wait for transaction confirmation
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = tx_receipt.contractAddress
    print(f"[DEPLOY] Contract deployed successfully!")
    print(f"[DEPLOY] Contract Address: {contract_address}")
    
    # Write deployed address to file
    address_file = os.path.join(os.path.dirname(__file__), "deployed_address.txt")
    with open(address_file, "w") as f:
        f.write(contract_address)
    print(f"[DEPLOY] Address written to: {address_file}")

if __name__ == "__main__":
    deploy_contract()
