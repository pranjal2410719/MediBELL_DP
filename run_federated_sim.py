import os
import sys
import pandas as pd
from fl.sim_utils import partition_data
from fl.client import FederatedClient
from fl.server import FederatedServer

# Ensure root is in path
sys.path.append(os.getcwd())

def run_simulation(data_path, num_clients=3, rounds=5, epsilon=1.0):
    print("\n" + "="*40)
    print("MEDIBELL PRIVACY-PRESERVING AI SYSTEM")
    print("Integrated DP + Federated Learning")
    print("="*40)
    
    # 1. Partition Data (Simulate multiple hospitals)
    print(f"\n[1] Partitioning data for {num_clients} nodes...")
    partitions = partition_data(data_path, num_clients)
    
    # 2. Initialize Clients and Server
    clients = [FederatedClient(i, partitions[i], epsilon=epsilon) for i in range(num_clients)]
    server = FederatedServer()
    
    global_model = None
    
    # 3. Training rounds
    for r in range(rounds):
        print(f"\n--- Round {r+1}/{rounds} ---")
        client_updates = []
        
        for client in clients:
            print(f"Node {client.client_id}: Preprocessing with DP (epsilon={epsilon}) & Local Training...")
            update = client.train_local(global_model)
            client_updates.append(update)
        
        print("Server: Aggregating weights (FedAvg)...")
        global_model = server.aggregate(client_updates)
    
    print("\n" + "="*40)
    print("SIMULATION COMPLETE")
    print("="*40)
    print(f"Privacy Strategy: Local DP (Laplace + Randomized Response)")
    print(f"Training Strategy: Federated Learning (Decentralized)")
    print(f"Nodes Participated: {num_clients}")
    print(f"Global Model: Aggregated from {num_clients} models without raw data transfer.")
    print("="*40 + "\n")

if __name__ == "__main__":
    DATA_PATH = "data/synthetic_dataset_25k_40symptoms.csv"
    if os.path.exists(DATA_PATH):
        run_simulation(DATA_PATH)
    else:
        print(f"Error: Dataset not found at {DATA_PATH}")
