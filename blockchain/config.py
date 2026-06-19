# blockchain/config.py
import os

# Toggles between fake services and actual endpoints
BLOCKCHAIN_SIMULATION_MODE = False
IPFS_SIMULATION_MODE = True

# IPFS Pinata Configuration (Placeholder for Real Mode)
PINATA_API_KEY = os.getenv("PINATA_API_KEY", "your_pinata_api_key")
PINATA_SECRET_API_KEY = os.getenv("PINATA_SECRET_API_KEY", "your_pinata_secret_key")

# Web3/Ethereum Provider Configuration (Placeholder for Real Mode)
PROVIDER_URL = os.getenv("WEB3_PROVIDER_URL", "http://127.0.0.1:8545")

# Dynamically load the deployed contract address if it exists
address_file = os.path.join(os.path.dirname(__file__), "deployed_address.txt")
if os.path.exists(address_file):
    with open(address_file, "r") as f:
        CONTRACT_ADDRESS = f.read().strip()
else:
    CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "0x0000000000000000000000000000000000000000")
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "0x0000000000000000000000000000000000000000000000000000000000000000")

# Local Audit Trail filepath
AUDIT_TRAIL_PATH = os.path.join(os.path.dirname(__file__), "audit_trail.json")
