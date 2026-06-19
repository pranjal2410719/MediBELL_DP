# tests/test_ipfs_integrity.py
import os
import sys
import unittest
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from blockchain.ipfs_manager import IPFSManager

class TestIPFSIntegrity(unittest.TestCase):
    def setUp(self):
        self.ipfs = IPFSManager()
        self.test_dir = "test_artifacts"
        os.makedirs(self.test_dir, exist_ok=True)
        self.test_file = os.path.join(self.test_dir, "test_model.pkl")
        with open(self.test_file, "wb") as f:
            f.write(b"dummy-model-binary-data")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        temp_dir = "temp_ipfs_downloads"
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

    def test_calculate_sha256(self):
        sha = self.ipfs.calculate_sha256(self.test_file)
        self.assertEqual(len(sha), 64)
        
        # Test content variation changes hash
        different_file = os.path.join(self.test_dir, "test_model_diff.pkl")
        with open(different_file, "wb") as f:
            f.write(b"dummy-model-binary-data-different")
        sha_diff = self.ipfs.calculate_sha256(different_file)
        self.assertNotEqual(sha, sha_diff)

    def test_upload_and_verify_integrity(self):
        cid = self.ipfs.upload_model(self.test_file)
        self.assertTrue(cid.startswith("Qm"))
        
        success, downloaded_path = self.ipfs.verify_model_integrity(cid, self.test_file)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(downloaded_path))

if __name__ == "__main__":
    unittest.main()
