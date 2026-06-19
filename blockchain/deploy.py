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
    from blockchain.config import PROVIDER_URL, PRIVATE_KEY
    
    # If the provider is localhost and Ganache isn't running, start it
    if "127.0.0.1" in PROVIDER_URL or "localhost" in PROVIDER_URL:
        # Parse port if custom
        port = 8545
        if ":" in PROVIDER_URL.split("//")[-1]:
            try:
                port = int(PROVIDER_URL.split(":")[-1])
            except ValueError:
                pass
        start_ganache()
        
    print(f"[DEPLOY] Connecting to Ethereum provider at: {PROVIDER_URL}")
    w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))
    if not w3.is_connected():
        raise ConnectionError(f"Failed to connect to Ethereum provider at {PROVIDER_URL}")
        
    print("[DEPLOY] Successfully connected to blockchain provider.")
    
    # Load ABI and BIN
    abi_path = os.path.join(os.path.dirname(__file__), "abi", "MediBellRegistry.json")
    bin_path = os.path.join(os.path.dirname(__file__), "abi", "MediBellRegistry.bin")
    
    if not os.path.exists(abi_path) or not os.path.exists(bin_path):
        raise FileNotFoundError("Compiled contract files (ABI/BIN) not found. Run solc compilation first.")
        
    with open(abi_path, "r") as f:
        abi = json.load(f)
        
    with open(bin_path, "r") as f:
        bytecode = f.read().strip()
        
    # Instantiate contract factory
    MediBellRegistry = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    # Determine deployment account
    use_raw_tx = False
    if PRIVATE_KEY and not PRIVATE_KEY.startswith("0x0000"):
        account = w3.eth.account.from_key(PRIVATE_KEY)
        deployer_address = account.address
        use_raw_tx = True
        print(f"[DEPLOY] Deployer Account Address (from Private Key): {deployer_address}")
        # Get balance
        balance_wei = w3.eth.get_balance(deployer_address)
        balance_eth = w3.from_wei(balance_wei, "ether")
        print(f"[DEPLOY] Deployer Account Balance: {balance_eth:.6f} ETH")
        if balance_wei == 0:
            print("[DEPLOY] WARNING: Account balance is 0. Deployment will likely fail due to lack of funds.")
    else:
        # Fallback to Ganache accounts
        if len(w3.eth.accounts) > 0:
            deployer_address = w3.eth.accounts[0]
            print(f"[DEPLOY] Deployer Account Address (Unlocked): {deployer_address}")
        else:
            raise ValueError("No private key configured and no unlocked accounts available on provider.")
            
    print("[DEPLOY] Sending contract deployment transaction...")
    
    if use_raw_tx:
        # Sign construction transaction
        nonce = w3.eth.get_transaction_count(deployer_address)
        construct_tx = MediBellRegistry.constructor().build_transaction({
            'from': deployer_address,
            'nonce': nonce,
            'gas': 1000000
        })
        signed_tx = w3.eth.account.sign_transaction(construct_tx, private_key=PRIVATE_KEY)
        tx_hash_bytes = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_hash = w3.to_hex(tx_hash_bytes)
    else:
        # Local Ganache unlocked transaction
        tx_hash_bytes = MediBellRegistry.constructor().transact({'from': deployer_address})
        tx_hash = w3.to_hex(tx_hash_bytes)
        
    print(f"[DEPLOY] Transaction sent. Hash: {tx_hash}")
    print("[DEPLOY] Waiting for receipt confirmation...")
    
    # Wait for transaction confirmation
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash_bytes)
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

