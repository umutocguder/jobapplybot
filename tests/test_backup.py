# Created by 11hopem (11 Hopem Software Ltd. Şti.)
# Copyright (c) 2026 11hopem. All rights reserved.
# Licensed under 11 Hopem Software Proprietary License.

import unittest
import tempfile
import shutil
import os
import json
from jobapplybot.backup import (
    create_autonomous_backup,
    verify_backup_integrity,
    restore_from_backup
)
from jobapplybot.tracker import ApplicationTracker

class TestJobApplyBackup(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_create_autonomous_backup_generates_snapshot_and_sha256(self):
        apps = [
            {"id": "APP-1", "company": "Apple", "position": "iOS Engineer", "status": "APPLIED"}
        ]
        meta = create_autonomous_backup(apps, backup_dir=self.test_dir)

        self.assertIn("sha256", meta)
        self.assertEqual(len(meta["sha256"]), 64)
        self.assertEqual(meta["applications_count"], 1)

        latest_path = os.path.join(self.test_dir, "jobapply_latest_backup.json")
        self.assertTrue(os.path.exists(latest_path))

    def test_verify_backup_integrity(self):
        apps = [
            {"id": "APP-1", "company": "Google", "position": "Backend Engineer", "status": "INTERVIEW"}
        ]
        create_autonomous_backup(apps, backup_dir=self.test_dir)
        self.assertTrue(verify_backup_integrity(backup_dir=self.test_dir))

    def test_restore_from_backup(self):
        apps = [
            {"id": "APP-100", "company": "11hopem", "position": "Lead Architect", "status": "OFFER"}
        ]
        create_autonomous_backup(apps, backup_dir=self.test_dir)
        restored = restore_from_backup(backup_dir=self.test_dir)

        self.assertEqual(restored["app"], "JobApplyBot")
        self.assertEqual(len(restored["applications"]), 1)
        self.assertEqual(restored["applications"][0]["company"], "11hopem")

    def test_tracker_auto_triggers_backup_on_save(self):
        storage_file = os.path.join(self.test_dir, "apps.json")
        backup_dir = os.path.join(self.test_dir, "backups")

        tracker = ApplicationTracker(storage_path=storage_file, backup_dir=backup_dir)
        tracker.add_application("Acme Corp", "Python Developer", 95.0)

        self.assertTrue(verify_backup_integrity(backup_dir=backup_dir))

    def test_checksum_log_capped_at_30(self):
        apps = [{"id": "APP-1", "company": "Test", "position": "Dev"}]
        for _ in range(35):
            create_autonomous_backup(apps, backup_dir=self.test_dir)

        checksum_file = os.path.join(self.test_dir, "jobapply_checksums.json")
        self.assertTrue(os.path.exists(checksum_file))

        with open(checksum_file, "r") as f:
            log = json.load(f)

        self.assertLessEqual(len(log), 30)
        self.assertGreater(len(log), 0)

if __name__ == "__main__":
    unittest.main()
