# MediBELL: Project Contribution Report

This report outlines the boundaries, scope, and technical deliverables of the Blockchain and IPFS audit trial extension layer added to the MediBELL system by **Pranjal Yadav**.

---

## 1. What Existed Before?

**MediBELL** was originally a local, privacy-preserving IoT healthcare prediction system utilizing:
* **Local Differential Privacy (LDP):** Edge node perturbations (Laplace and Randomized Response) protecting patient vitals.
* **Federated Learning (FL):** Decentralized SGD and MLP training across hospital nodes.
* **Vitals & Clinical Data Prediction:** Interactive CLI for clinical diagnosis prediction.

**The Problem:** While the ML loops were functional, there was **no public verifiability or immutable audit trail**. Future developers, reviewers, and healthcare auditors had to trust that:
- The global models were trained on the stated edge node distributions.
- No model parameter tampering occurred post-training.
- The model accuracy metrics reported were accurate and untampered with.

---

## 2. What Was Added? (The Contribution)

This extension introduces a secure, decentralized auditing layer that hashes model weights per round, stores the serialized weights on IPFS, and anchors their CIDs on the Sepolia Ethereum testnet. This creates a publicly verifiable, immutable history of the model's training state.

Key features added:
1. **Immutable Smart Contract Registry:** A Solidity contract verifying model round metrics on-chain.
2. **IPFS Model Provenance Layer:** Serializes intermediate models (`.pkl`) and pins them to Pinata IPFS gateway.
3. **Cryptographic Integrity Checks:** Dynamic downloads from public IPFS gateways with SHA256 checksum mismatch verification.
4. **Dynamic Verified API:** An `/audit` GET endpoint in Flask that checks local transaction logs against on-chain Web3 contract states, validating accuracy.
5. **Sepolia Deployer Engine:** EIP-1559 transaction sender with high-priority gas configuration.

---

## 3. Which Files Were Created?

To prevent pollution of the original codebase, the auditing layer is isolated to the `blockchain/` module:
* [blockchain/contracts/MediBellRegistry.sol](file:///home/dev/Desktop/projects/MediBELL_DP/blockchain/contracts/MediBellRegistry.sol) — Registry Solidity contract.
* [blockchain/deploy.py](file:///home/dev/Desktop/projects/MediBELL_DP/blockchain/deploy.py) — EIP-1559 contract compiler and deployer.
* [blockchain/chain_manager.py](file:///home/dev/Desktop/projects/MediBELL_DP/blockchain/chain_manager.py) — Web3 round registrator.
* [blockchain/ipfs_manager.py](file:///home/dev/Desktop/projects/MediBELL_DP/blockchain/ipfs_manager.py) — Pinata uploader and integrity validator.
* [blockchain/config.py](file:///home/dev/Desktop/projects/MediBELL_DP/blockchain/config.py) — Configuration settings.
* [blockchain/simulation.py](file:///home/dev/Desktop/projects/MediBELL_DP/blockchain/simulation.py) — Simulation verification script.
* [tests/test_audit_api.py](file:///home/dev/Desktop/projects/MediBELL_DP/tests/test_audit_api.py) — Flask audit API unit tests.
* [tests/test_ipfs_integrity.py](file:///home/dev/Desktop/projects/MediBELL_DP/tests/test_ipfs_integrity.py) — SHA256 download unit tests.
* [docs/CONTRIBUTION_REPORT.md](file:///home/dev/Desktop/projects/MediBELL_DP/docs/CONTRIBUTION_REPORT.md) — This contribution report.

---

## 4. Which Files Were Modified?

We integrated the auditing hooks into the existing machine learning loops and REST endpoints:
* [fl_advanced/run_production_fl.py](file:///home/dev/Desktop/projects/MediBELL_DP/fl_advanced/run_production_fl.py) — Injected intermediate model exports (`production_model_round_X.pkl`), IPFS uploads, and blockchain registration hooks inside the global aggregation loop.
* [app.py](file:///home/dev/Desktop/projects/MediBELL_DP/app.py) — Exposed `GET /audit` endpoint calling Web3 contract states dynamically.
* [README.md](file:///home/dev/Desktop/projects/MediBELL_DP/README.md) — Added blockchain deployment guides near the top of the system description.
* [requirements.txt](file:///home/dev/Desktop/projects/MediBELL_DP/requirements.txt) — Appended `web3` and `python-dotenv` dependencies.
* [.gitignore](file:///home/dev/Desktop/projects/MediBELL_DP/.gitignore) — Ignored local keys, deployment address, and cache files (`.env`, `deployed_address.txt`, `audit_trail.json`).

---

## 5. What Remains Outside the Scope?

The following product enhancements are excluded from this contribution:
- **Hospital Node Identity System:** Multi-signature validations or custom DID keys for each hospital node.
- **DAO Governance & Token Economics:** Custom governance layers or DAO structures.
- **Advanced ZK-Proof Integrations:** Off-chain computations validation using zero-knowledge proofs.
