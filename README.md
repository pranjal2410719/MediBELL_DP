# MediBELL: Privacy-Preserving IoT Healthcare System

MediBELL is a cutting-edge healthcare AI system designed with a focus on **IoT + Healthcare + Privacy-Preserving AI**. It leverages **Local Differential Privacy (LDP)** and **Federated Learning (FL)** to ensure that sensitive patient data remains protected, secure, and decentralized.

---

## 🚀 Key Features

- **Local Differential Privacy (LDP)**: Protects individual patient records at the edge using the **Laplace Mechanism** (for numeric vitals like age, heart rate, BP) and **Randomized Response** (for binary/categorical attributes like gender, smoker status, and symptom profiles).
- **Advanced Federated Learning (FL)**: Supports decentralized model training across multiple local nodes using the **Federated Averaging (FedAvg)** aggregation algorithm.
- **Deep MLP Architecture**: Leverages Multi-Layer Perceptrons (128-64-32 architecture) to capture complex non-linear symptom combinations and disease correlations.
- **IoT Integration**: Built to simulate and process continuous high-velocity health streams from wearables (Heart Rate, BP, SpO2, etc.).

---

## 🛠 Tech Stack

- **ML/DL Frameworks**: Scikit-Learn (SGDClassifier, MLPClassifier, RandomForestClassifier)
- **Core Logic**: NumPy, Pandas, Joblib, PyYAML
- **Visualization**: Matplotlib

---

## 📂 Project Structure

- `dp/`: Core Local Differential Privacy mechanisms (`ldp_mechanism.py`, `gender_dp.py`).
- `fl/`: Standard federated regression learning logic (Clients, Server, and Utilities).
- `fl_advanced/`: Advanced Deep Learning (MLP) federated structure and production scale simulations.
- `utils/`: Common preprocessing pipelines, config loaders, and predictability layers.
- `tests/`: Automated unit test suite verifying validation modules and privacy bounds.
- `visualizations/`: Generated evaluation plots (e.g., Epsilon tradeoff curves).
- `generate_missing_datasets.py`: Local utility to synthesize clinical/survey data and baseline models.

---

## 📊 Getting Started

### 1. Local Environment Setup
Clone the repository and set up a Python virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Generate Missing Datasets & Baseline Models
Since large CSV datasets and `.pkl` model binaries are excluded by Git (`.gitignore`), generate them locally first:
```bash
.venv/bin/python generate_missing_datasets.py
```
This utility creates:
- Clean clinical datasets (`data/synthetic_dataset_25k_40symptoms.csv`)
- Survey comparison datasets (`data/MODEL_2_MediBELL.csv` and `data/FINAL_DATABASE_MEDIBELL.csv`)
- Un-noised baseline model files under `models/`

### 3. Run Automated Unit Tests
Verify privacy mechanisms and validation structures:
```bash
.venv/bin/python -m unittest discover -s tests -p "test_*.py"
```

---

## 📈 Running Simulations & Experiments

### A. Run the Interactive Menu
To access baseline training, DP model fitting, local evaluation, epsilon budgeting experiments, and interactively predict diseases:
```bash
.venv/bin/python main.py
```

### B. Run the Advanced Production-Scale (25L) FL Simulation
To run a federated Multi-Layer Perceptron (MLP) simulation across three hospital nodes over **2.8 Lakh patient records** under LDP noise:
```bash
.venv/bin/python fl_advanced/run_production_fl.py
```
The aggregated global model weights will be saved to `fl_advanced/production_global_model.pkl`.

### C. Run the Advanced Patient Predictor
Query the trained global model interactively with patient vitals and symptom levels:
```bash
.venv/bin/python fl_advanced/predict_advanced.py
```

### D. Run Epsilon Tradeoff Experiments
Run localized DP evaluation and export tradeoff plots to `visualizations/`:
```bash
# Epsilon tradeoffs (with vs. without DP accuracy)
.venv/bin/python epsilon_experiment.py

# Clinical vs. Survey dataset accuracy degradation comparison
.venv/bin/python dp_comparison_experiment.py
```

---

## ⛓ Blockchain & IPFS Audit Trail

MediBELL includes a fully working decentralized audit layer that anchors federated learning models to the Ethereum blockchain and stores them on IPFS. This ensures **public verifiability** and **immutable provenance** of all trained models.

After each federated round:
1. The global aggregated model is saved as a serialized artifact.
2. The model is uploaded and pinned to **IPFS** (via Pinata API or simulation), returning a unique **Content Identifier (CID)**.
3. The CID, round number, average accuracy, and timestamp are written to the **MediBellRegistry** smart contract on Ethereum (via Ganache or Sepolia), generating an immutable transaction.
4. The local audit trail cache (`blockchain/audit_trail.json`) is updated, and can be publicly fetched/verified via the Flask API.

### 1. Environment Configuration (`.env`)
Create a `.env` file in the project root (using `.env.example` as a template):
```bash
# Toggle simulation modes (True/False)
BLOCKCHAIN_SIMULATION_MODE=False
IPFS_SIMULATION_MODE=True

# Pinata API credentials (Required for real IPFS pinning)
PINATA_API_KEY=your_api_key
PINATA_SECRET_API_KEY=your_secret_key

# Web3 provider URL (Defaults to local Ganache)
WEB3_PROVIDER_URL=http://127.0.0.1:8545

# Wallet private key (leave empty to auto-use Ganache unlocked account)
PRIVATE_KEY=
```

### 2. Deploying the Smart Contract
You can deploy the registry smart contract locally or to a public testnet:
- **Local Ganache (recommended for development)**:
  Make sure Ganache is running (starts automatically on port 8545 when deploying):
  ```bash
  .venv/bin/python blockchain/deploy.py
  ```
- **Sepolia Testnet**:
  1. Configure `WEB3_PROVIDER_URL` (e.g. Alchemy RPC) and `PRIVATE_KEY` (funded with Sepolia ETH) in `.env`.
  2. Run the deployer script:
     ```bash
     .venv/bin/python blockchain/deploy.py
     ```
  This script compiles the Solidity code, deploys the registry contract, and writes the address to `blockchain/deployed_address.txt`.

### 3. Testing the Integration
Run a mock integration pipeline that tests IPFS pinning, blockchain round anchoring, and local audit trail caching:
```bash
.venv/bin/python blockchain/simulation.py
```

### 4. Running the Flask Audit API
Start the local API server:
```bash
.venv/bin/python app.py
```
You can query the audit logs at:
- **Prediction endpoint (POST)**: `http://127.0.0.1:5000/predict`
- **Audit endpoint (GET)**: `http://127.0.0.1:5000/audit`

When `BLOCKCHAIN_SIMULATION_MODE=False` (real blockchain mode), the `/audit` endpoint automatically fetches the CIDs and accuracies from the smart contract on-chain and returns them with a `"on_chain_verified": true` property!

---

## 🛡 Privacy & Regulatory Compliance
- **Zero Raw Data Transfer**: Patient records stay on edge nodes; only mathematical weight matrices are shared via FedAvg.
- **Strict Privacy Bounds**: Epsilon ($\epsilon$) controls the math guarantee of individual privacy, protecting against membership inference attacks and ensuring HIPAA/GDPR compliance.
- **Synergy Optimization**: MLP captures non-linear features, minimizing accuracy loss under strict privacy budgets.

