# Pull Request Summary: Blockchain & IPFS Model Auditing Layer

**Author:** Pranjal Yadav  
**Contact:** 2k24.cs1l.2410719@gmail.com | +91919920362  
**Links:** [GitHub Profile](https://github.com/pranjal2410719) | [LinkedIn Profile](https://www.linkedin.com/in/-pranjal22/)

---

## 📖 Problem
In distributed, privacy-preserving healthcare AI systems (like MediBELL), model validation, training verification, and data provenance are critical. Without a secure audit trail:
- Aggregated Federated Learning (FL) models could be secretly modified, swapped, or corrupted.
- There is no verifiable proof of training history showing which client contributed to which round, and under what accuracy parameters.
- Traditional centralized auditing databases present a single point of failure and lack cryptographic immutability.

## 🛠️ Solution
This pull request introduces a non-invasive, decentralized model provenance and auditing layer for MediBELL without modifying core Differential Privacy or Federated Learning algorithms:
1. **Model Storage via IPFS:** Joblib-serialized model parameters from each FL training round are uploaded/pinned to IPFS (via Pinata API).
2. **On-Chain Metadata Registry:** Cryptographic Content Identifiers (CIDs), accuracy metrics, round numbers, and block timestamps are anchored immutably on-chain to the `MediBellRegistry` smart contract (on Ethereum Sepolia / local Ganache).
3. **Automated Validation:** Automatic SHA-256 validation checks verify downloaded artifacts against on-chain hash registers to guarantee model integrity.
4. **Audit API Endpoint:** A Web3-enabled Flask endpoint `/audit` dynamically queries the smart contract state in real-time to return model provenance.

---

## 📂 Files Added & Modified

### Files Added
* **[`blockchain/contracts/MediBellRegistry.sol`](file:///home/dev/Desktop/projects/MediBELL_DP/blockchain/contracts/MediBellRegistry.sol):** Smart contract registry storing round index, IPFS CID, accuracy, and timestamp.
* **[`blockchain/deploy.py`](file:///home/dev/Desktop/projects/MediBELL_DP/blockchain/deploy.py):** Automated deployment utility for Sepolia testnet and local Ganache.
* **[`blockchain/ipfs_manager.py`](file:///home/dev/Desktop/projects/MediBELL_DP/blockchain/ipfs_manager.py):** Pinata API wrapper for uploading model weights and verifying downloaded file checksum hashes.
* **[`blockchain/simulation.py`](file:///home/dev/Desktop/projects/MediBELL_DP/blockchain/simulation.py):** Offline simulation runner verifying anchoring hooks.
* **[`tests/test_audit_api.py`](file:///home/dev/Desktop/projects/MediBELL_DP/tests/test_audit_api.py):** Integration tests for the Flask Web3 audit API.
* **[`tests/test_ipfs_integrity.py`](file:///home/dev/Desktop/projects/MediBELL_DP/tests/test_ipfs_integrity.py):** Tests for Pinata upload wrapper and SHA-256 verifiers.

### Files Modified
* **[`app.py`](file:///home/dev/Desktop/projects/MediBELL_DP/app.py):** Added Flask `/audit` endpoint and developer footprint header.
* **[`fl_advanced/run_production_fl.py`](file:///home/dev/Desktop/projects/MediBELL_DP/fl_advanced/run_production_fl.py):** Integrated non-invasive IPFS and Web3 aggregation hooks, and added footprint.
* **[`.gitignore`](file:///home/dev/Desktop/projects/MediBELL_DP/.gitignore):** Configured to ignore local context metadata and project brain files.
* **[`.env.example`](file:///home/dev/Desktop/projects/MediBELL_DP/.env.example):** Added default parameters for local simulation toggles.

---

## 🧪 Testing Performed

All unit, integration, and flow validation tests pass cleanly. The suite includes:
- **`tests/test_ldp.py`:** Verifies Local Differential Privacy boundaries and Randomized Response.
- **`tests/test_ipfs_integrity.py`:** Validates model pinning, CID generation, and SHA-256 match integrity.
- **`tests/test_audit_api.py`:** Checks that the `/audit` JSON format output structure query matches on-chain Web3 states.
- **`tests/test_validation.py`:** Ensures parameters correctness and data parsing.

### Test Results
```text
tests/test_audit_api.py ..                                               [ 18%]
tests/test_ipfs_integrity.py ..                                          [ 36%]
tests/test_ldp.py ...                                                    [ 63%]
tests/test_predict_pipeline.py .                                         [ 72%]
tests/test_validation.py ...                                             [100%]

======================== 11 passed, 1 warning in 3.23s =========================
```

---

## ⚠️ Known Limitations
- **Latency Bounded:** Direct Sepolia transactions are bounded by Ethereum block confirmation times (12-15 seconds). The code handles this gracefully with connection timeout indicators and fallback simulation warning modes.
- **Gateway Dependability:** Pinata public gateway retrieval speeds are subject to global IPFS bandwidth capacity.
