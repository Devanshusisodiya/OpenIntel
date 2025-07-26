import asyncio

import pytest

from openintel import DetectionResult, TechStackDetector


@pytest.mark.asyncio
async def test_basic_detection():
    """Test basic website detection"""
    async with TechStackDetector() as detector:
        result = await detector.detect("https://httpbin.org")
        
        assert isinstance(result, DetectionResult)
        assert result.url.startswith("https://")
        assert result.response_time > 0
        assert isinstance(result.technologies, list)

@pytest.mark.asyncio
async def test_invalid_url():
    """Test handling of invalid URLs"""
    async with TechStackDetector() as detector:
        result = await detector.detect("invalid-url")
        
        assert len(result.errors) > 0 or len(result.technologies) == 0

@pytest.mark.asyncio
async def test_timeout_handling():
    """Test timeout handling"""
    async with TechStackDetector(timeout=1) as detector:
        # This should either succeed quickly or timeout gracefully
        result = await detector.detect("https://httpbin.org/delay/5")
        
        # Should not crash and should handle timeout gracefully
        assert isinstance(result, DetectionResult)

def test_detection_result_serialization():
    """Test DetectionResult JSON serialization"""
    from datetime import datetime

    from openintel.models import DetectedTech, TechCategory
    
    result = DetectionResult(
        url="https://example.com",
        timestamp=datetime.now(),
        technologies=[
            DetectedTech(
                name="React",
                category=TechCategory.FRONTEND_FRAMEWORK,
                confidence=0.9,
                evidence=["test evidence"]
            )
        ],
        total_score=5.5,
        response_time=1.2
    )
    
    json_str = result.to_json()
    assert "React" in json_str
    assert "frontend_framework" in json_str
    assert "0.9" in json_str