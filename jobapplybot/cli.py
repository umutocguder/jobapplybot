# Created by 11Hopem
# Copyright (c) 2026 11hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

import sys
import argparse
from typing import Optional, List
from .profile import CandidateProfile
from .matcher import ResumeMatcher
from .proposal import ProposalGenerator
from .radar import JobRadar
from .tracker import ApplicationTracker
from .report import ApplicationReporter
from .logger import SecureLogger

logger = SecureLogger()

def run_scan(args: argparse.Namespace) -> int:
    profile = CandidateProfile.load()
    radar = JobRadar(profile=profile)

    keywords = args.keywords.split(",") if args.keywords else None
    print(f"\n🔍 Scanning job feeds (Filter: {args.keywords or 'All'})...")

    jobs = []
    if args.online:
        print("🌐 Connecting to live remote feeds...")
        jobs = radar.scan_online_feeds()

    if not jobs:
        print("📋 Using verified curated and sample job postings...")
        jobs = radar.get_sample_jobs()

    if keywords:
        jobs = radar.filter_jobs(jobs, keywords)

    ranked = radar.evaluate_and_rank(jobs, min_score=float(args.min_score))

    print(f"\n🎯 Found {len(ranked)} matching opportunities:\n")
    print(f"{'#':<3} | {'SCORE':<7} | {'COMPANY':<22} | {'TITLE':<35} | {'LOCATION'}")
    print("-" * 90)

    for idx, j in enumerate(ranked[:args.limit], 1):
        score_str = f"%{j.get('match_score', 0):.1f}"
        print(f"{idx:<3} | {score_str:<7} | {j.get('company', '')[:20]:<22} | {j.get('title', '')[:33]:<35} | {j.get('location', '')[:20]}")

    print("\n💡 Tip: Use 'propose' or 'apply' with company and title to take action.")
    return 0

def run_match(args: argparse.Namespace) -> int:
    profile = CandidateProfile.load()
    matcher = ResumeMatcher()
    resume_text = profile.to_resume_text()

    job_text = args.text
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            job_text = f.read()

    if not job_text:
        print("❌ Error: Please provide job text with --text or a file path with --file.")
        return 1

    analysis = matcher.calculate_match_score(resume_text, job_text)
    print("\n🎯 ATS Resume Match Analysis:")
    print(f"Overall Compatibility Score: %{analysis['score']:.1f}")
    print(f"Total Job Keywords Found: {analysis['total_job_keywords']}")
    print(f"\n✅ Matched Keywords ({len(analysis['matched_keywords'])}):")
    print(", ".join(analysis['matched_keywords']) if analysis['matched_keywords'] else "None")
    print(f"\n⚠️ Missing Keywords ({len(analysis['missing_keywords'])}):")
    print(", ".join(analysis['missing_keywords'][:15]) if analysis['missing_keywords'] else "None")
    return 0

def run_propose(args: argparse.Namespace) -> int:
    generator = ProposalGenerator()
    desc = args.desc or f"Looking for an experienced engineer in {args.title}."

    if args.type == "freelance":
        result = generator.generate_freelance_proposal(
            job_title=args.title,
            job_description=desc,
            client_name=args.client,
            language=args.lang
        )
        print(f"\n🚀 Tailored Freelance Proposal (Match Score: %{result['match_score']:.1f}):\n")
        print(result["proposal_text"])
    else:
        result = generator.generate_cover_letter(
            company=args.company or "Hiring Team",
            position=args.title,
            job_description=desc,
            language=args.lang
        )
        print(f"\n💼 Corporate Cover Letter (Match Score: %{result['match_score']:.1f}):\n")
        print(result["cover_letter_text"])

    return 0

def run_apply(args: argparse.Namespace) -> int:
    tracker = ApplicationTracker(storage_path=args.storage)
    app = tracker.add_application(
        company=args.company,
        position=args.position,
        match_score=float(args.score),
        url=args.url or ""
    )
    print(f"\n✅ Application recorded successfully!")
    print(f"ID: {app['id']} | Company: {app['company']} | Position: {app['position']} | Status: {app['status']}")
    print("🔒 Autonomous backup automatically triggered and verified.")
    return 0

def run_status(args: argparse.Namespace) -> int:
    reporter = ApplicationReporter(ApplicationTracker(storage_path=args.storage))
    print("\n" + reporter.generate_markdown_report())
    return 0

