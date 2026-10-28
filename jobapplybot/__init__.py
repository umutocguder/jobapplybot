# Created by 11Hopem
# Copyright (c) 2026 11hopem. All rights reserved.
# Licensed under 11Hopem Proprietary License.

"""
JobApplyBot: Autonomous Job Application, ATS Resume Matcher, and Proposal Engine.
"""

from .matcher import ResumeMatcher
from .tracker import ApplicationTracker
from .backup import create_autonomous_backup, verify_backup_integrity, restore_from_backup
from .logger import SecureLogger
from .profile import CandidateProfile
from .proposal import ProposalGenerator
from .radar import JobRadar
from .report import ApplicationReporter

__version__ = "1.1.0"
__author__ = "11hopem <umutocgdr@gmail.com>"

__all__ = [
    "ResumeMatcher",
    "ApplicationTracker",
    "create_autonomous_backup",
    "verify_backup_integrity",
    "restore_from_backup",
    "SecureLogger",
    "CandidateProfile",
    "ProposalGenerator",
    "JobRadar",
    "ApplicationReporter"
]
