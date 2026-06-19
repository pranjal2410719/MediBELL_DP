# tests/test_audit_api.py
import os
import sys
import json
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from blockchain.config import AUDIT_TRAIL_PATH

class TestAuditAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.backup_path = AUDIT_TRAIL_PATH + ".bak"
        # Backup existing audit trail if any
        if os.path.exists(AUDIT_TRAIL_PATH):
            os.rename(AUDIT_TRAIL_PATH, self.backup_path)

    def tearDown(self):
        # Restore backup
        if os.path.exists(AUDIT_TRAIL_PATH):
            os.remove(AUDIT_TRAIL_PATH)
        if os.path.exists(self.backup_path):
            os.rename(self.backup_path, AUDIT_TRAIL_PATH)

    def test_audit_empty_response(self):
        # Test audit endpoint when no audit trail exists
        response = self.client.get("/audit")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_audit_with_mock_data(self):
        # Test audit endpoint when audit trail exists
        mock_data = [
            {
                "round": 1,
                "accuracy": 94.27,
                "cid": "QmSimulatedModelHash123",
                "timestamp": 1234567890
            }
        ]
        with open(AUDIT_TRAIL_PATH, "w") as f:
            json.dump(mock_data, f)
            
        response = self.client.get("/audit")
        self.assertEqual(response.status_code, 200)
        res_data = response.get_json()
        self.assertEqual(len(res_data), 1)
        self.assertEqual(res_data[0]["round"], 1)
        self.assertEqual(res_data[0]["accuracy"], 94.27)
        self.assertEqual(res_data[0]["cid"], "QmSimulatedModelHash123")

if __name__ == "__main__":
    unittest.main()
