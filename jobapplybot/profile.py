# Created by 11Hopem
# Copyright (c) 2026 11hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

import os
import json
from typing import Dict, List, Any, Optional

DEFAULT_PROFILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "profile.json"
)

class CandidateProfile:
    """
    Candidate profile and portfolio manager for ATS resume matching and proposals.
    """

    def __init__(self, data: Optional[Dict[str, Any]] = None):
        self.data: Dict[str, Any] = data or self.get_default_profile_data()

    @property
    def full_name(self) -> str:
        return self.data.get("full_name", "")

    @property
    def headline(self) -> str:
        return self.data.get("headline", "")

    @property
    def email(self) -> str:
        return self.data.get("email", "")

    @property
    def phone(self) -> str:
        return self.data.get("phone", "")

    @property
    def location(self) -> str:
        return self.data.get("location", "")

    @property
    def summary(self) -> str:
        return self.data.get("summary", "")

    @property
    def resume_url(self) -> str:
        return self.data.get("resume_url", "")

    @property
    def github_url(self) -> str:
        return self.data.get("github_url", "")

    @property
    def linkedin_url(self) -> str:
        return self.data.get("linkedin_url", "")

    @property
    def skills(self) -> Dict[str, List[str]]:
        return self.data.get("skills", {})

    @property
    def experiences(self) -> List[Dict[str, Any]]:
        return self.data.get("experiences", [])

    @property
    def projects(self) -> List[Dict[str, Any]]:
        return self.data.get("projects", [])

    def all_skills_list(self) -> List[str]:
        all_skills: List[str] = []
        for cat_skills in self.skills.values():
            if isinstance(cat_skills, list):
                all_skills.extend(cat_skills)
        return sorted(list(set(all_skills)))

    def to_resume_text(self) -> str:
        """
        Builds a dense textual resume representation for ATS keyword matching.
        """
        parts = [
            f"{self.full_name} - {self.headline}",
            f"Location: {self.location} | Email: {self.email} | Phone: {self.phone}",
            f"Summary: {self.summary}",
            "Technical Skills: " + ", ".join(self.all_skills_list())
        ]

        parts.append("Work Experience:")
        for exp in self.experiences:
            company = exp.get("company", "")
            role = exp.get("role", "")
            summary = exp.get("summary", "")
            highlights = " ".join(exp.get("highlights", []))
            parts.append(f"{role} at {company}. {summary} {highlights}")

        parts.append("Key Projects & Portfolio:")
        for proj in self.projects:
            name = proj.get("name", "")
            desc = proj.get("description", "")
            tech = ", ".join(proj.get("technologies", []))
            parts.append(f"Project: {name}. Description: {desc}. Tech stack: {tech}")

        return "\n\n".join(parts)

    def find_relevant_projects(self, keywords: List[str], limit: int = 3) -> List[Dict[str, Any]]:
        """
        Finds candidate projects best matching a list of target keywords.
        """
        normalized_kw = {k.lower() for k in keywords}
        scored_projects = []

        for proj in self.projects:
            score = 0
            searchable = (
                proj.get("name", "") + " " +
                proj.get("description", "") + " " +
                " ".join(proj.get("technologies", []))
            ).lower()

            for kw in normalized_kw:
                if kw in searchable:
                    score += 1

            scored_projects.append((score, proj))

        scored_projects.sort(key=lambda x: x[0], reverse=True)
        return [p[1] for p in scored_projects[:limit]]

    def save(self, filepath: Optional[str] = None):
        target = filepath or DEFAULT_PROFILE_PATH
        os.makedirs(os.path.dirname(os.path.abspath(target)), exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, filepath: Optional[str] = None) -> "CandidateProfile":
        target = filepath or DEFAULT_PROFILE_PATH
        if os.path.exists(target):
            with open(target, "r", encoding="utf-8") as f:
                data = json.load(f)
            return cls(data)
        profile = cls()
        profile.save(target)
        return profile

    @staticmethod
    def get_default_profile_data() -> Dict[str, Any]:
        return {
            "full_name": "Umut Öçgüder",
            "headline": "Senior iOS & Mobile Developer | Full-Stack Engineer",
            "email": "umutocgdr@gmail.com",
            "phone": "+90 507 490 26 05",
            "location": "Ankara, Türkiye (Remote / Worldwide)",
            "summary": (
                "Senior Mobile Developer with 4+ years of professional engineering experience "
                "delivering top-tier iOS (Swift, SwiftUI, UIKit, Combine) and Full-Stack systems. "
                "Shipped enterprise applications reaching millions of active users, including İşCep (banking), "
                "HomeWhiz (IoT, MQTT protocol) and DOA (nationwide government fintech & KYC). "
                "Experienced in creating robust web platforms, automated bots, and AI solutions with Next.js and Python."
            ),
            "resume_url": "https://github.com/umutocguder/Resume/raw/main/Click%20For%20Resume.pdf",
            "github_url": "https://github.com/umutocguder",
            "linkedin_url": "https://www.linkedin.com/in/umutocguder",
            "skills": {
                "mobile": [
                    "Swift", "SwiftUI", "UIKit", "Combine", "Objective-C", "CocoaPods", "SPM",
                    "CoreData", "Combine", "Jetpack Compose", "Kotlin", "React Native", "Expo"
                ],
                "web_backend": [
                    "TypeScript", "JavaScript", "React", "Next.js", "Python", "Node.js",
                    "Supabase", "PostgreSQL", "Firebase", "RESTful API", "GraphQL", "WebSockets"
                ],
                "architecture_tools": [
                    "MVVM", "Clean Architecture", "VIPER", "Modular Design", "CI/CD",
                    "GitHub Actions", "Docker", "Git", "MQTT", "NFC", "KYC", "Agile", "Scrum"
                ]
            },
            "experiences": [
                {
                    "company": "Intetra",
                    "role": "iOS Developer & Technical Partner",
                    "period": "2026 - Present",
                    "summary": "Engineering intelligent transportation systems and real-time mobile platforms.",
                    "highlights": [
                        "Architected scalable mobile infrastructure for smart transportation and field operations.",
                        "Streamlined background data synchronization and telemetry pipelines."
                    ]
                },
                {
                    "company": "DIAS Technology",
                    "role": "iOS Developer",
                    "period": "2024 - 2025",
                    "summary": "Core engineer on DOA, Turkey's largest nationwide public recycling and fintech initiative.",
                    "highlights": [
                        "Delivered KYC verification, NFC hardware integrations, and complex Compositional Layouts.",
                        "Integrated secure transaction and reward payout modules for millions of end users."
                    ]
                },
                {
                    "company": "Arçelik via OBSS",
                    "role": "iOS Developer",
                    "period": "2023 - 2024",
                    "summary": "Core engineer on HomeWhiz, an enterprise IoT connectivity platform.",
                    "highlights": [
                        "Built low-latency smart device communication using the MQTT protocol.",
                        "Led team migration to Agile methodologies and elevated Swift code quality."
                    ]
                },
                {
                    "company": "Softtech (İşbank Ecosystem)",
                    "role": "iOS Developer",
                    "period": "2021 - 2023",
                    "summary": "Developed mobile banking, factoring, and financial investment applications.",
                    "highlights": [
                        "Engineered core modules for İşCep (2M+ user reviews, 4.6 star rating).",
                        "Built localized banking apps for İşbank Iraq, Georgia, London, and Kosovo branches.",
                        "Integrated QR check scanning, NFC onboarding, and video banking protocols."
                    ]
                }
            ],
            "projects": [
                {
                    "name": "İşCep & Digital Banking",
                    "description": "High-throughput mobile banking application serving millions of daily active users.",
                    "technologies": ["Swift", "UIKit", "Security", "Fintech", "NFC", "REST API"]
                },
                {
                    "name": "HomeWhiz IoT Platform",
                    "description": "Smart home appliance ecosystem with real-time hardware telemetry and control.",
                    "technologies": ["Swift", "MQTT", "IoT", "Combine", "Bluetooth", "Networking"]
                },
                {
                    "name": "Misbetyy Boutique & Studio Platform",
                    "description": "Full-stack boutique e-commerce showcase, brand studio, and social media scheduler.",
                    "technologies": ["Next.js", "React", "TypeScript", "Supabase", "TailwindCSS"]
                },
                {
                    "name": "Sigorta Takip & WhatsApp CRM",
                    "description": "Insurance policy expiration tracker with automated client communication and WhatsApp CRM.",
                    "technologies": ["Next.js", "TypeScript", "PWA", "Supabase", "Automation"]
                },
                {
                    "name": "Zootech Eleman Takip",
                    "description": "B2B enterprise field sales management and GPS tracking mobile app for veterinary medicine.",
                    "technologies": ["SwiftUI", "Supabase", "CoreLocation", "Background Tasks"]
                }
            ]
        }
