import statistics
import typing as t
from collections import Counter, defaultdict
from datetime import datetime, timedelta

from openintel.models import DetectedTech, DetectionResult


class TechStackAnalyzer:
    """Analyzer for technology adoption trends and scoring"""
    
    def __init__(self):
        self.results_cache: t.List[DetectionResult] = []
        
    def add_result(self, result: DetectionResult):
        """Add a detection result to the analyzer"""
        self.results_cache.append(result)
        
    def get_technology_trends(self, days: int = 30) -> t.Dict[str, t.Any]:
        """Analyze technology adoption trends over time"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_results = [r for r in self.results_cache if r.timestamp >= cutoff_date]
        
        if not recent_results:
            return {"error": "No recent data available"}
        
        # Count technology occurrences
        tech_counts = Counter()
        category_counts = defaultdict(Counter)
        confidence_scores = defaultdict(list)
        
        for result in recent_results:
            for tech in result.technologies:
                tech_counts[tech.name] += 1
                category_counts[tech.category.value][tech.name] += 1
                confidence_scores[tech.name].append(tech.confidence)
        
        # Calculate trend data
        trends = {}
        for tech_name, count in tech_counts.most_common():
            avg_confidence = statistics.mean(confidence_scores[tech_name])
            trends[tech_name] = {
                "occurrences": count,
                "adoption_rate": count / len(recent_results),
                "avg_confidence": round(avg_confidence, 3),
                "trend_score": count * avg_confidence
            }
        
        return {
            "period_days": days,
            "total_sites_analyzed": len(recent_results),
            "technology_trends": trends,
            "category_breakdown": dict(category_counts),
            "top_technologies": list(tech_counts.most_common(10))
        }
    
    def score_tech_stack(self, result: DetectionResult) -> t.Dict[str, t.Any]:
        """Generate a comprehensive score for a detected tech stack"""
        if not result.technologies:
            return {"overall_score": 0, "breakdown": {}, "recommendations": []}
        
        scores = {
            "modernity": self._calculate_modernity_score(result.technologies),
            "performance": self._calculate_performance_score(result.technologies),
            "security": self._calculate_security_score(result.technologies),
            "scalability": self._calculate_scalability_score(result.technologies),
            "developer_experience": self._calculate_dx_score(result.technologies)
        }
        
        # Weighted overall score
        weights = {
            "modernity": 0.25,
            "performance": 0.25,
            "security": 0.20,
            "scalability": 0.20,
            "developer_experience": 0.10
        }
        
        overall_score = sum(scores[category] * weights[category] for category in weights)
        
        recommendations = self._generate_recommendations(result.technologies, scores)
        
        return {
            "overall_score": round(overall_score, 2),
            "breakdown": scores,
            "recommendations": recommendations,
            "technology_categories": self._categorize_technologies(result.technologies)
        }
    
    def _calculate_modernity_score(self, technologies: t.List[DetectedTech]) -> float:
        """Calculate how modern the tech stack is"""
        modern_techs = {
            "React": 9,
            "Vue.js": 9,
            "Angular": 8,
            "Svelte": 10,
            "Next.js": 10,
            "Tailwind CSS": 9,
            "TypeScript": 9,
            "GraphQL": 9
        }
        
        outdated_techs = {
            "jQuery": 3,
            "Internet Explorer": 1,
            "Flash": 1,
            "AngularJS": 4
        }
        
        total_score = 0
        tech_count = 0
        
        for tech in technologies:
            if tech.name in modern_techs:
                total_score += modern_techs[tech.name] * tech.confidence
                tech_count += 1
            elif tech.name in outdated_techs:
                total_score += outdated_techs[tech.name] * tech.confidence
                tech_count += 1
        
        return (total_score / tech_count) if tech_count > 0 else 5.0
    
    def _calculate_performance_score(self, technologies: t.List[DetectedTech]) -> float:
        """Calculate performance-related score"""
        cdn_techs = ["Cloudflare", "Amazon CloudFront", "KeyCDN", "MaxCDN"]
        performance_techs = ["AMP", "Service Worker", "HTTP/2", "Gzip"]
        heavy_techs = ["jQuery UI", "Bootstrap 3", "Font Awesome 4"]
        
        score = 5.0  # Base score
        
        for tech in technologies:
            if tech.name in cdn_techs:
                score += 1.5 * tech.confidence
            elif tech.name in performance_techs:
                score += 1.0 * tech.confidence
            elif tech.name in heavy_techs:
                score -= 0.5 * tech.confidence
        
        return min(max(score, 0), 10)
    
    def _calculate_security_score(self, technologies: t.List[DetectedTech]) -> float:
        """Calculate security-related score"""
        secure_techs = ["Cloudflare", "Let's Encrypt", "HSTS", "CSP"]
        insecure_techs = ["HTTP", "Outdated WordPress", "Outdated Drupal"]
        
        score = 5.0
        
        for tech in technologies:
            if tech.name in secure_techs:
                score += 1.0 * tech.confidence
            elif tech.name in insecure_techs:
                score -= 1.5 * tech.confidence
        
        return min(max(score, 0), 10)
    
    def _calculate_scalability_score(self, technologies: t.List[DetectedTech]) -> float:
        """Calculate scalability-related score"""
        scalable_techs = ["React", "Vue.js", "Angular", "Node.js", "Docker", "Kubernetes"]
        
        score = 5.0
        
        for tech in technologies:
            if tech.name in scalable_techs:
                score += 0.8 * tech.confidence
        
        return min(max(score, 0), 10)
    
    def _calculate_dx_score(self, technologies: t.List[DetectedTech]) -> float:
        """Calculate developer experience score"""
        good_dx_techs = ["React", "Vue.js", "TypeScript", "Webpack", "npm"]
        
        score = 5.0
        
        for tech in technologies:
            if tech.name in good_dx_techs:
                score += 0.6 * tech.confidence
        
        return min(max(score, 0), 10)
    
    def _categorize_technologies(self, technologies: t.List[DetectedTech]) -> t.Dict[str, t.List[str]]:
        """Group technologies by category"""
        categories = defaultdict(list)
        
        for tech in technologies:
            categories[tech.category.value].append({
                "name": tech.name,
                "confidence": tech.confidence,
                "version": tech.version
            })
        
        return dict(categories)
    
    def _generate_recommendations(self, technologies: t.List[DetectedTech], scores: t.Dict[str, float]) -> t.List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        tech_names = [tech.name for tech in technologies]
        
        # Modernity recommendations
        if scores["modernity"] < 6:
            if "jQuery" in tech_names and "React" not in tech_names:
                recommendations.append("Consider migrating from jQuery to a modern framework like React or Vue.js")
            if "Bootstrap 3" in tech_names:
                recommendations.append("Upgrade to Bootstrap 5 or consider Tailwind CSS for better performance")
        
        # Performance recommendations
        if scores["performance"] < 6:
            if not any(cdn in tech_names for cdn in ["Cloudflare", "Amazon CloudFront"]):
                recommendations.append("Implement a CDN solution like Cloudflare for better performance")
            recommendations.append("Consider implementing lazy loading and code splitting")
        
        # Security recommendations
        if scores["security"] < 6:
            recommendations.append("Implement Content Security Policy (CSP) headers")
            recommendations.append("Ensure all dependencies are up to date")
        
        return recommendations