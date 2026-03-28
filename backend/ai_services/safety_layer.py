"""
Safety & Compliance Layer
"""
import asyncio
from typing import Dict, Any, List
from datetime import datetime, timezone

class SafetyLayer:
    def __init__(self):
        self.max_daily_publications = 5
        self.daily_publishing_count = {}

    async def validate_product_quality(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure each product meets minimum quality standards."""
        issues = []
        if not product.get("title") or len(product.get("title", "")) < 10:
            issues.append("Title is too short")
        if not product.get("description") or len(product.get("description", "")) < 30:
            issues.append("Description is too short")
        if product.get("quality_score") is None:
            product["quality_score"] = 75
        if len(product.get("content", "")) < 200:
            issues.append("Content may be too short")

        status = "passed" if not issues else "failed"
        return {
            "status": status,
            "issues": issues,
            "quality_score": product.get("quality_score", 75)
        }

    async def check_platform_tos(self, product: Dict[str, Any], marketplace: str) -> Dict[str, Any]:
        """Basic TOS compliance simulation for marketplaces."""
        disallowed = ["plagiarism", "adult", "illegal"]
        content_text = str(product.get("content", "")).lower()

        violation = any(term in content_text for term in disallowed)
        if violation:
            return {
                "marketplace": marketplace,
                "status": "rejected",
                "reason": "Potential TOS violation"
            }

        return {
            "marketplace": marketplace,
            "status": "passed",
            "reason": "No immediate violations"
        }

    async def monitor_social_spam(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Rate-limiting style checks for generated social posts."""
        statuses = []
        for post in posts:
            if len(post.get("content", "")) < 15:
                statuses.append({"post": post.get("platform"), "status": "rejected", "reason": "Too short"})
            else:
                statuses.append({"post": post.get("platform"), "status": "approved"})

        return {"platform_checks": statuses}

    async def enforce_daily_publication_limit(self, platform: str, count: int = 1) -> bool:
        """Ensure safe staggered publishing per platform."""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        key = f"{platform}-{today}"
        current = self.daily_publishing_count.get(key, 0)
        if current + count > self.max_daily_publications:
            return False

        self.daily_publishing_count[key] = current + count
        return True

    async def scan_for_plagiarism(self, text: str) -> bool:
        """Mock plagiarism scanner - always OK in demo mode."""
        blacklisted = ["copy", "duplicate", "ripoff"]
        content = text.lower()
        return not any(word in content for word in blacklisted)

    async def check_legal_compliance(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Basic legal and privacy checks."""
        required = ["terms_of_service", "privacy_policy"]
        missing = [item for item in required if not product.get(item)]
        return {
            "legal_status": "passed" if not missing else "incomplete",
            "missing": missing
        }
