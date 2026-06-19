# blockchain/simulation.py
import os
import sys
import json

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from blockchain.ipfs_manager import IPFSManager
from blockchain.chain_manager import ChainManager
from blockchain.config import AUDIT_TRAIL_PATH

def run_integration_simulation():
    print("\n" + "="*50)
    print("MEDIBELL BLOCKCHAIN & IPFS INTEGRATION SIMULATION")
    print("="*50)
    
    # 1. Create a dummy model artifact for simulation
    dummy_model_dir = "models_sim"
    os.makedirs(dummy_model_dir, exist_ok=True)
    dummy_model_path = os.path.join(dummy_model_dir, "sim_global_model_round_1.pkl")
    
    print(f"\n[Step 1] Simulating model saving step...")
    with open(dummy_model_path, "w") as f:
        f.write("dummy-serialized-model-weights-and-metadata-round-1")
    print(f" -> Mock model artifact saved to: {dummy_model_path}")
    
    # 2. Upload to IPFS
    print(f"\n[Step 2] Triggering IPFS Upload...")
    ipfs = IPFSManager()
    cid = ipfs.upload_model(dummy_model_path)
    print(f" -> Retreived Content Identifier (CID): {cid}")
    
    # 3. Register to Blockchain
    print(f"\n[Step 3] Registering round details on-chain...")
    chain = ChainManager()
    mock_accuracy = 94.27
    tx_hash = chain.register_round(
        round_num=1,
        accuracy=mock_accuracy,
        cid=cid
    )
    print(f" -> Transaction Anchored successfully. Tx Hash: {tx_hash}")
    
    # 4. Display Audit Trail
    print(f"\n[Step 4] Reading local audit trail ledger...")
    if os.path.exists(AUDIT_TRAIL_PATH):
        with open(AUDIT_TRAIL_PATH, "r") as f:
            trail = json.load(f)
            print(json.dumps(trail, indent=2))
    else:
        print("Error: Audit trail ledger not found.")
        
    # Clean up dummy model
    try:
        os.remove(dummy_model_path)
        os.rmdir(dummy_model_dir)
    except Exception:
        pass
        
    print("\n" + "="*50)
    print("INTEGRATION SIMULATION RUN SUCCESSFUL")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_integration_simulation()
