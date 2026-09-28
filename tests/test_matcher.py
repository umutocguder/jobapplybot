# Created by 11hopem (11 Hopem Software Ltd. Şti.)
# Copyright (c) 2026 11hopem. All rights reserved.
# Licensed under 11 Hopem Software Proprietary License.

import unittest
from jobapplybot.matcher import ResumeMatcher

class TestResumeMatcher(unittest.TestCase):

    def setUp(self):
        self.matcher = ResumeMatcher()

    def test_tokenization_and_keywords(self):
        text = "Senior Python Developer with FastApi, Docker and SQL skills."
        keywords = self.matcher.extract_keywords(text)
        self.assertIn("python", keywords)
        self.assertIn("fastapi", keywords)
        self.assertIn("docker", keywords)
        self.assertIn("developer", keywords)
        self.assertNotIn("and", keywords)

    def test_high_match_score(self):
        resume = "Experienced Python developer with Django, PostgreSQL, Docker, AWS and CI/CD."
        job = "Looking for a Python developer with Docker and PostgreSQL."
        result = self.matcher.calculate_match_score(resume, job)

        self.assertGreater(result["score"], 60.0)
        self.assertIn("python", result["matched_keywords"])
        self.assertIn("docker", result["matched_keywords"])

    def test_empty_job_description(self):
        result = self.matcher.calculate_match_score("Python resume", "")
        self.assertEqual(result["score"], 0.0)
        self.assertEqual(result["total_job_keywords"], 0)

if __name__ == '__main__':
    unittest.main()
