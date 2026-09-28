# Created by 11hopem (11 Hopem Software Ltd. Şti.)
# Copyright (c) 2026 11hopem. All rights reserved.
# Licensed under 11 Hopem Software Proprietary License.

import unittest
import os
import tempfile
from jobapplybot.logger import SecureLogger

class TestSecureLogger(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.logger = SecureLogger(log_dir=self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_scrub_sensitive_data(self):
        raw = "Aday Ahmet Kaya TCKN: 12345678901 ve telefon: 05321112233 başvuru yaptı."
        sanitized = self.logger.scrub_sensitive_data(raw)

        self.assertNotIn("12345678901", sanitized)
        self.assertNotIn("05321112233", sanitized)
        self.assertIn("[TCKN_REDACTED]", sanitized)
        self.assertIn("[PHONE_REDACTED]", sanitized)

    def test_log_file_created(self):
        self.logger.info("Application submitted successfully", tag="Submission")
        log_file = os.path.join(self.temp_dir.name, "telemetry.jsonl")
        self.assertTrue(os.path.exists(log_file))

        with open(log_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Application submitted successfully", content)
            self.assertIn("hopem-software-cloud", content)

if __name__ == '__main__':
    unittest.main()
