# MediBELL: Sepolia Testnet & IPFS Deployment Guide

This guide details the steps to deploy the registry smart contract, set up Pinata credentials, and run the verified federated learning pipeline on the Sepolia Ethereum testnet.

---

## 📋 Prerequisites

Ensure you have the following installed and configured:
1. **Python 3.10+** (with packages from `requirements.txt`).
2. **Node.js** (for running Ganache locally during development).
3. **MetaMask** or another Ethereum Web3 wallet.
4. **Pinata Account** (for IPFS pinning API access).

---

## 🛠️ Step-by-Step Deployment Instructions

### Step 1: Environment Configuration
Create a [.env](file:///home/dev/Desktop/projects/MediBELL_DP/.env) file in the root of the project:
```bash
# Set simulation modes to False to use Sepolia + Pinata
BLOCKCHAIN_SIMULATION_MODE=False
IPFS_SIMULATION_MODE=False

# Paste your Pinata API Key and Secret (generated from Pinata Dashboard)
PINATA_API_KEY=your_pinata_api_key
PINATA_SECRET_API_KEY=your_pinata_secret_key

# Paste your Sepolia RPC Provider URL (e.g. from Alchemy or Infura)
WEB3_PROVIDER_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY

# Paste your Sepolia funded wallet private key (keep this strictly private)
PRIVATE_KEY=your_sepolia_wallet_private_key
```

### Step 2: Fund the Deployer Wallet
1. Open your MetaMask wallet and select the **Ethereum Sepolia** network.
2. Copy your wallet address.
3. Request test Sepolia ETH from a faucet:
   - **Sepolia PoW Faucet:** [https://sepolia-faucet.pk910.de/](https://sepolia-faucet.pk910.de/) (No mainnet balance check required)
   - **QuickNode Sepolia Faucet:** [https://faucet.quicknode.com/ethereum/sepolia](https://faucet.quicknode.com/ethereum/sepolia)
4. Verify your balance is at least `0.005 ETH` before proceeding.

### Step 3: Deploy the Smart Contract
Run the deployer script:
```bash
.venv/bin/python blockchain/deploy.py
```
This script will:
1. Connect to your Sepolia RPC.
2. Compile `blockchain/contracts/MediBellRegistry.sol` using Solidity `0.8.19`.
3. Sign and submit the construction transaction with optimized EIP-1559 gas limits (`1,500,000` limit, `3 Gwei` priority fee).
4. Save the contract address to `blockchain/deployed_address.txt`.

### Step 4: Run the Simulation & FL Pipeline
To test the full integration:
```bash
.venv/bin/python blockchain/simulation.py
```
To run the production-scale Federated Learning simulation which automatically aggregates weights, pins intermediate rounds, and registers them on-chain:
```bash
.venv/bin/python fl_advanced/run_production_fl.py
```

### Step 5: Start the Flask API
Start the Flask API to serve audit logs and check transaction proofs:
```bash
.venv/bin/python app.py
```
Query the verified audit list:
```bash
curl -s http://127.0.0.1:5000/audit
```
Look for `"on_chain_verified": true` in the output JSON.
