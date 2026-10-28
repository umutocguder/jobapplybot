# Created by 11Hopem
# Copyright (c) 2026 11hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

import os
import shutil
import tempfile
import unittest
from jobapplybot.tracker import ApplicationTracker
from jobapplybot.report import ApplicationReporter

class TestApplicationReporter(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.storage = os.path.join(self.test_dir, "apps.json")
        self.backup_dir = os.path.join(self.test_dir, "backups")
        self.tracker = ApplicationTracker(storage_path=self.storage, backup_dir=self.backup_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_statistics_empty_tracker(self):
        reporter = ApplicationReporter(self.tracker)
        stats = reporter.generate_statistics()
        self.assertEqual(stats["total_tracked"], 0)
        self.assertEqual(stats["interview_rate_pct"], 0.0)
        self.assertEqual(stats["offer_rate_pct"], 0.0)

    def test_statistics_with_applications(self):
        app1 = self.tracker.add_application("Apple", "iOS Lead", match_score=85.0)
        app2 = self.tracker.add_application("Google", "Mobile Architect", match_score=75.0)
        app3 = self.tracker.add_application("Amazon", "Software Dev", match_score=60.0)

        self.tracker.update_status(app1["id"], "INTERVIEW")
        self.tracker.update_status(app2["id"], "OFFER")

        reporter = ApplicationReporter(self.tracker)
        stats = reporter.generate_statistics()

        self.assertEqual(stats["total_tracked"], 3)
        self.assertEqual(stats["applied_count"], 3)
        # 2 interviews or offers out of 3 = 66.67%
        self.assertAlmostEqual(stats["interview_rate_pct"], 66.67, places=1)
        # 1 offer out of 3 = 33.33%
        self.assertAlmostEqual(stats["offer_rate_pct"], 33.33, places=1)
        self.assertAlmostEqual(stats["average_match_score"], 73.33, places=1)

    def test_generate_markdown_report(self):
        self.tracker.add_application("Netflix", "Senior iOS", match_score=90.0)
        reporter = ApplicationReporter(self.tracker)
        md = reporter.generate_markdown_report()
        self.assertIn("# 📊 JobApplyBot Pipeline Report", md)
        self.assertIn("Netflix", md)
        self.assertIn("%90.0", md)

if __name__ == "__main__":
    unittest.main()
