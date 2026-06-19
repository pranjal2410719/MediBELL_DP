# MediBELL: Project Progress & Integration Report

This progress report summarizes the technical advancements, features implemented, and milestones achieved for the **MediBELL Privacy-Preserving IoT Healthcare System** fork.

---

## 📅 Project Milestones & Progress

| Component | Initial Status | Current Status | Notes |
| :--- | :--- | :--- | :--- |
| **Local ML Environment** | Missing local datasets / baseline models | **100% Completed** | Regenerated clinical data and trained SGD/MLP models |
| **Solidity Smart Contract** | Not implemented | **100% Completed** | Written, compiled (solc 0.8.19), and duplicate-protected |
| **IPFS Storage Layer** | Simulated CIDs only | **100% Completed** | Integrates with live Pinata API, downloads from public gateways, and verifies integrity using SHA256 hashes |
| **Blockchain Manager** | Offline/None | **100% Completed** | Handles transaction signing, gas estimation, and EIP-1559 priority fee packing |
| **Audit Trails & API** | None | **100% Completed** | Exposes Flask `GET /audit` with dynamic on-chain Web3 verification checks |
| **Sepolia Testnet Deployment** | Local Ganache only | **100% Completed** | Deployed at `0xd4015AD2259801a6E9b2A66B5d38Ac79Db111A88` on Sepolia |

---

## 🛠️ Step-by-Step Implementation Details

### Phase 1: Local ML Recovery & Setup
- **Dataset Synthesis:** Created the `generate_missing_datasets.py` script to bypass Git exclusions. This generated `synthetic_dataset_25k_40symptoms.csv` and initialized standard/DP models locally.
- **Privacy Verification:** Validated Local Differential Privacy (LDP) boundaries and Laplace mechanisms.

### Phase 2: Registry Smart Contract Creation
- **Contract Design:** Developed `MediBellRegistry.sol` to track federated learning rounds:
  ```solidity
  struct RoundInfo {
      uint256 round;
      string cid;
      uint256 accuracy;
      uint256 timestamp;
  }
  ```
- **Duplicate Protection:** Implemented contract-level constraints to prevent tampering:
  ```solidity
  require(rounds[_round].timestamp == 0, "Round already registered");
  ```
- **Compilation Compatibility:** Targeted compiler version `0.8.19` (Paris EVM) to avoid Cancun-specific opcode mismatches (e.g., `PUSH0`, `MCOPY`) on local development blockchains.

### Phase 3: IPFS Manager & Integrity Verification
- **Pinata API Integration:** Configured the manager to pin serialized model weights (`.pkl` artifacts) directly to the Pinata Gateway, returning actual IPFS CIDs (e.g., `Qmbozu5G2J...`).
- **Cryptographic Verification:** Implemented downloading from public gateways (`gateway.pinata.cloud`, `cloudflare-ipfs.com`) and verifying that the downloaded model's SHA256 checksum matches the original model hash.

### Phase 4: Dynamic Flask Audit API
- Exposed a `GET /audit` route in `app.py`.
- **Live Verification:** If `BLOCKCHAIN_SIMULATION_MODE` is disabled, the server queries the Sepolia contract using the recorded transaction hash and round number. If the on-chain record matches the local cache, the API appends `"on_chain_verified": true`.

### Phase 5: Sepolia Ethereum Testnet Migration
- **Secure Key Storage:** Populated RPC URLs and wallet private keys securely via a local-only `.env` file (excluded from Git).
- **EIP-1559 Fee Optimization:**
  - Deployment gas limit optimized to `1,500,000` to cover bytecode storage limits (consuming `787,904` gas).
  - Explicitly specified EIP-1559 fees (`3.0 Gwei` priority fee, `10.0 Gwei` max fee) to overwrite stuck transactions in the mempool (replace-by-fee).
  - Round registration gas limits set to `500,000` to prevent testnet out-of-gas reverts.
- **Active Deployment:**
  - **Sepolia Contract Address:** `0xd4015AD2259801a6E9b2A66B5d38Ac79Db111A88`
  - **Mined Round 1 Transaction Hash:** `0xc34db71cff3bcba9babacad2c21840b360d09e97e7c3f9c54c3f87732711c36d`

---

## 🧪 Automated Testing Results

All tests pass successfully inside the virtual environment:
1. `tests/test_validation.py` - Core inputs and vitals structure.
2. `tests/test_ldp.py` - LDP bounds validation.
3. `tests/test_predict_pipeline.py` - ML model outputs.
4. `tests/test_audit_api.py` - Flask endpoint `/audit` mocking and formatting.
5. `tests/test_ipfs_integrity.py` - SHA256 calculations, Pinata pinning, public downloads, and integrity matching.

> [!TIP]
> Run all tests locally with:
> ```bash
> .venv/bin/python -m pytest
> ```

---

## 📈 Summary of Achievements
MediBELL has evolved from a local healthcare AI design into a **publicly verifiable Web3 clinical AI pipeline**. Any external verifier or judge can query Etherscan, download the exact model from IPFS, check its SHA256 hash, and prove the provenance, accuracy, and compliance of the federated models without trusting the server or having access to sensitive patient clinical records.
