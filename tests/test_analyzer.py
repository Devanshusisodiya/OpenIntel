from datetime import datetime, timedelta

from openintel import DetectionResult, TechStackAnalyzer
from openintel.models import DetectedTech, TechCategory


def test_trend_analysis():
    """Test technology trend analysis"""
    analyzer = TechStackAnalyzer()
    
    # Create mock results
    for i in range(5):
        result = DetectionResult(
            url=f"https://example{i}.com",
            timestamp=datetime.now() - timedelta(days=i),
            technologies=[
                DetectedTech(
                    name="React",
                    category=TechCategory.FRONTEND_FRAMEWORK,
                    confidence=0.9
                )
            ],
            total_score=5.0,
            response_time=1.0
        )
        analyzer.add_result(result)
    
    trends = analyzer.get_technology_trends(days=30)
    
    assert "React" in trends["technology_trends"]
    assert trends["total_sites_analyzed"] == 5
    assert trends["technology_trends"]["React"]["occurrences"] == 5

def test_tech_stack_scoring():
    """Test technology stack scoring"""
    analyzer = TechStackAnalyzer()
    
    result = DetectionResult(
        url="https://example.com",
        timestamp=datetime.now(),
        technologies=[
            DetectedTech(
                name="React",
                category=TechCategory.FRONTEND_FRAMEWORK,
                confidence=0.9
            ),
            DetectedTech(
                name="Cloudflare",
                category=TechCategory.CDN,
                confidence=0.95
            )
        ],
        total_score=10.0,
        response_time=1.0
    )
    
    scores = analyzer.score_tech_stack(result)
    
    assert "overall_score" in scores
    assert "breakdown" in scores
    assert "recommendations" in scores
    assert 0 <= scores["overall_score"] <= 10