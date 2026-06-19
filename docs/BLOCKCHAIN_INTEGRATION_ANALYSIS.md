# MediBELL: Blockchain & IPFS Integration Analysis

This document traces the Federated Learning (FL) pipeline, model serialization formats, and save locations, and defines the integration hooks for anchoring global models onto Blockchain and IPFS.

---

## 1. Current Federated Learning Flow

MediBELL features three entry points for Federated Learning simulation:

### A. Standard Simulation (`run_federated_sim.py`)
- **Flow:** Shuffles and partitions the 25k clinical dataset across 3 hospital nodes in-memory.
- **Model Type:** Linear model (`SGDClassifier` with log loss).
- **Execution:** Runs `FederatedClient.train_local()` for each round, then calls `FederatedServer.aggregate()` (FedAvg) to combine weights.
- **Artifact Export:** **None.** Weights are maintained strictly in-memory during execution.

### B. Advanced Simulation (`fl_advanced/run_advanced_sim.py`)
- **Flow:** Partitions the 25k clinical dataset across 3 local nodes in-memory.
- **Model Type:** Supports `SGDClassifier` or Multi-Layer Perceptron (`MLPClassifier`).
- **Execution:** Iterates over local epochs, sends weights to `AdvancedFederatedServer`, and aggregates using FedAvg.
- **Artifact Export:** Saves the final global model to `fl_advanced/global_model_advanced.pkl` at the end of the simulation.

### C. Production Scale Simulation (`fl_advanced/run_production_fl.py`)
- **Flow:** Loads three pre-partitioned client datasets (`data/client_1.csv`, `client_2.csv`, `client_3.csv`), each containing 93,750 samples (~2.8L scale).
- **Model Type:** Deep Multi-Layer Perceptron (MLP) architecture.
- **Execution:** Performs local training epochs, transmits weight tensors to the server, and runs FedAvg.
- **Artifact Export:** Saves the final global model to `fl_advanced/production_global_model.pkl` at the end of the simulation.

---

## 2. Current Model Flow & Save Locations

### A. Export Formats
The models are exported as dictionary objects containing weights, architectures, scalers, and encoders. They are serialized using `joblib` (.pkl format):
```python
model_data = {
    'weights': global_weights,
    'model_type': model_type,
    'scaler': scaler_instance,
    'le': label_encoder_instance
}
```

### B. Save Locations
- **Standard Baseline (No DP):** `models/disease_model.pkl` (Only baseline, not federated).
- **DP Baseline (Local RF):** `models/dp_model.pkl` (Only local training, not federated).
- **Advanced Federated Simulation:** `fl_advanced/global_model_advanced.pkl`.
- **Production Federated Scale:** `fl_advanced/production_global_model.pkl`.

---

## 3. Core Verification Findings
1. **No Round-by-Round Persistence:** Currently, neither `run_production_fl.py` nor `run_advanced_sim.py` saves intermediate model weights between global rounds. The `global_weights` dictionary is updated in-memory and only serialized to disk once training finishes.
2. **First Technical Task:** To verify the blockchain trail per round, we must implement an intermediate model export step. We will serialize the global model at the end of every round:
   - For advanced sim: `fl_advanced/global_model_round_{round}.pkl`
   - For production sim: `fl_advanced/production_model_round_{round}.pkl`

---

## 4. Blockchain & IPFS Integration Hook Location

The primary integration hook will reside in the main training loops of `run_production_fl.py` and `run_advanced_sim.py`.

### Target Hook Point:
At the end of each training round, immediately after aggregation and accuracy metrics computation:

```python
# Location: fl_advanced/run_production_fl.py (around line 55) or run_advanced_sim.py (around line 66)
for r in range(num_rounds):
    # ... Local training and weight aggregation ...
    global_weights = server.aggregate(updates)
    avg_acc = np.mean([u['acc'] for u in updates])
    
    # ---------------------------------------------
    # INTEGRATION HOOK: Blockchain & IPFS Register
    # ---------------------------------------------
    if blockchain_enabled:
        # 1. Export intermediate model to disk
        round_model_path = f"fl_advanced/model_round_{r+1}.pkl"
        save_round_model(global_weights, round_model_path)
        
        # 2. Upload to IPFS (returns CID)
        cid = ipfs_manager.upload_model(round_model_path)
        
        # 3. Anchoring to Blockchain (returns Transaction Hash)
        tx_hash = chain_manager.register_round(
            round_num=r+1,
            accuracy=avg_acc,
            cid=cid
        )
```
This keeps the core FL logic clean while adding a secure, automated audit trail for auditing global healthcare models.
