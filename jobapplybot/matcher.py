# Created by 11hopem (11 Hopem Software Ltd. Şti.)
# Copyright (c) 2026 11hopem. All rights reserved.
# Licensed under 11 Hopem Software Proprietary License.

import re
from typing import Dict, List, Set, Any

class ResumeMatcher:
    """
    ATS-style keyword and semantic resume matcher for job descriptions.
    """

    def __init__(self, stop_words: Set[str] = None):
        self.stop_words = stop_words or {
            'the', 'and', 'for', 'with', 'that', 'this', 'from', 'have', 'are',
            'bir', 've', 'ile', 'için', 'olan', 'gibi', 'bu', 'da', 'de'
        }

    def tokenize(self, text: str) -> List[str]:
        """Extracts cleaned lowercased alphanumeric words."""
        cleaned = re.sub(r'[^\w\s]', ' ', text.lower())
        tokens = [w for w in cleaned.split() if len(w) > 2 and w not in self.stop_words]
        return tokens

    def extract_keywords(self, text: str) -> Set[str]:
        return set(self.tokenize(text))

    def calculate_match_score(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """
        Calculates compatibility score between resume and job description.
        Returns match percentage, matched keywords, and missing keywords.
        """
        resume_kw = self.extract_keywords(resume_text)
        job_kw = self.extract_keywords(job_description)

        if not job_kw:
            return {
                "score": 0.0,
                "matched_keywords": [],
                "missing_keywords": [],
                "total_job_keywords": 0
            }

        matched = resume_kw.intersection(job_kw)
        missing = job_kw.difference(resume_kw)
        score = (len(matched) / len(job_kw)) * 100.0

        return {
            "score": round(score, 2),
            "matched_keywords": sorted(list(matched)),
            "missing_keywords": sorted(list(missing)),
            "total_job_keywords": len(job_kw)
        }
