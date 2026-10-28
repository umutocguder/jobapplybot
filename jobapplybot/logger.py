# Created by 11Hopem
# Copyright (c) 2026 11Hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

import os
import re
import json
import datetime
import urllib.request
import urllib.error
from typing import Dict, Any, Optional
from .firebase_config import FIREBASE_ECOSYSTEM_CONFIG

SENSITIVE_KEY_PATTERNS = [
    re.compile(r"pass(word)?", re.IGNORECASE),
    re.compile(r"token", re.IGNORECASE),
    re.compile(r"secret", re.IGNORECASE),
    re.compile(r"auth(orization)?", re.IGNORECASE),
    re.compile(r"api[_-]?key", re.IGNORECASE),
    re.compile(r"card[_-]?number", re.IGNORECASE),
    re.compile(r"credit[_-]?card", re.IGNORECASE),
    re.compile(r"cvv", re.IGNORECASE),
    re.compile(r"pin", re.IGNORECASE),
    re.compile(r"tckn", re.IGNORECASE)
]

TCKN_REGEX = re.compile(r"\b[1-9]\d{10}\b")
PHONE_REGEX = re.compile(r"(?:\+90|0)?5\d{9}")
CREDIT_CARD_REGEX = re.compile(r"\b(?:\d{4}[ -]?){3}\d{4}\b")
BEARER_REGEX = re.compile(r"Bearer\s+[A-Za-z0-9\-._~+/]+=*", re.IGNORECASE)

def scrub_sensitive_data(value: Any) -> Any:
    """Recursively scrub PII, cards, tokens, phones, and passwords."""
    if value is None:
        return None

    if isinstance(value, str):
        cleaned = BEARER_REGEX.sub("Bearer ***REDACTED***", value)
        cleaned = CREDIT_CARD_REGEX.sub("***CARD_REDACTED***", cleaned)
        cleaned = TCKN_REGEX.sub("[TCKN_REDACTED]", cleaned)
        cleaned = PHONE_REGEX.sub("[PHONE_REDACTED]", cleaned)
        return cleaned

    if isinstance(value, list):
        return [scrub_sensitive_data(item) for item in value]

    if isinstance(value, dict):
        scrubbed = {}
        for k, v in value.items():
            key_str = str(k)
            if any(p.search(key_str) for p in SENSITIVE_KEY_PATTERNS):
                scrubbed[key_str] = "***REDACTED***"
            else:
                scrubbed[key_str] = scrub_sensitive_data(v)
        return scrubbed

    return value

