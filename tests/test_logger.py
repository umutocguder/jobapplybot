# Created by 11Hopem
# Copyright (c) 2026 11Hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

import unittest
import os
import tempfile
import json
from jobapplybot.logger import SecureLogger, scrub_sensitive_data, to_firestore_fields
from jobapplybot.firebase_config import FIREBASE_ECOSYSTEM_CONFIG

class TestSecureLogger(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.logger = SecureLogger(log_dir=self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_firebase_config(self):
        self.assertEqual(FIREBASE_ECOSYSTEM_CONFIG["account"], "umutocgdr@gmail.com")
        self.assertEqual(FIREBASE_ECOSYSTEM_CONFIG["project_id"], "hopem-software-cloud")
        self.assertTrue("hopem-software-cloud" in FIREBASE_ECOSYSTEM_CONFIG["firestore_base_url"])

    def test_scrub_sensitive_data(self):
        raw = "Aday Ahmet Kaya TCKN: 12345678901 ve telefon: 05321112233 başvuru yaptı."
        sanitized = self.logger.scrub_sensitive_data(raw)

        self.assertNotIn("12345678901", sanitized)
        self.assertNotIn("05321112233", sanitized)
        self.assertIn("[TCKN_REDACTED]", sanitized)
        self.assertIn("[PHONE_REDACTED]", sanitized)

    def test_scrub_dictionary_and_cards(self):
        dirty = {
            "password": "SecretPassword123",
            "api_key": "AIzaSyKeySecret",
            "token": "Bearer token-value-123",
            "candidate": {
                "tckn": "98765432101",
                "phone": "05051234567",
                "credit_card": "4543 1234 5678 9012"
            },
            "notes": "Candidate with TCKN 98765432101 and card 4543 1234 5678 9012"
        }
        clean = scrub_sensitive_data(dirty)
        self.assertEqual(clean["password"], "***REDACTED***")
        self.assertEqual(clean["api_key"], "***REDACTED***")
        self.assertEqual(clean["token"], "***REDACTED***")
        self.assertEqual(clean["candidate"]["tckn"], "***REDACTED***")
        self.assertIn("[PHONE_REDACTED]", clean["candidate"]["phone"])
        self.assertEqual(clean["candidate"]["credit_card"], "***REDACTED***")
        self.assertNotIn("98765432101", clean["notes"])
        self.assertNotIn("4543 1234 5678 9012", clean["notes"])

    def test_to_firestore_fields(self):
        fields = to_firestore_fields({
            "appName": "jobapplybot",
            "applications": 42,
            "successRate": 85.5,
            "active": True,
            "notes": None
        })
        self.assertEqual(fields["appName"], {"stringValue": "jobapplybot"})
        self.assertEqual(fields["applications"], {"integerValue": "42"})
        self.assertEqual(fields["successRate"], {"doubleValue": 85.5})
        self.assertEqual(fields["active"], {"booleanValue": True})
        self.assertEqual(fields["notes"], {"nullValue": None})

    def test_multi_collection_routing(self):
        sec = self.logger.security("CV upload blocked: executable detected", tag="Security")
        self.assertEqual(sec["target_collection"], "security_audit_logs")

        tel = self.logger.telemetry("ATS score calculated", tag="Engine", metadata={"score": 92})
        self.assertEqual(tel["target_collection"], "telemetry_logs")

        vis = self.logger.visitor("User viewed proposal preview", tag="Web")
        self.assertEqual(vis["target_collection"], "visitor_logs")

        cr = self.logger.crash("Worker thread timeout", tag="Worker")
        self.assertEqual(cr["target_collection"], "crash_logs")

        perf = self.logger.performance("ats_match", 120.5)
        self.assertEqual(perf["target_collection"], "telemetry_logs")

    def test_log_file_created(self):
        self.logger.info("Application submitted successfully", tag="Submission")
        log_file = os.path.join(self.temp_dir.name, "telemetry.jsonl")
        self.assertTrue(os.path.exists(log_file))

        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Application submitted successfully", content)
            self.assertIn("hopem-software-cloud", content)

    def test_zero_crash_guarantee(self):
        res1 = self.logger.log("INFO", "Tag", None)
        self.assertIsNotNone(res1)
        res2 = self.logger.error("Error with broken meta", metadata=None)
        self.assertIsNotNone(res2)

if __name__ == '__main__':
    unittest.main()
