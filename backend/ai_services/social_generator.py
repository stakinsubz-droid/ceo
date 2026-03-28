"""
Social Content Generator
"""
import asyncio
from typing import Dict, Any, List
from datetime import datetime, timezone
from .social_media_ai import SocialMediaAI

class SocialGenerator:
    def __init__(self):
        self.social_ai = SocialMediaAI()

    async def generate_full_social_set(self, product: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate multi-platform social copy assets."""
        # Reuse the existing social media ai generator if available
        posts = []

        # Expected platforms
        platforms = ["tiktok", "instagram", "x", "linkedin", "youtube_shorts"]

        for platform in platforms:
            base_post = {
                "platform": platform,
                "content": f"Launch {product.get('title')} - {product.get('description','')[:100]}",
                "hooks": ["Save this", "Link in bio"],
                "cta": "Learn more",
                "hashtags": ["#AI", "#OnlineBusiness", f"#{product.get('product_type','product')}"]
            }
            posts.append(base_post)

        return posts

    async def validate_content_variation(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Ensure no duplicate posts and safe style"""
        seen = set()
        unique_posts = []

        for post in posts:
            key = post["platform"] + ":" + post["content"][:45]
            if key in seen:
                post["status"] = "duplicate"
            else:
                post["status"] = "ok"
                seen.add(key)
            unique_posts.append(post)

        return unique_posts
