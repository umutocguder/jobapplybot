# Created by 11Hopem
# Copyright (c) 2026 11hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

import os
import shutil
import tempfile
import unittest
from jobapplybot.cli import main

class TestCLI(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.storage = os.path.join(self.test_dir, "test_apps.json")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_cli_help(self):
        exit_code = main([])
        self.assertEqual(exit_code, 0)

    def test_cli_profile(self):
        exit_code = main(["profile"])
        self.assertEqual(exit_code, 0)

    def test_cli_scan(self):
        exit_code = main(["scan", "--keywords", "ios,swift", "--limit", "3"])
        self.assertEqual(exit_code, 0)

    def test_cli_match(self):
        exit_code = main(["match", "--text", "Looking for a Senior Swift iOS developer with UIKit knowledge."])
        self.assertEqual(exit_code, 0)

    def test_cli_propose_freelance(self):
        exit_code = main([
            "propose",
            "--title", "iOS Mobile App for Restaurant",
            "--desc", "Need Swift developer to build food delivery iOS app.",
            "--client", "Sarah",
            "--type", "freelance",
            "--lang", "en"
        ])
        self.assertEqual(exit_code, 0)

    def test_cli_propose_corporate(self):
        exit_code = main([
            "propose",
            "--title", "Staff iOS Engineer",
            "--company", "Stripe",
            "--desc", "Payment SDK architecture with Swift and Combine.",
            "--type", "corporate",
            "--lang", "tr"
        ])
        self.assertEqual(exit_code, 0)

    def test_cli_apply_and_status(self):
        exit_code = main([
            "apply",
            "--company", "Uber",
            "--position", "iOS Engineer",
            "--score", "88.5",
            "--url", "https://uber.com/jobs/123",
            "--storage", self.storage
        ])
        self.assertEqual(exit_code, 0)

        stat_exit_code = main(["status", "--storage", self.storage])
        self.assertEqual(stat_exit_code, 0)

if __name__ == "__main__":
    unittest.main()
