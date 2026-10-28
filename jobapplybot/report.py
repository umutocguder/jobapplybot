# Created by 11Hopem
# Copyright (c) 2026 11hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

from collections import Counter
from typing import Dict, Any, List, Optional
from .tracker import ApplicationTracker

class ApplicationReporter:
    """
    Computes analytics and generates markdown reports on the application pipeline.
    """

    def __init__(self, tracker: Optional[ApplicationTracker] = None):
        self.tracker = tracker or ApplicationTracker()

    def generate_statistics(self) -> Dict[str, Any]:
        apps = self.tracker.list_applications()
        total = len(apps)

        status_counts = {status: 0 for status in ApplicationTracker.VALID_STATUSES}
        scores: List[float] = []

        for app in apps:
            st = app.get("status", "SAVED")
            status_counts[st] = status_counts.get(st, 0) + 1
            if "match_score" in app and isinstance(app["match_score"], (int, float)):
                scores.append(float(app["match_score"]))

        applied_or_further = (
            status_counts.get("APPLIED", 0) +
            status_counts.get("INTERVIEW", 0) +
            status_counts.get("OFFER", 0) +
            status_counts.get("REJECTED", 0)
        )

        interview_count = status_counts.get("INTERVIEW", 0) + status_counts.get("OFFER", 0)
        interview_rate = (interview_count / applied_or_further * 100.0) if applied_or_further > 0 else 0.0
        offer_rate = (status_counts.get("OFFER", 0) / applied_or_further * 100.0) if applied_or_further > 0 else 0.0
        avg_score = (sum(scores) / len(scores)) if scores else 0.0

        return {
            "total_tracked": total,
            "status_breakdown": status_counts,
            "applied_count": applied_or_further,
            "interview_rate_pct": round(interview_rate, 2),
            "offer_rate_pct": round(offer_rate, 2),
            "average_match_score": round(avg_score, 2)
        }

    def generate_markdown_report(self) -> str:
        stats = self.generate_statistics()
        sb = stats["status_breakdown"]

        lines = [
            "# 📊 JobApplyBot Pipeline Report",
            "",
            f"- **Total Tracked Applications:** {stats['total_tracked']}",
            f"- **Average Match Score:** %{stats['average_match_score']}",
            f"- **Interview Rate:** %{stats['interview_rate_pct']}",
            f"- **Offer Rate:** %{stats['offer_rate_pct']}",
            "",
            "### 📈 Status Breakdown",
            "| Status | Count |",
            "|---|---|",
            f"| 💾 Saved | {sb.get('SAVED', 0)} |",
            f"| 🚀 Applied | {sb.get('APPLIED', 0)} |",
            f"| 💬 Interview | {sb.get('INTERVIEW', 0)} |",
            f"| 🏆 Offer | {sb.get('OFFER', 0)} |",
            f"| ❌ Rejected | {sb.get('REJECTED', 0)} |",
            ""
        ]

        recent_apps = self.tracker.list_applications()[-5:]
        if recent_apps:
            lines.append("### 🕒 Recent Activity (Last 5)")
            lines.append("| ID | Company | Position | Score | Status |")
            lines.append("|---|---|---|---|---|")
            for a in reversed(recent_apps):
                lines.append(
                    f"| {a.get('id')} | {a.get('company')} | {a.get('position')} | %{a.get('match_score', 0)} | {a.get('status')} |"
                )
            lines.append("")

        return "\n".join(lines)
