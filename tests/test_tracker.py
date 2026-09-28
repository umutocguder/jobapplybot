# Created by 11hopem (11 Hopem Software Ltd. Şti.)
# Copyright (c) 2026 11hopem. All rights reserved.
# Licensed under 11 Hopem Software Proprietary License.

import unittest
import os
import tempfile
from jobapplybot.tracker import ApplicationTracker

class TestApplicationTracker(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "apps.json")
        self.tracker = ApplicationTracker(storage_path=self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_list_application(self):
        app = self.tracker.add_application("Acme Corp", "Backend Engineer", 85.5)
        self.assertEqual(app["company"], "Acme Corp")
        self.assertEqual(app["status"], "APPLIED")
        self.assertEqual(len(self.tracker.list_applications()), 1)

    def test_update_status(self):
        app = self.tracker.add_application("Beta Ltd", "DevOps Specialist", 92.0)
        app_id = app["id"]

        updated = self.tracker.update_status(app_id, "INTERVIEW", "HR called, scheduled round 1.")
        self.assertTrue(updated)

        apps = self.tracker.list_applications(status="INTERVIEW")
        self.assertEqual(len(apps), 1)
        self.assertEqual(apps[0]["notes"], "HR called, scheduled round 1.")

    def test_invalid_status_raises(self):
        app = self.tracker.add_application("Gamma Inc", "Frontend Lead")
        with self.assertRaises(ValueError):
            self.tracker.update_status(app["id"], "NOT_A_STATUS")

    def test_persistence(self):
        self.tracker.add_application("Delta LLC", "Fullstack", 78.0)
        # Re-initialize tracker pointing to the same file
        tracker2 = ApplicationTracker(storage_path=self.db_path)
        self.assertEqual(len(tracker2.list_applications()), 1)
        self.assertEqual(tracker2.list_applications()[0]["company"], "Delta LLC")

if __name__ == '__main__':
    unittest.main()
