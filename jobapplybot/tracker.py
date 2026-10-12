# Created by 11Hopem
# Copyright (c) 2026 11hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
from .backup import create_autonomous_backup

class ApplicationTracker:
    """
    Manages job application lifecycle with 100% local persistence.
    """

    VALID_STATUSES = ["SAVED", "APPLIED", "INTERVIEW", "OFFER", "REJECTED"]

    def __init__(self, storage_path: Optional[str] = None, backup_dir: Optional[str] = None):
        self.storage_path = storage_path
        self.backup_dir = backup_dir
        self.applications: List[Dict[str, Any]] = []
        if self.storage_path and os.path.exists(self.storage_path):
            self.load()

    def add_application(self, company: str, position: str, match_score: float = 0.0, url: str = "") -> Dict[str, Any]:
        app_id = f"APP-{int(datetime.now().timestamp() * 1000)}"
        app_data = {
            "id": app_id,
            "company": company,
            "position": position,
            "match_score": match_score,
            "url": url,
            "status": "APPLIED",
            "applied_at": datetime.now().isoformat(),
            "notes": ""
        }
        self.applications.append(app_data)
        self.save()
        return app_data

    def update_status(self, app_id: str, new_status: str, notes: str = "") -> bool:
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {new_status}. Must be one of {self.VALID_STATUSES}")
        for app in self.applications:
            if app["id"] == app_id:
                app["status"] = new_status
                if notes:
                    app["notes"] = notes
                self.save()
                return True
        return False

    def list_applications(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        if status:
            return [a for a in self.applications if a["status"] == status]
        return self.applications

    def save(self):
        if self.storage_path:
            os.makedirs(os.path.dirname(os.path.abspath(self.storage_path)), exist_ok=True)
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(self.applications, f, indent=2, ensure_ascii=False)
        try:
            create_autonomous_backup(self.applications, self.backup_dir)
        except Exception:
            pass

    def load(self):
        if self.storage_path and os.path.exists(self.storage_path):
            with open(self.storage_path, "r", encoding="utf-8") as f:
                self.applications = json.load(f)
