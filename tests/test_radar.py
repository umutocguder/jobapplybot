# Created by 11Hopem
# Copyright (c) 2026 11hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

import unittest
from jobapplybot.radar import JobRadar
from jobapplybot.profile import CandidateProfile

class TestJobRadar(unittest.TestCase):

    def setUp(self):
        self.profile = CandidateProfile()
        self.radar = JobRadar(profile=self.profile)

    def test_sample_jobs_loaded(self):
        jobs = self.radar.get_sample_jobs()
        self.assertGreaterEqual(len(jobs), 4)
        self.assertTrue(any("iOS" in j["title"] for j in jobs))

    def test_filter_jobs_by_keyword(self):
        jobs = self.radar.get_sample_jobs()
        filtered = self.radar.filter_jobs(jobs, ["swift", "ios"])
        self.assertGreaterEqual(len(filtered), 1)
        for j in filtered:
            text = f"{j['title']} {j['description']}".lower()
            self.assertTrue("swift" in text or "ios" in text)

    def test_evaluate_and_rank_jobs(self):
        jobs = self.radar.get_sample_jobs()
        ranked = self.radar.evaluate_and_rank(jobs, min_score=0.0)
        self.assertEqual(len(ranked), len(jobs))
        # Verify sorted descending by match_score
        scores = [j["match_score"] for j in ranked]
        self.assertEqual(scores, sorted(scores, reverse=True))
        # Top job should have positive match score with Umut's profile
        self.assertGreater(scores[0], 0.0)

    def test_parse_sample_rss_xml(self):
        sample_rss = """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
            <channel>
                <title>Test Jobs</title>
                <item>
                    <title>Senior Swift Engineer</title>
                    <link>https://example.com/job1</link>
                    <description><![CDATA[<p>Looking for a Swift expert.</p>]]></description>
                    <guid>guid-123</guid>
                </item>
            </channel>
        </rss>"""
        import xml.etree.ElementTree as ET
        import re

        root = ET.fromstring(sample_rss)
        items = []
        for elem in root.findall(".//item"):
            title = elem.findtext("title") or ""
            link = elem.findtext("link") or ""
            desc = elem.findtext("description") or ""
            cleaned = re.sub(r'<[^>]+>', ' ', desc).strip()
            items.append({"title": title, "link": link, "desc": cleaned})

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "Senior Swift Engineer")
        self.assertIn("Looking for a Swift expert", items[0]["desc"])

if __name__ == "__main__":
    unittest.main()
