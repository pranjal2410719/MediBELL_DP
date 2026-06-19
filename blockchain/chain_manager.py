# blockchain/chain_manager.py
import os
import json
import time
import hashlib
from blockchain.config import SIMULATION_MODE, PROVIDER_URL, CONTRACT_ADDRESS, PRIVATE_KEY, AUDIT_TRAIL_PATH

class ChainManager:
    def __init__(self):
        self.simulation_mode = SIMULATION_MODE
        
    def register_round(self, round_num, accuracy, cid):
        """
        Registers a federated round audit parameters to the ledger.
        Returns the transaction hash.
        """
        current_time = int(time.time())
        
        if self.simulation_mode:
            # 1. Generate fake transaction hash
            tx_data = f"{round_num}-{accuracy}-{cid}-{current_time}"
            tx_hash = "0x" + hashlib.sha256(tx_data.encode()).hexdigest()
            print(f"[CHAIN SIMULATION] Registered Round {round_num} -> Tx Hash: {tx_hash}")
            
            # 2. Append to local audit trail json file
            trail_record = {
                "round": round_num,
                "accuracy": round(float(accuracy), 4),
                "cid": cid,
                "timestamp": current_time
            }
            
            records = []
            if os.path.exists(AUDIT_TRAIL_PATH):
                try:
                    with open(AUDIT_TRAIL_PATH, "r") as f:
                        records = json.load(f)
                        if not isinstance(records, list):
                            records = []
                except Exception:
                    records = []
            
            # Append new record
            records.append(trail_record)
            
            # Write back
            with open(AUDIT_TRAIL_PATH, "w") as f:
                json.dump(records, f, indent=2)
                
            print(f"[CHAIN SIMULATION] Saved to local audit trail: {AUDIT_TRAIL_PATH}")
            return tx_hash
        else:
            # Real Mode: Connect to Web3 provider and call contract function registerRound
            try:
                from web3 import Web3
            except ImportError:
                raise ImportError("Web3 library not installed. Please run: pip install web3")
                
            w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))
            if not w3.is_connected():
                raise ConnectionError(f"Failed to connect to Ethereum provider at {PROVIDER_URL}")
                
            # Parse contract ABI (normally loaded from abi/MediBellRegistry.json)
            abi_path = os.path.join(os.path.dirname(__file__), "abi", "MediBellRegistry.json")
            if not os.path.exists(abi_path):
                raise FileNotFoundError(f"Contract ABI file missing at {abi_path}")
                
            with open(abi_path, "r") as f:
                contract_abi = json.load(f)
                
            contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)
            
            # Get account from private key
            account = w3.eth.account.from_key(PRIVATE_KEY)
            
            # Multiply accuracy by 100 to avoid floating point issues on-chain (e.g. 94.27% -> 9427)
            accuracy_integer = int(round(accuracy * 100))
            
            # Build transaction
            nonce = w3.eth.get_transaction_count(account.address)
            tx = contract.functions.registerRound(
                round_num,
                cid,
                accuracy_integer
            ).build_transaction({
                'from': account.address,
                'nonce': nonce,
                'gas': 200000,
                'gasPrice': w3.eth.gas_price
            })
            
            # Sign and send transaction
            signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
            tx_hash_bytes = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            tx_hash = w3.to_hex(tx_hash_bytes)
            
            print(f"[CHAIN] Transaction sent. Tx Hash: {tx_hash}")
            return tx_hash
