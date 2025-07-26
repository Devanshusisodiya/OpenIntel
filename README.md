# OpenIntel

A comprehensive Python package for detecting and analyzing technology stacks used by websites. Perfect for competitive intelligence, lead generation, and market research.

## Features

- **Comprehensive Detection**: Identifies 50+ technologies across multiple categories
- **Fast Async Processing**: Concurrent analysis of multiple websites
- **Detailed Analysis**: Confidence scoring and evidence collection
- **Trend Analysis**: Track technology adoption over time
- **CLI Interface**: Easy command-line usage
- **API Ready**: Use as a library in your Python projects

## Categories Detected

- Frontend Frameworks (React, Vue.js, Angular)
- JavaScript Libraries (jQuery, Lodash)
- CSS Frameworks (Bootstrap, Tailwind CSS)
- Analytics (Google Analytics, Facebook Pixel)
- CDNs (Cloudflare, Amazon CloudFront)
- CMS (WordPress, Drupal)
- E-commerce (Shopify, WooCommerce)
- Backend Technologies (Apache, Nginx, Express.js)
- And many more...

## Installation

```bash
pip install openintel
```

## Quick Start

### Command Line Usage

```bash
# Analyze a single website
openintel example.com

# Analyze multiple websites from file
openintel --file urls.txt --format json --output results.json

# Analyze with custom timeout
openintel example.com --timeout 60
```

### Python API Usage

```python
import asyncio
from openintel import TechStackDetector, TechStackAnalyzer

async def main():
    # Basic detection
    async with TechStackDetector() as detector:
        result = await detector.detect("https://example.com")
        
        print(f"Found {len(result.technologies)} technologies")
        for tech in result.technologies:
            print(f"- {tech.name} ({tech.confidence:.2f})")
    
    # Advanced analysis
    analyzer = TechStackAnalyzer()
    analyzer.add_result(result)
    
    # Get technology scoring
    scores = analyzer.score_tech_stack(result)
    print(f"Overall tech stack score: {scores['overall_score']}/10")

asyncio.run(main())
```

## API Reference

### TechStackDetector

Main detection class with async context manager support.

```python
async with TechStackDetector(timeout=30) as detector:
    result = await detector.detect(url)
```

### DetectionResult

Contains comprehensive analysis results:

```python
class DetectionResult:
    url: str
    timestamp: datetime
    technologies: List[DetectedTech]
    total_score: float
    response_time: float
    errors: List[str]
    raw_data: Dict[str, Any]
```

### TechStackAnalyzer

Advanced analysis and trend tracking:

```python
analyzer = TechStackAnalyzer()
trends = analyzer.get_technology_trends(days=30)
scores = analyzer.score_tech_stack(result)
```

## Detection Methods

The detector uses multiple techniques:

1. **HTML Pattern Matching**: Searches for framework-specific patterns
2. **JavaScript Analysis**: Identifies libraries and frameworks
3. **HTTP Headers**: Analyzes server and security headers
4. **Meta Tags**: Extracts generator and other meta information
5. **Script Sources**: Identifies external libraries and CDNs
6. **DNS Analysis**: Checks for hosting and CDN providers

## Example Output

```json
{
  "url": "https://example.com",
  "timestamp": "2024-01-15T10:30:00",
  "technologies": [
    {
      "name": "React",
      "category": "frontend_framework",
      "confidence": 0.95,
      "version": "18.2.0",
      "evidence": ["HTML pattern: _react", "Script: react.min.js"]
    },
    {
      "name": "Cloudflare",
      "category": "cdn",
      "confidence": 0.98,
      "evidence": ["Header server: cloudflare"]
    }
  ],
  "total_score": 15.7,
  "response_time": 2.34
}
```

## Advanced Features

### Batch Processing

```python
urls = ["site1.com", "site2.com", "site3.com"]
async with TechStackDetector() as detector:
    tasks = [detector.detect(url) for url in urls]
    results = await asyncio.gather(*tasks)
```

### Custom Signatures

Extend detection capabilities by adding custom technology signatures:

```python
from openintel.models import TechSignature, TechCategory

custom_sig = TechSignature(
    name="Custom Framework",
    category=TechCategory.FRONTEND_FRAMEWORK,
    patterns={"html": [r"custom-framework"]},
    confidence_score=0.9
)
```

### Trend Analysis

```python
analyzer = TechStackAnalyzer()
for result in results:
    analyzer.add_result(result)

trends = analyzer.get_technology_trends(days=30)
print(f"Most popular: {trends['top_technologies'][0]}")
```

## Performance

- **Concurrent Processing**: Analyze multiple sites simultaneously
- **Async Operations**: Non-blocking I/O for maximum efficiency
- **Intelligent Caching**: Reduces redundant requests
- **Configurable Timeouts**: Prevent hanging requests

## Use Cases

- **Competitive Intelligence**: Analyze competitor tech stacks
- **Lead Generation**: Identify prospects using specific technologies
- **Market Research**: Track technology adoption trends
- **Security Auditing**: Identify outdated or vulnerable technologies
- **Sales Intelligence**: Tailor pitches based on prospect's tech stack

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

- GitHub Issues: Report bugs and request features
- Documentation: Full API documentation available
- Examples: Check the examples/ directory

## Changelog

### v1.0.0
- Initial release
- 50+ technology signatures
- Async detection engine
- CLI interface
- Trend analysis capabilities