import os
import sys
import pandas as pd
import numpy as np

# Add project root to path
sys.path.append(os.getcwd())

from fl.sim_utils import partition_data
from fl_advanced.advanced_client import AdvancedFederatedClient
from fl_advanced.advanced_server import AdvancedFederatedServer

def run_advanced_simulation():
    print("\n" + "="*50)
    print("MEDIBELL ADVANCED FEDERATED LEARNING SIMULATION")
    print("================================================")
    
    # 1. Configuration
    print("\n[1] Select Model Type:")
    print("1. Logistic Regression (Linear)")
    print("2. Neural Network (MLP - Non-Linear)")
    choice = input("Choice [1/2, default=1]: ").strip()
    model_type = "mlp" if choice == "2" else "logistic"
    
    eps_input = input("Enter Privacy Budget (Epsilon) [default=1.0]: ").strip()
    epsilon = float(eps_input) if eps_input else 1.0
    
    num_rounds = 5
    num_clients = 3
    data_path = "data/synthetic_dataset_25k_40symptoms.csv"
    
    if not os.path.exists(data_path):
        print(f"Error: Data not found at {data_path}")
        return

    # 2. Setup
    print(f"\n[2] Partitioning data for {num_clients} nodes...")
    partitions = partition_data(data_path, num_clients)
    
    clients = [
        AdvancedFederatedClient(i, partitions[i], model_type=model_type, epsilon=epsilon) 
        for i in range(num_clients)
    ]
    server = AdvancedFederatedServer(model_type=model_type)
    
    global_weights = None
    
    # 3. Simulation
    print(f"\n[3] Starting Simulation ({model_type.upper()})...")
    
    for r in range(num_rounds):
        print(f"\n--- Round {r+1}/{num_rounds} ---")
        updates = []
        
        for client in clients:
            update = client.train_local(global_weights)
            updates.append(update)
            print(f"Node {client.client_id}: Acc={update['acc']:.2%}, F1={update['f1']:.3f}, P={update['precision']:.3f}, R={update['recall']:.3f}")
            
        print("Server: Aggregating weights...")
        global_weights = server.aggregate(updates)
        
        # Calculate global accuracy
        avg_acc = np.mean([u['acc'] for u in updates])
        avg_f1  = np.mean([u['f1'] for u in updates])
        print(f"Global Stats: Avg Accuracy={avg_acc:.2%}, Avg F1 Score={avg_f1:.3f}")

    # 4. Save Final Global Model for Prediction
    import joblib
    model_data = {
        'weights': global_weights,
        'model_type': model_type,
        'scaler': clients[0].scaler,   # Use scaler from one trained client
        'le': clients[0].le            # Use label encoder from one trained client
    }
    joblib.dump(model_data, "fl_advanced/global_model_advanced.pkl")
    print(f"\n[4] Global Model saved to fl_advanced/global_model_advanced.pkl")

    print("\n" + "="*50)
    print("ADVANCED SIMULATION COMPLETE")
    print(f"Model Used    : {model_type.upper()}")
    print(f"Final Accuracy: {avg_acc:.2%}")
    print(f"Final F1 Score: {avg_f1:.3f}")
    print(f"Epsilon (\u03b5)    : {epsilon}")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_advanced_simulation()