def run_profile(args: argparse.Namespace) -> int:
    profile = CandidateProfile.load()
    print(f"\n👤 Candidate Profile: {profile.full_name}")
    print(f"🎯 Headline: {profile.headline}")
    print(f"🏢 Company: {profile.company} | 🌐 {profile.website_url}")
    print(f"📍 Location: {profile.location} | ✉️ {profile.email} | 📞 {profile.phone}")
    print(f"🔗 Links: GitHub: {profile.github_url} | LinkedIn: {profile.linkedin_url}")
    
    if profile.education:
        edu = profile.education[0]
        print(f"🎓 Education: {edu.get('degree')} in {edu.get('field')} - {edu.get('school')} (GPA: {edu.get('gpa')})")

    print(f"\n🛠️ Technical Skills ({len(profile.all_skills_list())} total):")
    for category, skills in profile.skills.items():
        cat_title = category.replace("_", " ").title()
        print(f"  • {cat_title}: {', '.join(skills)}")

    print(f"\n💼 Enterprise Work Experience ({len(profile.experiences)} roles):")
    for exp in profile.experiences:
        print(f"  • {exp.get('role')} @ {exp.get('company')} ({exp.get('period')})")
        if exp.get('summary'):
            print(f"    - {exp.get('summary')}")

    print(f"\n🌟 Live Production Projects & Showcases ({len(profile.projects)} platforms):")
    for proj in profile.projects:
        url_info = f" -> {proj.get('url')}" if proj.get('url') else ""
        metrics_info = f" ({proj.get('metrics')})" if proj.get('metrics') else ""
        print(f"  • {proj.get('name')} [{proj.get('category')}]{url_info}")
        if metrics_info:
            print(f"    Metrics:{metrics_info}")

    return 0

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jobapplybot",
        description="JobApplyBot: Autonomous Job Application, ATS Matcher & Freelance Proposal Engine."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # scan
    p_scan = subparsers.add_parser("scan", help="Scan and rank job opportunities")
    p_scan.add_argument("--keywords", "-k", type=str, default="", help="Comma-separated keywords (e.g. ios,swift,react)")
    p_scan.add_argument("--min-score", "-m", type=float, default=0.0, help="Minimum ATS score threshold")
    p_scan.add_argument("--limit", "-l", type=int, default=10, help="Max results to display")
    p_scan.add_argument("--online", action="store_true", help="Connect to live online remote feeds")

    # match
    p_match = subparsers.add_parser("match", help="Evaluate ATS match score for a job description")
    p_match.add_argument("--text", "-t", type=str, default="", help="Raw job description text")
    p_match.add_argument("--file", "-f", type=str, default="", help="Path to text file containing job description")

    # propose
    p_prop = subparsers.add_parser("propose", help="Generate targeted proposal or cover letter")
    p_prop.add_argument("--title", "-t", required=True, help="Job title / role")
    p_prop.add_argument("--desc", "-d", type=str, default="", help="Job description text")
    p_prop.add_argument("--company", "-c", type=str, default="Client", help="Company or client name")
    p_prop.add_argument("--client", type=str, default="", help="Client personal name")
    p_prop.add_argument("--type", choices=["freelance", "corporate"], default="freelance", help="Proposal type")
    p_prop.add_argument("--lang", choices=["en", "tr"], default="en", help="Language (en or tr)")

    # apply
    p_apply = subparsers.add_parser("apply", help="Track a new job application")
    p_apply.add_argument("--company", "-c", required=True, help="Company name")
    p_apply.add_argument("--position", "-p", required=True, help="Position title")
    p_apply.add_argument("--score", "-s", type=float, default=0.0, help="ATS match score")
    p_apply.add_argument("--url", "-u", type=str, default="", help="Job listing URL")
    p_apply.add_argument("--storage", type=str, default=None, help="Custom storage path")

    # status
    p_stat = subparsers.add_parser("status", help="Show application pipeline status and statistics")
    p_stat.add_argument("--storage", type=str, default=None, help="Custom storage path")

    # profile
    subparsers.add_parser("profile", help="Display candidate profile and skills")

    return parser

def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args_list = sys.argv[1:] if argv is None else argv
    args = parser.parse_args(args_list)

    if not args.command:
        parser.print_help()
        return 0

    commands = {
        "scan": run_scan,
        "match": run_match,
        "propose": run_propose,
        "apply": run_apply,
        "status": run_status,
        "profile": run_profile
    }

    handler = commands.get(args.command)
    if handler:
        return handler(args)
    parser.print_help()
    return 0

if __name__ == "__main__":
    sys.exit(main())
