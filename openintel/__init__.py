"""
TechStack Detector - A comprehensive tool to detect technology stacks used by websites
"""

__version__ = "1.0.0"
__author__ = "Devanshu Singh"

from openintel.analyzer import TechStackAnalyzer
from openintel.detector import TechStackDetector
from openintel.models import DetectionResult, TechCategory, TechSignature

__all__ = [
    "TechStackDetector",
    "TechStackAnalyzer", 
    "DetectionResult",
    "TechCategory",
    "TechSignature",
]
