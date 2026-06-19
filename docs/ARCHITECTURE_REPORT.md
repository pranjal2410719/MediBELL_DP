# MediBELL: Architectural Report

This document outlines the software architecture, folder structure, service dependencies, and design patterns utilized in the MediBELL decentralized audit layer.

---

## 1. Folder Structure Breakdown

The codebase is organized into modular directories to enforce separation of concerns:

- `blockchain/` — Core decentralized audit logic:
  - `contracts/MediBellRegistry.sol` — Solidity smart contract registry.
  - `abi/` — Compiled contract compiler ABI and BIN outputs.
  - `config.py` — Dynamic configuration parsing `.env` file.
  - `deploy.py` — Solidity compiler and EIP-1559 deployer script.
  - `chain_manager.py` — Web3 provider interfaces.
  - `ipfs_manager.py` — Pinata API pinning and public gateway retrieval.
  - `simulation.py` — Offline simulation test pipeline.
- `fl_advanced/` — Advanced Federated Learning MLP models:
  - `run_production_fl.py` — Main entry point executing ~2.8L training scale.
  - `advanced_client.py` — Local client model training.
  - `advanced_server.py` — Server FedAvg aggregations.
- `dp/` — Core Differential Privacy Laplace and Randomized Response mechanisms.
- `docs/` — System manuals, contribution scopes, verification logs, and architectural reports.
- `tests/` — Automated test files covering LDP, API, and IPFS integrity matches.

---

## 2. Component Interactions & Data Flow

```
┌─────────────────┐             ┌─────────────────┐             ┌──────────────────┐
│   MLP Clients   │ ──────────► │ FedAvg Server   │ ──────────► │ joblib Serializer│
│  (Hospital LDP) │             │  (Aggregation)  │             │   (.pkl File)    │
└─────────────────┘             └─────────────────┘             └──────────────────┘
                                                                          │
                                                                          ▼
┌─────────────────┐             ┌─────────────────┐             ┌──────────────────┐
│ Ethereum Ledger │ ◄────────── │  Chain Manager  │ ◄────────── │  IPFS Manager    │
│  (Sepolia Registry)           │ (EIP-1559 Tx)   │ (CID Output)│   (Pinata API)   │
└─────────────────┘             └─────────────────┘             └──────────────────┘
```

1. **Local Training:** Distributed hospital client nodes train a deep MLP architecture locally, using LDP to add mathematical noise to their clinical datasets.
2. **FedAvg Aggregation:** Weights are aggregated at the server via the FedAvg algorithm.
3. **Weight Export:** The aggregated weights, scalers, and labels are saved into a `.pkl` joblib model file.
4. **Pinning:** The `.pkl` file is pinned to IPFS via Pinata.
5. **Anchoring:** The IPFS CID and average accuracy are signed and recorded on the `MediBellRegistry` contract on Sepolia.
6. **API Query:** Flask queries Etherscan dynamically to return verified statuses to the audit browser.

---

## 3. Core Architectural Design Patterns

### A. Non-Invasive Hooks (Decorator Pattern)
To ensure that Web3/storage tasks do not impact core clinical simulations, the blockchain and IPFS interfaces are written as non-invasive extensions. If a Sepolia RPC times out, the training loop logs a warning but proceeds with the simulation without crashing.

### B. Scaled Integer Mappings (EVM compatibility)
Solidity does not support floating point arithmetic natively. To save the round accuracy (e.g. `94.27%`), the values are scaled by 100 on-chain (`9427`) and decoded back on the API (`94.27`), preventing calculation loss.

### C. Unified Cache Indexing
The Flask `/audit` endpoint reads metadata logs from a local `audit_trail.json` file. It then uses the logged transaction hashes to query the Sepolia testnet dynamically using Web3, validating the authenticity of the records.
