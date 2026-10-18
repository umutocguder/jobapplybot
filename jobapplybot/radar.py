# Created by 11Hopem
# Copyright (c) 2026 11hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

import re
import json
import urllib.request
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
from .profile import CandidateProfile
from .matcher import ResumeMatcher

DEFAULT_REMOTE_FEEDS = [
    {
        "name": "WeWorkRemotely (Programming)",
        "type": "rss",
        "url": "https://weworkremotely.com/categories/remote-programming-jobs.rss"
    },
    {
        "name": "RemoteOK (API)",
        "type": "json",
        "url": "https://remoteok.com/api"
    }
]

SAMPLE_JOBS_FIXTURE: List[Dict[str, Any]] = [
    {
        "id": "job-sample-1",
        "title": "Senior iOS Engineer (Swift / SwiftUI)",
        "company": "Fintech Global Inc",
        "url": "https://example.com/jobs/senior-ios-engineer",
        "location": "Remote (Worldwide)",
        "description": (
            "Looking for an experienced Senior iOS Engineer to build next-generation fintech applications. "
            "Must have strong proficiency in Swift, SwiftUI, Combine, and UIKit. Experience with banking, "
            "fintech, NFC, and clean architecture (MVVM) is highly desirable."
        ),
        "source": "Curated Direct"
    },
    {
        "id": "job-sample-2",
        "title": "Mobile Developer (iOS / Flutter / Kotlin)",
        "company": "IoT Smart Solutions",
        "url": "https://example.com/jobs/mobile-dev-iot",
        "location": "Remote (Europe / Remote)",
        "description": (
            "Seeking a Mobile Developer to connect smart home appliances. Requires Swift or Kotlin experience, "
            "MQTT protocol, Bluetooth connectivity, background sync, and RESTful APIs."
        ),
        "source": "Curated Direct"
    },
    {
        "id": "job-sample-3",
        "title": "Full-Stack React & Next.js Developer",
        "company": "SaaS Studio Labs",
        "url": "https://example.com/jobs/full-stack-nextjs",
        "location": "Remote",
        "description": (
            "We need a full-stack engineer experienced in TypeScript, React, Next.js, and Supabase. "
            "Experience building e-commerce vitrines, CRM tools, or SaaS dashboards is a major plus."
        ),
        "source": "Curated Direct"
    },
    {
        "id": "job-sample-4",
        "title": "Junior Python Automation Script Writer",
        "company": "Data Scraping Corp",
        "url": "https://example.com/jobs/python-automation",
        "location": "Remote",
        "description": (
            "Looking for a Python developer to write automated scrapers, data pipelines, and CLI tools. "
            "Knowledge of standard library, regex, and json is required."
        ),
        "source": "Curated Direct"
    }
]

class JobRadar:
    """
    Scans, filters, and ranks real-world and curated job feeds for the candidate.
    """

    def __init__(self, profile: Optional[CandidateProfile] = None):
        self.profile = profile or CandidateProfile.load()
        self.matcher = ResumeMatcher()

    def fetch_rss_feed(self, url: str, timeout: int = 5) -> List[Dict[str, Any]]:
        """Parses an RSS 2.0 XML job feed."""
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; JobApplyBot/1.0; +https://github.com/umutocguder)'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)
        items = []
        for elem in root.findall(".//item"):
            title = elem.findtext("title") or ""
            link = elem.findtext("link") or ""
            description = elem.findtext("description") or ""
            guid = elem.findtext("guid") or link

            cleaned_desc = re.sub(r'<[^>]+>', ' ', description)
            items.append({
                "id": guid,
                "title": title,
                "company": "Feed Posting",
                "url": link,
                "location": "Remote",
                "description": cleaned_desc.strip(),
                "source": "RSS Feed"
            })
        return items

    def fetch_json_feed(self, url: str, timeout: int = 5) -> List[Dict[str, Any]]:
        """Parses a JSON job feed (such as RemoteOK)."""
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; JobApplyBot/1.0; +https://github.com/umutocguder)'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read().decode('utf-8')

        data = json.loads(raw)
        items = []
        if isinstance(data, list):
            for entry in data:
                if not isinstance(entry, dict) or not entry.get("position"):
                    continue
                items.append({
                    "id": str(entry.get("id", "")),
                    "title": entry.get("position", ""),
                    "company": entry.get("company", ""),
                    "url": entry.get("url", ""),
                    "location": entry.get("location", "Remote"),
                    "description": entry.get("description", ""),
                    "source": "RemoteOK"
                })
        return items

    def scan_online_feeds(self, feeds: Optional[List[Dict[str, str]]] = None, timeout: int = 5) -> List[Dict[str, Any]]:
        """Fetches from online feeds with graceful fallback on network timeout."""
        target_feeds = feeds or DEFAULT_REMOTE_FEEDS
        collected: List[Dict[str, Any]] = []

        for f in target_feeds:
            feed_type = f.get("type", "")
            feed_url = f.get("url", "")
            try:
                if feed_type == "rss":
                    collected.extend(self.fetch_rss_feed(feed_url, timeout=timeout))
                elif feed_type == "json":
                    collected.extend(self.fetch_json_feed(feed_url, timeout=timeout))
            except Exception:
                pass

        return collected

    def get_sample_jobs(self) -> List[Dict[str, Any]]:
        return list(SAMPLE_JOBS_FIXTURE)

    def filter_jobs(self, jobs: List[Dict[str, Any]], keywords: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        if not keywords:
            return jobs
        filtered = []
        normalized_kw = [k.lower() for k in keywords]
        for job in jobs:
            text = f"{job.get('title', '')} {job.get('description', '')}".lower()
            if any(k in text for k in normalized_kw):
                filtered.append(job)
        return filtered

    def evaluate_and_rank(
        self,
        jobs: List[Dict[str, Any]],
        min_score: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Ranks jobs by ATS keyword compatibility score with candidate's profile.
        """
        resume_text = self.profile.to_resume_text()
        ranked = []

        for job in jobs:
            title = job.get("title", "")
            desc = job.get("description", "")
            full_job_text = f"{title} {desc}"

            analysis = self.matcher.calculate_match_score(resume_text, full_job_text)
            score = analysis.get("score", 0.0)

            if score >= min_score:
                job_copy = dict(job)
                job_copy["match_score"] = score
                job_copy["matched_keywords"] = analysis.get("matched_keywords", [])
                job_copy["missing_keywords"] = analysis.get("missing_keywords", [])
                ranked.append(job_copy)

        ranked.sort(key=lambda x: x.get("match_score", 0.0), reverse=True)
        return ranked
