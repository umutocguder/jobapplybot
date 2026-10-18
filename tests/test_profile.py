# Created by 11Hopem
# Copyright (c) 2026 11hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

import os
import shutil
import tempfile
import unittest
from jobapplybot.profile import CandidateProfile

class TestCandidateProfile(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.profile_path = os.path.join(self.test_dir, "profile.json")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_default_profile_loads_valid_data(self):
        profile = CandidateProfile()
        self.assertEqual(profile.full_name, "Umut Öçgüder")
        self.assertIn("Senior iOS", profile.headline)
        self.assertIn("Swift", profile.all_skills_list())
        self.assertGreater(len(profile.experiences), 0)
        self.assertGreater(len(profile.projects), 0)

    def test_to_resume_text_contains_key_elements(self):
        profile = CandidateProfile()
        text = profile.to_resume_text()
        self.assertIn("Umut Öçgüder", text)
        self.assertIn("İşCep", text)
        self.assertIn("HomeWhiz", text)
        self.assertIn("Swift", text)

    def test_find_relevant_projects(self):
        profile = CandidateProfile()
        relevant = profile.find_relevant_projects(["Swift", "MQTT", "IoT"], limit=2)
        self.assertGreaterEqual(len(relevant), 1)
        self.assertEqual(relevant[0]["name"], "HomeWhiz IoT Platform")

    def test_save_and_load_profile(self):
        custom_data = {
            "full_name": "Test Candidate",
            "headline": "Lead Architect",
            "email": "test@candidate.com",
            "phone": "+90 555 111 22 33",
            "location": "Istanbul, Remote",
            "summary": "Building resilient systems.",
            "skills": {"languages": ["Python", "Swift"]},
            "experiences": [],
            "projects": []
        }
        profile = CandidateProfile(custom_data)
        profile.save(self.profile_path)
        self.assertTrue(os.path.exists(self.profile_path))

        loaded = CandidateProfile.load(self.profile_path)
        self.assertEqual(loaded.full_name, "Test Candidate")
        self.assertEqual(loaded.skills["languages"], ["Python", "Swift"])

if __name__ == "__main__":
    unittest.main()
