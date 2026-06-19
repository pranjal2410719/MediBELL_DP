import os
import sys
import pandas as pd
import numpy as np
import joblib

# Add project root to path
sys.path.append(os.getcwd())

from fl_advanced.advanced_client import AdvancedFederatedClient
from fl_advanced.advanced_server import AdvancedFederatedServer

def run_production_simulation():
    print("\n" + "="*60)
    print("MEDIBELL PRODUCTION FL ARCHITECTURE TEST (25L SCALE)")
    print("====================================================")
    
    # 1. Configuration
    model_type = "mlp"
    epsilon = 10.0
    num_rounds = 15
    client_files = ["data/client_1.csv", "data/client_2.csv", "data/client_3.csv"]
    
    # 2. Setup Clients
    print(f"\n[1] Initializing {len(client_files)} Clients from local CSV files...")
    clients = []
    for i, file_path in enumerate(client_files):
        if not os.path.exists(file_path):
            print(f"Error: Missing data file {file_path}")
            return
        df = pd.read_csv(file_path)
        clients.append(AdvancedFederatedClient(i, df, model_type=model_type, epsilon=epsilon))
        print(f" -> Client {i} initialized with {len(df)} samples")

    server = AdvancedFederatedServer(model_type=model_type)
    global_weights = None
    
    # 3. Simulation
    print(f"\n[2] Starting Federated MLP Training ({num_rounds} Rounds)...")
    
    for r in range(num_rounds):
        print(f"\n--- Global Round {r+1} ---")
        updates = []
        
        for client in clients:
            update = client.train_local(global_weights)
            updates.append(update)
            print(f" Client {client.client_id}: Acc={update['acc']:.2%}, F1={update['f1']:.3f}, Noise={update['noise']:.4f}")
            
        print(" Server: Aggregating local weights via FedAvg...")
        global_weights = server.aggregate(updates)
        
        avg_acc = np.mean([u['acc'] for u in updates])
        avg_f1  = np.mean([u['f1'] for u in updates])
        print(f" Global Progress: Avg Accuracy={avg_acc:.2%}, Avg F1 Score={avg_f1:.3f}")

        # -------------------------------------------------------------
        # INTEGRATION HOOK: Blockchain & IPFS Register
        # -------------------------------------------------------------
        try:
            # 1. Export intermediate model to disk
            round_model_data = {
                'weights': global_weights,
                'model_type': model_type,
                'scaler': clients[0].scaler,
                'le': clients[0].le
            }
            os.makedirs("models", exist_ok=True)
            round_model_path = f"models/production_model_round_{r+1}.pkl"
            joblib.dump(round_model_data, round_model_path)
            
            from blockchain.ipfs_manager import IPFSManager
            from blockchain.chain_manager import ChainManager
            
            ipfs = IPFSManager()
            chain = ChainManager()
            
            print(f" -> Web3: Pinning round {r+1} model to IPFS...")
            cid = ipfs.upload_model(round_model_path)
            
            print(f" -> Web3: Anchoring round {r+1} audit record on-chain...")
            tx_hash = chain.register_round(
                round_num=r+1,
                accuracy=avg_acc * 100.0,
                cid=cid
            )
            print(f" -> Web3: Anchored successfully! Tx Hash: {tx_hash}")
        except Exception as e:
            print(f" -> Web3: Warning - Blockchain anchoring failed for round {r+1}: {e}")

    # 4. Save Final Global Model
    model_data = {
        'weights': global_weights,
        'model_type': model_type,
        'scaler': clients[0].scaler,
        'le': clients[0].le
    }
    output_path = "fl_advanced/production_global_model.pkl"
    joblib.dump(model_data, output_path)
    
    print("\n" + "="*60)
    print("PRODUCTION SCALE TEST COMPLETE")
    print(f"Architectue   : DP+FL (MLP)")
    print(f"Total Rows    : ~2.8 Lakhs (across 3 clients)")
    print(f"Final Outcome : Accuracy={avg_acc:.2%}, F1={avg_f1:.3f}")
    print(f"Model Artifact: {output_path}")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_production_simulation()
