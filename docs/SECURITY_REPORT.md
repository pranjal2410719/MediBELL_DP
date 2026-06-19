# MediBELL: Security Report

This report analyzes potential security vulnerabilities, credential/secret management strategies, smart contract execution security, data privacy metrics, and mitigation actions for the MediBELL decentralized audit layer.

---

## 1. Vulnerability Analysis & Risk Matrix

| Risk | Impact | Likelihood | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Credential Leakage** | Critical | High | Ignore `.env` from Git via `.gitignore` and enforce prompt API key rotation. |
| **Mempool Front-Running** | Medium | Medium | Implement signature verification on the smart contract registry. |
| **Out-of-Gas Transaction Revert** | High | Low | Enforce safe gas limits (`1.5M` for deployment, `500k` for updates) on testnets. |
| **Mempool Nonce Blockage** | High | High | Enforce EIP-1559 priority fee overrides (`3 Gwei` priority fee, `10 Gwei` max fee). |
| **Reconstruction Attack** | Medium | Low | Maintain strict Epsilon ($\epsilon$) privacy budgets to prevent data leakage. |

---

## 2. Secrets Management & Environment Isolation

### A. Environment Configuration
All credentials, API keys, private keys, and RPC endpoint URLs are isolated to the [.env](file:///home/dev/Desktop/projects/MediBELL_DP/.env) file. 

### B. Git Exclusion
The [.gitignore](file:///home/dev/Desktop/projects/MediBELL_DP/.gitignore) file explicitly ignores the following local files:
- `.env`
- `blockchain/deployed_address.txt`
- `blockchain/audit_trail.json`

This ensures no private keys or local test runs are pushed to public GitHub repositories.

---

## 3. Smart Contract Execution & Access Control

### A. Ownership Restrictions
The [MediBellRegistry.sol](file:///home/dev/Desktop/projects/MediBELL_DP/blockchain/contracts/MediBellRegistry.sol) smart contract defines an `onlyOwner` modifier:
```solidity
modifier onlyOwner() {
    require(msg.sender == owner, "Only owner can call this function");
    _;
}
```
Only the deployer account (controlled by the private key in `.env`) can call `registerRound`, preventing unauthorized entities from anchoring false training metrics.

### B. Tamper Prevention (Write-Once Constraint)
Round metrics cannot be overwritten once committed:
```solidity
require(rounds[_round].timestamp == 0, "Round already registered");
```
Even if the owner wallet is compromised, an attacker cannot modify or delete previously recorded round accuracies or model CIDs on the ledger.

---

## 4. Privacy & Production Mitigation Guidelines

1. **Rotate Credentials Periodically:** Any keys shared during debugging or log sharing must be revoked on the Pinata/Alchemy dashboard immediately.
2. **Burner Wallet Practices:** Always deploy using a burner wallet containing only the necessary test ETH. Never use wallets holding mainnet assets.
3. **Dynamic Gas Adaptation:** When network congestion spikes, EIP-1559 parameters must dynamically increase priority fees to ensure transaction confirmation.
