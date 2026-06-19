# blockchain/ipfs_manager.py
import os
import hashlib
import requests
from blockchain.config import IPFS_SIMULATION_MODE, PINATA_API_KEY, PINATA_SECRET_API_KEY

class IPFSManager:
    def __init__(self):
        self.simulation_mode = IPFS_SIMULATION_MODE
        
    def upload_model(self, file_path):
        """
        Uploads a model artifact file to IPFS.
        Returns the IPFS Content Identifier (CID).
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Artifact file not found: {file_path}")
            
        if self.simulation_mode:
            # Generate a consistent fake CID based on file hash for realism
            hasher = hashlib.sha256()
            with open(file_path, 'rb') as f:
                buf = f.read()
                hasher.update(buf)
            file_hash = hasher.hexdigest()[:16]
            fake_cid = f"QmSimulatedModelHash{file_hash}XyZ987"
            print(f"[IPFS SIMULATION] Uploaded '{os.path.basename(file_path)}' -> CID: {fake_cid}")
            return fake_cid
        else:
            # Real Mode: Upload to Pinata IPFS gateway
            print(f"[IPFS] Uploading '{os.path.basename(file_path)}' to Pinata Gateway...")
            url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
            headers = {
                "pinata_api_key": PINATA_API_KEY,
                "pinata_secret_api_key": PINATA_SECRET_API_KEY
            }
            with open(file_path, "rb") as file_to_upload:
                files = {"file": (os.path.basename(file_path), file_to_upload)}
                response = requests.post(url, files=files, headers=headers)
                
            if response.status_code == 200:
                cid = response.json()["IpfsHash"]
                print(f"[IPFS] Successfully pinned. CID: {cid}")
                return cid
            else:
                raise Exception(f"Pinata IPFS pinning failed: {response.text}")
