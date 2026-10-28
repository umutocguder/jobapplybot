# Created by 11Hopem
# Copyright (c) 2026 11hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

import unittest
from jobapplybot.proposal import ProposalGenerator
from jobapplybot.profile import CandidateProfile

class TestProposalGenerator(unittest.TestCase):

    def setUp(self):
        self.profile = CandidateProfile()
        self.generator = ProposalGenerator(profile=self.profile)

    def test_generate_freelance_proposal_english(self):
        title = "Senior iOS Developer for Banking App"
        desc = "Need a senior Swift developer with experience in iOS, UIKit, fintech, and banking architecture."
        result = self.generator.generate_freelance_proposal(
            job_title=title,
            job_description=desc,
            client_name="Alex",
            language="en"
        )
        self.assertIn("Hi Alex,", result["proposal_text"])
        self.assertIn(self.profile.full_name, result["proposal_text"])
        self.assertGreater(result["match_score"], 0.0)
        self.assertIn("İşCep", result["proposal_text"])

    def test_generate_freelance_proposal_turkish(self):
        title = "Mobil Uygulama Geliştiricisi"
        desc = "Swift ve iOS deneyimi olan, e-ticaret ve fintech projelerinde çalışmış geliştirici aranıyor."
        result = self.generator.generate_freelance_proposal(
            job_title=title,
            job_description=desc,
            client_name=None,
            language="tr"
        )
        self.assertIn("Merhaba,", result["proposal_text"])
        self.assertIn(self.profile.full_name, result["proposal_text"])
        self.assertGreater(result["match_score"], 0.0)

    def test_generate_cover_letter_english(self):
        result = self.generator.generate_cover_letter(
            company="Acme Corp",
            position="Lead iOS Engineer",
            job_description="Swift, SwiftUI, Combine, unit testing, and scalable architecture.",
            language="en"
        )
        self.assertEqual(result["company"], "Acme Corp")
        self.assertIn("Dear Hiring Team at Acme Corp,", result["cover_letter_text"])
        self.assertIn("Lead iOS Engineer", result["cover_letter_text"])
        self.assertIn(self.profile.full_name, result["cover_letter_text"])

    def test_generate_cover_letter_turkish(self):
        result = self.generator.generate_cover_letter(
            company="Büyük Şirket A.Ş.",
            position="Kıdemli iOS Geliştirici",
            job_description="Swift, UIKit, mimari ve test konularında deneyimli.",
            language="tr"
        )
        self.assertIn("Büyük Şirket A.Ş. İnsan Kaynakları", result["cover_letter_text"])
        self.assertIn("Kıdemli iOS Geliştirici", result["cover_letter_text"])

if __name__ == "__main__":
    unittest.main()