def to_firestore_fields(obj: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a dictionary to Cloud Firestore typed REST fields."""
    fields = {}
    if not isinstance(obj, dict):
        return fields

    for key, val in obj.items():
        if val is None:
            fields[key] = {"nullValue": None}
        elif isinstance(val, bool):
            fields[key] = {"booleanValue": val}
        elif isinstance(val, int):
            fields[key] = {"integerValue": str(val)}
        elif isinstance(val, float):
            fields[key] = {"doubleValue": val}
        elif isinstance(val, str):
            fields[key] = {"stringValue": val[:1000]}
        elif isinstance(val, (dict, list)):
            try:
                fields[key] = {"stringValue": json.dumps(val, ensure_ascii=False)[:1000]}
            except Exception:
                fields[key] = {"stringValue": "[Unserializable]"}
        else:
            fields[key] = {"stringValue": str(val)[:1000]}
    return fields

class SecureLogger:
    """
    Dual-tier telemetry logger with KVKK & PII scrubbing, Cloud Firestore REST streaming,
    and zero-crash guarantee.
    """
    def __init__(self, log_dir: str = "logs", project_id: Optional[str] = None):
        self.log_dir = log_dir
        self.project_id = project_id or FIREBASE_ECOSYSTEM_CONFIG["project_id"]
        self.app_name = "jobapplybot"
        self.app_version = "1.0.0"
        self.api_key = FIREBASE_ECOSYSTEM_CONFIG.get("api_key")
        self.firestore_base_url = FIREBASE_ECOSYSTEM_CONFIG.get("firestore_base_url")
        self.events = []
        self.offline_queue = []
        self.max_offline_queue = 50

    def scrub_sensitive_data(self, text: Any) -> Any:
        return scrub_sensitive_data(text)

    def log(
        self,
        level: str,
        tag: str,
        message: Any,
        metadata: Optional[Dict[str, Any]] = None,
        target_collection: str = "app_logs"
    ) -> Dict[str, Any]:
        try:
            sanitized_msg = scrub_sensitive_data(str(message) if message is not None else "")
            sanitized_meta = scrub_sensitive_data(metadata or {})

            event = {
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "level": str(level).upper() if level else "INFO",
                "tag": tag or "JobApplyBot",
                "appName": self.app_name,
                "appVersion": self.app_version,
                "target_collection": target_collection,
                "message": sanitized_msg,
                "metadata": sanitized_meta,
                "projectId": self.project_id
            }

            self.events.append(event)
            if len(self.events) > 100:
                self.events.pop(0)

            # Local Data Custody
            try:
                os.makedirs(self.log_dir, exist_ok=True)
                log_file = os.path.join(self.log_dir, "telemetry.jsonl")
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(event, ensure_ascii=False) + "\n")
            except Exception:
                pass

            # Cloud Firestore Dispatch
            self._dispatch_to_cloud(event, target_collection)

            return event
        except Exception:
            # Fallback zero-crash object
            return {
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "level": str(level or "INFO").upper(),
                "tag": tag or "JobApplyBot",
                "message": str(message or ""),
                "metadata": metadata or {},
                "projectId": self.project_id
            }

    def info(self, message: str, tag: str = "JobApplyBot", metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self.log("INFO", tag, message, metadata, "app_logs")

    def warn(self, message: str, tag: str = "JobApplyBot", metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self.log("WARN", tag, message, metadata, "app_logs")

    def error(self, message: str, tag: str = "JobApplyBot", metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self.log("ERROR", tag, message, metadata, "app_logs")

    def crash(self, message: str, tag: str = "JobApplyBot", metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self.log("CRASH", tag, message, metadata, "crash_logs")

    def security(self, message: str, tag: str = "JobApplyBot", metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self.log("SECURITY", tag, message, metadata, "security_audit_logs")

    def telemetry(self, message: str, tag: str = "JobApplyBot", metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self.log("TELEMETRY", tag, message, metadata, "telemetry_logs")

    def visitor(self, message: str, tag: str = "JobApplyBot", metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self.log("VISITOR", tag, message, metadata, "visitor_logs")

    def performance(self, metric: str, duration_ms: float, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        meta = {"metric": metric, "duration_ms": duration_ms}
        if metadata:
            meta.update(metadata)
        return self.log("PERF", "Performance", f"Metric: {metric} - {duration_ms}ms", meta, "telemetry_logs")

    def _dispatch_to_cloud(self, entry: Dict[str, Any], collection: str = "app_logs") -> None:
        if not self.api_key or not self.firestore_base_url:
            return

        firestore_url = f"{self.firestore_base_url}/{collection}?key={self.api_key}"
        payload = {
            "fields": to_firestore_fields({
                "event": f"{collection.upper()}_{entry['level']}",
                "timestamp": entry["timestamp"],
                "projectId": entry["projectId"],
                "appId": FIREBASE_ECOSYSTEM_CONFIG.get("app_id", ""),
                "appName": entry["appName"],
                "appVersion": entry["appVersion"],
                "logLevel": entry["level"],
                "tag": entry["tag"],
                "message": entry["message"],
                "metadata": entry["metadata"]
            })
        }

        try:
            req = urllib.request.Request(
                firestore_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=1.5):
                pass
        except Exception:
            self._enqueue_offline({"url": firestore_url, "payload": payload})

    def _enqueue_offline(self, item: Dict[str, Any]) -> None:
        try:
            self.offline_queue.append(item)
            if len(self.offline_queue) > self.max_offline_queue:
                self.offline_queue.pop(0)
        except Exception:
            pass

    def flush_offline_queue(self) -> None:
        if not self.offline_queue:
            return
        items = list(self.offline_queue)
        self.offline_queue = []
        for item in items:
            try:
                req = urllib.request.Request(
                    item["url"],
                    data=json.dumps(item["payload"]).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=1.5):
                    pass
            except Exception:
                self._enqueue_offline(item)

logger = SecureLogger()
