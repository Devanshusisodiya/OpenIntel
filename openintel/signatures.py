import typing as t

from openintel.models import TechCategory, TechSignature


class TechSignatures:
    """Database of technology signatures for detection"""
    
    @staticmethod
    def get_all_signatures() -> t.List[TechSignature]:
        """Returns all technology signatures"""
        return [
            # Frontend Frameworks
            TechSignature(
                name="React",
                category=TechCategory.FRONTEND_FRAMEWORK,
                patterns={
                    "html": [r"_react", r"react-dom", r"__REACT_DEVTOOLS_GLOBAL_HOOK__"],
                    "js": [r"React\.createElement", r"ReactDOM\.render"]
                },
                scripts=["react.js", "react.min.js", "react-dom.js"],
                confidence_score=0.9
            ),
            TechSignature(
                name="Vue.js",
                category=TechCategory.FRONTEND_FRAMEWORK,
                patterns={
                    "html": [r"v-if", r"v-for", r"v-model", r"{{.*}}"],
                    "js": [r"Vue\.component", r"new Vue\("]
                },
                scripts=["vue.js", "vue.min.js"],
                confidence_score=0.9
            ),
            TechSignature(
                name="Angular",
                category=TechCategory.FRONTEND_FRAMEWORK,
                patterns={
                    "html": [r"ng-app", r"ng-controller", r"\*ngFor", r"\*ngIf"],
                    "js": [r"angular\.module", r"@angular/"]
                },
                scripts=["angular.js", "angular.min.js"],
                confidence_score=0.9
            ),
            
            # JavaScript Libraries
            TechSignature(
                name="jQuery",
                category=TechCategory.JAVASCRIPT_LIBRARY,
                patterns={
                    "js": [r"jQuery", r"\$\(document\)\.ready"]
                },
                scripts=["jquery.js", "jquery.min.js"],
                confidence_score=0.8
            ),
            TechSignature(
                name="Lodash",
                category=TechCategory.JAVASCRIPT_LIBRARY,
                patterns={"js": [r"_.map", r"_.forEach", r"lodash"]},
                scripts=["lodash.js", "lodash.min.js"],
                confidence_score=0.7
            ),
            
            # CSS Frameworks
            TechSignature(
                name="Bootstrap",
                category=TechCategory.CSS_FRAMEWORK,
                patterns={
                    "html": [r"class=[\"'].*bootstrap", r"class=[\"'].*btn-primary"],
                    "css": [r"bootstrap", r"\.container-fluid"]
                },
                scripts=["bootstrap.js", "bootstrap.min.js"],
                confidence_score=0.8
            ),
            TechSignature(
                name="Tailwind CSS",
                category=TechCategory.CSS_FRAMEWORK,
                patterns={
                    "html": [r"class=[\"'].*flex", r"class=[\"'].*bg-blue-500"],
                    "css": [r"tailwindcss"]
                },
                confidence_score=0.7
            ),
            
            # Analytics
            TechSignature(
                name="Google Analytics",
                category=TechCategory.ANALYTICS,
                patterns={
                    "html": [r"google-analytics\.com", r"gtag\(", r"ga\("],
                    "js": [r"GoogleAnalyticsObject"]
                },
                scripts=["gtag/js", "analytics.js"],
                confidence_score=0.95
            ),
            TechSignature(
                name="Facebook Pixel",
                category=TechCategory.ANALYTICS,
                patterns={
                    "html": [r"connect\.facebook\.net", r"fbq\("],
                    "js": [r"facebook pixel"]
                },
                confidence_score=0.9
            ),
            
            # CDNs
            TechSignature(
                name="Cloudflare",
                category=TechCategory.CDN,
                headers={"server": "cloudflare", "cf-ray": ".*"},
                patterns={"html": [r"cloudflare"]},
                confidence_score=0.95
            ),
            TechSignature(
                name="Amazon CloudFront",
                category=TechCategory.CDN,
                headers={"via": ".*CloudFront", "x-amz-cf-id": ".*"},
                confidence_score=0.9
            ),
            
            # CMS
            TechSignature(
                name="WordPress",
                category=TechCategory.CMS,
                patterns={
                    "html": [r"wp-content", r"wp-includes", r"wordpress"],
                    "meta": [r"generator.*wordpress"]
                },
                meta_tags={"generator": "WordPress"},
                confidence_score=0.95
            ),
            TechSignature(
                name="Drupal",
                category=TechCategory.CMS,
                patterns={
                    "html": [r"drupal", r"sites/default/files"],
                    "meta": [r"generator.*drupal"]
                },
                confidence_score=0.9
            ),
            
            # E-commerce
            TechSignature(
                name="Shopify",
                category=TechCategory.ECOMMERCE,
                patterns={
                    "html": [r"shopify", r"cdn\.shopify\.com"],
                    "js": [r"Shopify\.theme"]
                },
                confidence_score=0.95
            ),
            TechSignature(
                name="WooCommerce",
                category=TechCategory.ECOMMERCE,
                patterns={
                    "html": [r"woocommerce", r"wc-"],
                    "css": [r"woocommerce"]
                },
                confidence_score=0.9
            ),
            
            # Backend Detection (Server Headers)
            TechSignature(
                name="Apache",
                category=TechCategory.BACKEND_FRAMEWORK,
                headers={"server": "Apache"},
                confidence_score=0.8
            ),
            TechSignature(
                name="Nginx",
                category=TechCategory.BACKEND_FRAMEWORK,
                headers={"server": "nginx"},
                confidence_score=0.8
            ),
            TechSignature(
                name="Express.js",
                category=TechCategory.BACKEND_FRAMEWORK,
                headers={"x-powered-by": "Express"},
                confidence_score=0.9
            ),
        ]