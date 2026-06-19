# MediBELL: Dependency & Environment Report

This document reports the software dependencies, package versions, virtual environment configurations, and resolution of dependency conflicts for the MediBELL project.

---

## 1. Core Dependency Specifications

The project dependencies are managed via [requirements.txt](file:///home/dev/Desktop/projects/MediBELL_DP/requirements.txt):

```text
scikit-learn==1.5.2
pandas==2.2.3
numpy==2.2.3
matplotlib==3.9.2
joblib==1.4.2
pyyaml==6.0.2
web3==6.20.0
python-dotenv==1.0.1
flask==3.0.3
requests==2.32.3
```

- **`web3`:** Enables Ethereum node RPC connections, EIP-1559 transaction building, and smart contract queries.
- **`python-dotenv`:** Dynamically loads configuration values from `.env` into environment variables.
- **`flask`:** Powers the prediction and auditing endpoints.
- **`joblib`:** Handles serialized machine learning weight exports (.pkl).

---

## 2. Dependency Conflict Resolutions

During the local environment setup, the following conflicts and resolution steps were handled:

### A. EVM Compiler Hardfork Opcode Mismatch
- **Issue:** Modern Solidity compilers (like `solc 0.8.20+`) default to the Cancun EVM hardfork, generating Cancun-specific opcodes (e.g. `PUSH0`, `MCOPY`) which throw execution reverts on older EVM nodes like local Ganache.
- **Resolution:** Compiled `MediBellRegistry.sol` using Solidity `0.8.19` targeting the Paris EVM hardfork, ensuring total backward compatibility on both Ganache and Sepolia.

### B. Flask Server Port Conflict
- **Issue:** Spinning up a new Flask instance throws `Address already in use` error if another server process is already running on port 5000 in the background.
- **Resolution:** Integrated background task tracking to kill redundant Flask processes and release port 5000 before initializing API test sweeps.

### C. Web3 Testnet Upfront Balance Requirement
- **Issue:** Standard web3.py calls with a high gas limit (e.g. `1,000,000` gas) fail node validation checks if the wallet balance is less than `gas_limit * gas_price`, even if the actual gas consumed is much lower.
- **Resolution:** Optimized gas limits to `787,904` for deployment and `500,000` for transaction anchoring, keeping upfront checks compatible with small faucet balances.
