# Created by 11Hopem
# Copyright (c) 2026 11hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jobapplybot.tracker import ApplicationTracker
from jobapplybot.backup import create_autonomous_backup, verify_backup_integrity

def main():
    tracker = ApplicationTracker()
    metadata = create_autonomous_backup(tracker.applications)
    if not verify_backup_integrity():
        print("[Backup Error]: JobApplyBot backup integrity check failed!", file=sys.stderr)
        sys.exit(1)

    print(f"[Backup Success]: JobApplyBot backup generated successfully.")
    print(f"  File: {metadata['latest_backup_file']}")
    print(f"  SHA-256: {metadata['sha256']}")
    print(f"  Applications: {metadata['applications_count']}")
    print(f"  Size: {metadata['file_size']} bytes")

if __name__ == "__main__":
    main()
