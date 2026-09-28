# Created by 11hopem (11 Hopem Software Ltd. Şti.)
# Copyright (c) 2026 11hopem. All rights reserved.
# Licensed under 11 Hopem Software Proprietary License.

import os
import re
import json
from datetime import datetime
from typing import Dict, Any, Optional

class SecureLogger:
    """
    Dual-tier telemetry logger with KVKK & PII scrubbing and zero-crash guarantee.
    """

    def __init__(self, log_dir: str = "logs", project_id: str = "hopem-software-cloud"):
        self.log_dir = log_dir
        self.project_id = project_id
        self.events = []

    def scrub_sensitive_data(self, text: str) -> str:
        if not isinstance(text, str):
            return str(text)
        # Scrub Turkish Phone numbers
        text = re.sub(r'(?:\+90|0)?5\d{9}', '[PHONE_REDACTED]', text)
        # Scrub Turkish TCKN (11 digits starting with 1-9)
        text = re.sub(r'\b[1-9]\d{10}\b', '[TCKN_REDACTED]', text)
        return text

    def log(self, level: str, tag: str, message: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        sanitized_msg = self.scrub_sensitive_data(message)
        event = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "tag": tag,
            "message": sanitized_msg,
            "metadata": metadata or {},
            "projectId": self.project_id
        }
        self.events.append(event)
        try:
            os.makedirs(self.log_dir, exist_ok=True)
            log_file = os.path.join(self.log_dir, "telemetry.jsonl")
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")
        except Exception:
            pass  # Zero-crash guarantee
        return event

    def info(self, message: str, tag: str = "JobApplyBot", metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self.log("INFO", tag, message, metadata)

    def error(self, message: str, tag: str = "JobApplyBot", metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self.log("ERROR", tag, message, metadata)
