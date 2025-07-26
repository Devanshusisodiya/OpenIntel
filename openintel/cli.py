#!/usr/bin/env python3
"""
Command-line interface for OpenIntel
"""

import argparse
import asyncio
import json
import sys
from typing import List

from openintel.analyzer import TechStackAnalyzer
from openintel.detector import TechStackDetector


async def detect_single_site(url: str, output_format: str = "json") -> None:
    """Detect tech stack for a single website"""
    async with TechStackDetector() as detector:
        result = await detector.detect(url)
        
        if output_format == "json":
            print(result.to_json())
        else:
            print(f"\n=== Tech Stack Analysis for {result.url} ===")
            print(f"Scan completed in {result.response_time:.2f} seconds")
            print(f"Total confidence score: {result.total_score:.2f}")
            
            if result.technologies:
                print(f"\nDetected Technologies ({len(result.technologies)}):")
                for tech in sorted(result.technologies, key=lambda x: x.confidence, reverse=True):
                    version_str = f" v{tech.version}" if tech.version else ""
                    print(f"  • {tech.name}{version_str} ({tech.category.value}) - {tech.confidence:.2f}")
                    if tech.evidence:
                        print(f"    Evidence: {tech.evidence[0]}")
            else:
                print("\nNo technologies detected.")
                
            if result.errors:
                print(f"\nErrors:")
                for error in result.errors:
                    print(f"  • {error}")

async def detect_multiple_sites(urls: List[str], output_format: str = "json") -> None:
    """Detect tech stacks for multiple websites"""
    results = []
    
    async with TechStackDetector() as detector:
        tasks = [detector.detect(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    
    if output_format == "json":
        valid_results = [r.to_dict() for r in results if not isinstance(r, Exception)]
        print(json.dumps(valid_results, indent=2))
    else:
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"\nError analyzing {urls[i]}: {result}")
                continue
            
            print(f"\n{'='*60}")
            print(f"Site {i+1}: {result.url}")
            print(f"Technologies: {len(result.technologies)}")
            print(f"Total Score: {result.total_score:.2f}")
            
            if result.technologies:
                top_techs = sorted(result.technologies, key=lambda x: x.confidence, reverse=True)[:5]
                for tech in top_techs:
                    print(f"  • {tech.name} ({tech.confidence:.2f})")

def analyze_trends(results_file: str) -> None:
    """Analyze technology trends from results file"""
    try:
        with open(results_file, 'r') as f:
            data = json.load(f)
        
        analyzer = TechStackAnalyzer()
        
        # Convert JSON data back to DetectionResult objects
        for item in data:
            # Simplified conversion - you'd implement full conversion in practice
            print(f"Trend analysis would process: {item.get('url', 'Unknown')}")
            
    except Exception as e:
        print(f"Error analyzing trends: {e}")

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="TechStack Detector - Analyze website technology stacks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  openintel example.com
  openintel example.com --format table
  openintel --file urls.txt --output results.json
  openintel --analyze results.json
        """
    )
    
    parser.add_argument(
        "url", 
        nargs="?", 
        help="Website URL to analyze"
    )
    
    parser.add_argument(
        "--file", "-f",
        help="File containing URLs to analyze (one per line)"
    )
    
    parser.add_argument(
        "--format",
        choices=["json", "table"],
        default="table",
        help="Output format (default: table)"
    )
    
    parser.add_argument(
        "--output", "-o",
        help="Output file for results"
    )
    
    parser.add_argument(
        "--analyze", "-a",
        help="Analyze trends from results file"
    )
    
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=30,
        help="Request timeout in seconds (default: 30)"
    )
    
    args = parser.parse_args()
    
    # Analyze trends mode
    if args.analyze:
        analyze_trends(args.analyze)
        return
    
    # Determine URLs to process
    urls = []
    if args.url:
        urls = [args.url]
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Error reading file {args.file}: {e}")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)
    
    # Run detection
    if len(urls) == 1:
        asyncio.run(detect_single_site(urls[0], args.format))
    else:
        asyncio.run(detect_multiple_sites(urls, args.format))

if __name__ == "__main__":
    main()