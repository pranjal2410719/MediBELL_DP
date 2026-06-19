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
            fake_cid = f"QmSimulatedModelHash{self.calculate_sha256(file_path)[:16]}XyZ987"
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

    def download_model(self, cid, output_path):
        """
        Downloads a model artifact file from IPFS by CID.
        Uses public IPFS gateways in real mode, or simulation mode.
        """
        if self.simulation_mode:
            print(f"[IPFS SIMULATION] Downloading CID: {cid} to {output_path}...")
            # In simulation, we write a dummy file or copy a local simulator file if known
            with open(output_path, "wb") as f:
                f.write(b"[SIMULATED MODEL DATA] serialized-weights")
            return output_path

        # Real Mode: Try multiple public gateways
        gateways = [
            f"https://gateway.pinata.cloud/ipfs/{cid}",
            f"https://cloudflare-ipfs.com/ipfs/{cid}",
            f"https://ipfs.io/ipfs/{cid}"
        ]
        
        print(f"[IPFS] Fetching CID {cid} from IPFS network...")
        for gw in gateways:
            try:
                print(f" -> Trying gateway: {gw}")
                response = requests.get(gw, timeout=30)
                if response.status_code == 200:
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                    print(f"[IPFS] Successfully downloaded to {output_path}")
                    return output_path
                else:
                    print(f" -> Gateway returned status code {response.status_code}")
            except Exception as e:
                print(f" -> Failed to fetch from gateway {gw}: {e}")
                
        raise Exception(f"Failed to download IPFS CID {cid} from all attempted gateways.")

    def calculate_sha256(self, file_path):
        """
        Calculates SHA256 checksum of a file.
        """
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def verify_model_integrity(self, cid, original_file_path):
        """
        Downloads a file via its CID and compares its SHA256 hash to the original file.
        Returns (True, downloaded_file_path) if they match, or raises ValueError.
        """
        if not os.path.exists(original_file_path):
            raise FileNotFoundError(f"Original file not found: {original_file_path}")

        # In simulation mode, mock the match to be realistic if we want it to pass,
        # but if we actually want to test the full pipeline, we mock the download content
        # to match the original content.
        temp_dir = "temp_ipfs_downloads"
        os.makedirs(temp_dir, exist_ok=True)
        temp_file = os.path.join(temp_dir, f"downloaded_{cid}.pkl")

        if self.simulation_mode:
            print("[IPFS SIMULATION] Verifying model integrity...")
            # For realistic simulation test, we copy the original file to simulate successful download
            import shutil
            shutil.copyfile(original_file_path, temp_file)
        else:
            self.download_model(cid, temp_file)

        original_hash = self.calculate_sha256(original_file_path)
        downloaded_hash = self.calculate_sha256(temp_file)

        print(f"[IPFS] Integrity Verification:")
        print(f" -> Original SHA256:   {original_hash}")
        print(f" -> Downloaded SHA256: {downloaded_hash}")

        if original_hash == downloaded_hash:
            print("[IPFS] Success: Hashes match! Content integrity verified.")
            return True, temp_file
        else:
            # Clean up temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise ValueError("Integrity check failed: SHA256 hashes do not match!")

