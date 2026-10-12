# Created by 11Hopem
# Copyright (c) 2026 11hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional, List

DEFAULT_BACKUP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "backups")

def create_autonomous_backup(applications: List[Dict[str, Any]], backup_dir: Optional[str] = None) -> Dict[str, Any]:
    target_dir = backup_dir or DEFAULT_BACKUP_DIR
    os.makedirs(target_dir, exist_ok=True)

    timestamp_iso = datetime.now().isoformat()
    clean_timestamp = timestamp_iso.replace(":", "-").replace(".", "-")

    payload = {
        "version": "1.0.0",
        "app": "JobApplyBot",
        "timestamp": timestamp_iso,
        "applications_count": len(applications),
        "applications": applications
    }

    raw_json = json.dumps(payload, indent=2, ensure_ascii=False)
    sha256 = hashlib.sha256(raw_json.encode("utf-8")).hexdigest()

    timestamped_file = os.path.join(target_dir, f"jobapply_backup_{clean_timestamp}.json")
    latest_file = os.path.join(target_dir, "jobapply_latest_backup.json")
    checksum_file = os.path.join(target_dir, "jobapply_checksums.json")

    with open(timestamped_file, "w", encoding="utf-8") as f:
        f.write(raw_json)

    with open(latest_file, "w", encoding="utf-8") as f:
        f.write(raw_json)

    metadata = {
        "timestamp": timestamp_iso,
        "applications_count": len(applications),
        "sha256": sha256,
        "file_size": len(raw_json.encode("utf-8")),
        "backup_file": os.path.basename(timestamped_file),
        "latest_backup_file": os.path.basename(latest_file)
    }

    checksum_log = []
    if os.path.exists(checksum_file):
        try:
            with open(checksum_file, "r", encoding="utf-8") as f:
                checksum_log = json.load(f)
                if not isinstance(checksum_log, list):
                    checksum_log = []
        except Exception:
            checksum_log = []

    checksum_log.insert(0, metadata)
    if len(checksum_log) > 30:
        checksum_log = checksum_log[:30]

    with open(checksum_file, "w", encoding="utf-8") as f:
        json.dump(checksum_log, f, indent=2, ensure_ascii=False)

    return metadata

def verify_backup_integrity(backup_dir: Optional[str] = None) -> bool:
    target_dir = backup_dir or DEFAULT_BACKUP_DIR
    latest_file = os.path.join(target_dir, "jobapply_latest_backup.json")

    if not os.path.exists(latest_file):
        return False

    try:
        with open(latest_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        return (
            data.get("app") == "JobApplyBot" and
            isinstance(data.get("applications"), list) and
            "timestamp" in data
        )
    except Exception:
        return False

def restore_from_backup(backup_dir: Optional[str] = None) -> Dict[str, Any]:
    target_dir = backup_dir or DEFAULT_BACKUP_DIR
    latest_file = os.path.join(target_dir, "jobapply_latest_backup.json")

    if not os.path.exists(latest_file):
        raise FileNotFoundError(f"Latest backup file not found at {latest_file}")

    with open(latest_file, "r", encoding="utf-8") as f:
        return json.load(f)
