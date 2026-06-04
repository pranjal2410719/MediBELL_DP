# MediBELL: Privacy-Preserving IoT Healthcare System

MediBELL is a cutting-edge healthcare AI system designed with a focus on **IoT + Healthcare + Privacy-Preserving AI**. It leverages **Differential Privacy (DP)** and **Federated Learning (FL)** to ensure that sensitive patient data remains protected and decentralized.

## 🚀 Key Features

- **Local Differential Privacy (LDP)**: Protects individual level records using Laplace noise (numeric data) and Randomized Response (gender/categorical data).
- **Federated Learning (FL)**: Enables collaborative model training across multiple hospitals/nodes without ever sharing raw patient data.
- **IoT Integration**: Built to handle continuous data streams from wearables (Heart Rate, BP, SpO2, etc.).
- **Scalable Architecture**: Can scale from individual devices to large-scale healthcare networks.

## 🛠 Tech Stack

- **ML Framework**: Scikit-Learn
- **Core Logic**: NumPy, Pandas
- **Privacy Layers**: Custom DP mechanisms + FedAvg Aggregator

## 📂 Project Structure

- `dp/`: Core Local Differential Privacy mechanisms.
- `fl/`: Federated Learning logic (Clients, Server, and Utilities).
- `utils/`: Data preprocessing and helper functions.
- `train_dp.py`: Baseline DP training script.
- `run_federated_sim.py`: Simulation entry point for DP + FL.

## 📊 Getting Started

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Run DP Training (Local)
```bash
python train_dp.py
```

### 3. Run DP + Federated Learning Simulation
```bash
python run_federated_sim.py
```

## 🛡 Privacy Guarantees
- **Individual Privacy**: DP ensures that no individual's presence can be confidently identified from the model.
- **Organizational Privacy**: FL ensures that raw data stays within the local infrastructure of the healthcare provider.

---
*Developed with focus on HIPAA/GDPR compliance and secure decentralized AI.*
