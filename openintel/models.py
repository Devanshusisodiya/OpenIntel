import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class TechCategory(Enum):
    """Categories of technologies that can be detected"""
    FRONTEND_FRAMEWORK = "frontend_framework"
    BACKEND_FRAMEWORK = "backend_framework"
    JAVASCRIPT_LIBRARY = "javascript_library"
    CSS_FRAMEWORK = "css_framework"
    ANALYTICS = "analytics"
    ADVERTISING = "advertising"
    CDN = "cdn"
    HOSTING = "hosting"
    DATABASE = "database"
    CMS = "cms"
    ECOMMERCE = "ecommerce"
    SECURITY = "security"
    PERFORMANCE = "performance"
    MARKETING = "marketing"
    SOCIAL = "social"
    PAYMENT = "payment"
    OTHER = "other"

@dataclass
class TechSignature:
    """Represents a technology signature for detection"""
    name: str
    category: TechCategory
    patterns: Dict[str, List[str]] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    meta_tags: Dict[str, str] = field(default_factory=dict)
    scripts: List[str] = field(default_factory=list)
    cookies: List[str] = field(default_factory=list)
    dns_records: List[str] = field(default_factory=list)
    confidence_score: float = 1.0
    version_regex: Optional[str] = None

@dataclass
class DetectedTech:
    """Represents a detected technology"""
    name: str
    category: TechCategory
    confidence: float
    version: Optional[str] = None
    evidence: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DetectionResult:
    """Complete result from technology detection"""
    url: str
    timestamp: datetime
    technologies: List[DetectedTech]
    total_score: float
    response_time: float
    errors: List[str] = field(default_factory=list)
    raw_data: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "url": self.url,
            "timestamp": self.timestamp.isoformat(),
            "technologies": [
                {
                    "name": tech.name,
                    "category": tech.category.value,
                    "confidence": tech.confidence,
                    "version": tech.version,
                    "evidence": tech.evidence,
                    "metadata": tech.metadata
                }
                for tech in self.technologies
            ],
            "total_score": self.total_score,
            "response_time": self.response_time,
            "errors": self.errors,
            "raw_data": self.raw_data
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)
