import re
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse

import aiohttp
import dns.resolver
from bs4 import BeautifulSoup

from openintel.models import DetectedTech, DetectionResult, TechCategory
from openintel.signatures import TechSignatures


class TechStackDetector:
    """Main detector class for identifying technology stacks"""
    
    def __init__(self, timeout: int = 30, max_redirects: int = 5):
        self.timeout = timeout
        self.max_redirects = max_redirects
        self.signatures = TechSignatures.get_all_signatures()
        self.session = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            connector=aiohttp.TCPConnector(limit=100, limit_per_host=30)
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def detect(self, url: str) -> DetectionResult:
        """Main detection method"""
        start_time = time.time()
        
        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'
            
        result = DetectionResult(
            url=url,
            timestamp=datetime.now(),
            technologies=[],
            total_score=0.0,
            response_time=0.0,
            errors=[],
            raw_data={}
        )
        
        try:
            # Gather all data concurrently
            html_content, headers, status_code = await self._fetch_page(url)
            dns_info = await self._get_dns_info(url)
            
            result.raw_data = {
                'headers': dict(headers),
                'status_code': status_code,
                'dns_info': dns_info,
                'html_length': len(html_content) if html_content else 0
            }
            
            if html_content:
                # Parse HTML
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Extract various elements
                scripts = self._extract_scripts(soup)
                styles = self._extract_styles(soup)
                meta_tags = self._extract_meta_tags(soup)
                
                # Detect technologies
                detected_techs = []
                
                for signature in self.signatures:
                    detection = self._check_signature(
                        signature, html_content, headers, scripts, 
                        styles, meta_tags, dns_info
                    )
                    if detection:
                        detected_techs.append(detection)
                
                result.technologies = detected_techs
                result.total_score = sum(tech.confidence for tech in detected_techs)
                
        except Exception as e:
            result.errors.append(f"Detection error: {str(e)}")
        
        result.response_time = time.time() - start_time
        return result
    
    async def _fetch_page(self, url: str) -> Tuple[Optional[str], Dict[str, str], int]:
        """Fetch webpage content and headers"""
        try:
            if not self.session:
                raise RuntimeError("Detector must be used as async context manager")
                
            async with self.session.get(
                url, 
                allow_redirects=True,
                max_redirects=self.max_redirects
            ) as response:
                headers = {k.lower(): v for k, v in response.headers.items()}
                content = await response.text()
                return content, headers, response.status
                
        except Exception as e:
            return None, {}, 0
    
    async def _get_dns_info(self, url: str) -> Dict[str, Any]:
        """Get DNS information for the domain"""
        try:
            domain = urlparse(url).netloc
            if not domain:
                return {}
                
            dns_info = {}
            
            # Get A records
            try:
                a_records = dns.resolver.resolve(domain, 'A')
                dns_info['a_records'] = [str(r) for r in a_records]
            except:
                pass
                
            # Get CNAME records
            try:
                cname_records = dns.resolver.resolve(domain, 'CNAME')
                dns_info['cname_records'] = [str(r) for r in cname_records]
            except:
                pass
                
            # Get MX records
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                dns_info['mx_records'] = [str(r) for r in mx_records]
            except:
                pass
                
            return dns_info
            
        except Exception:
            return {}
    
    def _extract_scripts(self, soup: BeautifulSoup) -> List[str]:
        """Extract script sources and inline scripts"""
        scripts = []
        
        # External scripts
        for script in soup.find_all('script', src=True):
            scripts.append(script.get('src', ''))
            
        # Inline scripts
        for script in soup.find_all('script'):
            if script.string:
                scripts.append(script.string)
                
        return scripts
    
    def _extract_styles(self, soup: BeautifulSoup) -> List[str]:
        """Extract stylesheet links and inline styles"""
        styles = []
        
        # External stylesheets
        for link in soup.find_all('link', rel='stylesheet'):
            styles.append(link.get('href', ''))
            
        # Inline styles
        for style in soup.find_all('style'):
            if style.string:
                styles.append(style.string)
                
        return styles
    
    def _extract_meta_tags(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract meta tag information"""
        meta_tags = {}
        
        for meta in soup.find_all('meta'):
            name = meta.get('name', '').lower()
            content = meta.get('content', '')
            
            if name and content:
                meta_tags[name] = content
                
        return meta_tags
    
    def _check_signature(
        self, 
        signature, 
        html_content: str, 
        headers: Dict[str, str],
        scripts: List[str], 
        styles: List[str], 
        meta_tags: Dict[str, str],
        dns_info: Dict[str, Any]
    ) -> Optional[DetectedTech]:
        """Check if a technology signature matches"""
        
        evidence = []
        confidence_factors = []
        
        # Check HTML patterns
        if 'html' in signature.patterns:
            for pattern in signature.patterns['html']:
                if re.search(pattern, html_content, re.IGNORECASE):
                    evidence.append(f"HTML pattern: {pattern}")
                    confidence_factors.append(0.8)
        
        # Check JavaScript patterns
        if 'js' in signature.patterns:
            all_js = ' '.join(scripts)
            for pattern in signature.patterns['js']:
                if re.search(pattern, all_js, re.IGNORECASE):
                    evidence.append(f"JS pattern: {pattern}")
                    confidence_factors.append(0.9)
        
        # Check CSS patterns
        if 'css' in signature.patterns:
            all_css = ' '.join(styles)
            for pattern in signature.patterns['css']:
                if re.search(pattern, all_css, re.IGNORECASE):
                    evidence.append(f"CSS pattern: {pattern}")
                    confidence_factors.append(0.7)
        
        # Check script sources
        for script_pattern in signature.scripts:
            for script in scripts:
                if script_pattern.lower() in script.lower():
                    evidence.append(f"Script: {script}")
                    confidence_factors.append(0.9)
        
        # Check headers
        for header_name, header_pattern in signature.headers.items():
            header_value = headers.get(header_name.lower(), '')
            if re.search(header_pattern, header_value, re.IGNORECASE):
                evidence.append(f"Header {header_name}: {header_value}")
                confidence_factors.append(0.95)
        
        # Check meta tags
        for meta_name, meta_pattern in signature.meta_tags.items():
            meta_value = meta_tags.get(meta_name.lower(), '')
            if re.search(meta_pattern, meta_value, re.IGNORECASE):
                evidence.append(f"Meta {meta_name}: {meta_value}")
                confidence_factors.append(0.85)
        
        # If we found evidence, create detection
        if evidence:
            # Calculate confidence score
            base_confidence = signature.confidence_score
            evidence_boost = min(len(confidence_factors) * 0.1, 0.3)
            final_confidence = min(base_confidence + evidence_boost, 1.0)
            
            # Try to extract version if pattern provided
            version = None
            if signature.version_regex:
                version_match = re.search(signature.version_regex, html_content)
                if version_match:
                    version = version_match.group(1)
            
            return DetectedTech(
                name=signature.name,
                category=signature.category,
                confidence=final_confidence,
                version=version,
                evidence=evidence,
                metadata={}
            )
        
        return None