# MediBELL: Project Analysis Report

This document performs a deep analysis of the MediBELL codebase, covering its purpose, feature completeness, AI/ML pipelines, privacy guarantees, and blockchain integration mechanisms.

---

## 1. Project Overview & Business Logic

### A. Purpose & Problem Statement
In digital health and IoT wearables, patient vitals must be collected continuously to predict disease risks. However, transmitting raw clinical records to a central cloud server violates **HIPAA and GDPR** compliance. 
**MediBELL** resolves this by keeping patient clinical records entirely decentralized on hospital edge nodes. It trains predictive models locally and aggregates only the mathematical weight updates (FedAvg) under strict mathematically bounded mathematical noise.

### B. Solution Architecture
1. **LDP Layer:** Patient vitals (BP, Heart Rate, SpO2, symptoms) are perturbed locally using Laplace Noise (numerical vitals) and Randomized Response (categorical symptoms).
2. **Federated Learning:** Edge clients train a local Multi-Layer Perceptron (MLP) on the perturbed data.
3. **Ledger Provenance:** The resulting global model weights are serialized, pinned to IPFS, and their cryptographic CIDs are immutably anchored on the Ethereum Sepolia blockchain, creating a verified provenance history.

---

## 2. Feature Analysis

| Feature | Category | Status | Notes |
| :--- | :--- | :--- | :--- |
| **Local Differential Privacy (LDP)** | Security | **Implemented** | Bounded noise via Laplace Mechanism and Randomized Response |
| **Federated Avg Aggregator** | ML Pipeline | **Implemented** | Combines weights across distributed edge clients |
| **MLP Classifier Model** | ML Architecture | **Implemented** | 128-64-32 neural layer predicting disease classes |
| **Solidity Registry Contract** | Blockchain | **Implemented** | Anchors CIDs, accuracies, and block timestamps |
| **EIP-1559 Deployer Engine** | DevOps | **Implemented** | Overwrites mempool transactions with high priority fees |
| **Pinata IPFS Uploader** | Storage | **Implemented** | Pins serialized weights off-chain |
| **SHA256 Integrity Verification** | Cryptography | **Implemented** | Downloads models from public gateways and matches hashes |
| **Flask API Auditor** | REST Services | **Implemented** | Dynamically verifies on-chain records via Web3 calls |
| **Role-based Multi-Sig Access** | Security | *Missing* | Deferred to production out-of-scope phase |

---

## 3. AI/ML & Federated Learning Pipeline

### A. Dataset Structure
- **Production Scale:** 2.8 Lakh samples split across three client hospital nodes (`data/client_1.csv`, `client_2.csv`, `client_3.csv`).
- **Features:** 40 symptom parameters (binary/ordinal) and vitals (Systolic BP, Diastolic BP, Heart Rate, SpO2).
- **Target:** 41 distinct disease outcomes (labeled via label encoder).

### B. MLP Training Loop
1. Local clients load their datasets and normalize features via `StandardScaler`.
2. Clients run local training epochs using a custom neural network architecture (128 input features, 64 hidden neurons, 32 hidden neurons, and 41 softmax output classes).
3. Local weights are extracted and aggregated at the server using the **Federated Averaging (FedAvg)** algorithm:
   $$\bar{w} = \sum_{k=1}^{K} \frac{n_k}{n} w_k$$

### C. Inference & Evaluation
- **Metrics:** Tracked via Classification Accuracy, F1 Score, and Epsilon tradeoff curves.
- **Privacy Bound:** Managed via Epsilon ($\epsilon$). Lower epsilon increases privacy noise but decreases accuracy, while higher epsilon approaches unperturbed accuracy levels.

---

## 4. Blockchain & IPFS Auditing System

### A. Smart Contract Interface
The smart contract [MediBellRegistry.sol](file:///home/dev/Desktop/projects/MediBELL_DP/blockchain/contracts/MediBellRegistry.sol) stores the following metrics for each training round:
- **Round number (`uint256`):** Identifies the global aggregation round.
- **CID (`string`):** The cryptographic Content Identifier on IPFS containing the serialized model joblib file.
- **Accuracy (`uint256`):** The average training accuracy of the round scaled by 100 to avoid floating point limits in Solidity.
- **Timestamp (`uint256`):** The block confirmation timestamp.

### B. Storage & Integrity Path
- **Serialization:** Joblib dumps dictionary `{weights, model_type, scaler, le}` into `models/production_model_round_X.pkl`.
- **IPFS Pinned CID:** The `.pkl` file is uploaded to the Pinata gateway.
- **Verification:** An auditor can query the CID from Etherscan, download it via `gateway.pinata.cloud`, and verify that the file's SHA256 checksum matches the locally calculated record, proving zero tampering.
