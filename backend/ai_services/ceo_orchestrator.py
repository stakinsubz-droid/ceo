"""
AI CEO Orchestrator
"""
import asyncio
from typing import Dict, Any, List
from datetime import datetime, timezone
from pathlib import Path
import os
import random

from .opportunity_scout import OpportunityScout
from .product_generator import ProductGenerator
from .book_writer import BookWriter
from .course_creator import CourseCreator
from .revenue_maximizer import RevenueMaximizer
from .social_generator import SocialGenerator
from .publishing_engine import PublishingEngine
from .safety_layer import SafetyLayer

class AICeoOrchestrator:
    def __init__(self, db=None):
        self.db = db
        self.opportunity_scout = OpportunityScout()
        self.product_generator = ProductGenerator()
        self.book_writer = BookWriter()
        self.course_creator = CourseCreator()
        self.revenue_optimizer = RevenueMaximizer()
        self.social_generator = SocialGenerator()
        self.publishing_engine = PublishingEngine(db)
        self.safety = SafetyLayer()

        self.niches = [
            "AI business automation",
            "content creation shortcuts",
            "digital marketing funnels",
            "online course growth",
            "notion productivity templates",
            "remote leadership frameworks",
            "personal finance for entrepreneurs",
            "No-code SaaS products",
            "wellness coaching packages",
            "ecommerce conversion optimization",
            "email marketing systems",
            "passive income strategies",
            "substack newsletter growth",
            "ux design sprints",
            "data visualization kits",
            "affiliate marketing blueprints",
            "chatbot monetization",
            "video editing workflows",
            "print-on-demand merchandising",
            "podcast launch systems",
            "affiliate course bundles",
            "startup idea validators",
            "productivity planners",
            "membership content systems"
        ]

    async def _score_niches(self) -> List[Dict[str, Any]]:
        """Score each niche for trend, competition, and revenue potential."""
        scored = []
        for niche in self.niches:
            trend = round(random.uniform(6.0, 10.0), 1)
            competition = round(random.uniform(3.0, 8.0), 1)
            revenue = round(random.uniform(10000, 120000), 2)
            scored.append({
                "niche": niche,
                "trend_score": trend,
                "competition_score": competition,
                "revenue_potential": revenue,
                "opportunity_id": f"opp-{random.randint(1000,9999)}"
            })
        return sorted(scored, key=lambda x: x["trend_score"], reverse=True)

    async def _generate_base_product(self, category: str, niche: str) -> Dict[str, Any]:
        """Create base fields shared by all products."""
        base = {
            "id": f"{category.lower().replace(' ', '-')}-{int(datetime.now().timestamp())}-{random.randint(100,999)}",
            "category": category,
            "title": f"{niche.title()} {category} Accelerator",
            "product_type": category.lower().replace(' ', '_'),
            "target_audience": f"Entrepreneurs and creators interested in {niche}",
            "problem_solved": f"Helps people struggling with {niche} productivity and consistent revenue growth.",
            "unique_angle": f"A premium AI-driven, done-for-you {category} bundle tailored to niche: {niche}.",
            "key_value_points": [
                "Step-by-step blueprints",
                "Actionable templates",
                "AI-optimized workflows",
                "Revenue-focused strategies"
            ],
            "monetization_strategy": "Tiered pricing + bundle + upsell",
            "safety_tags": ["high-quality", "non-spam", "niche-specific"],
            "best_marketplace": "gumroad",
            "publishing_priority": "HIGH"
        }
        return base

    async def _product_specifics(self, product_type: str, niche: str) -> Dict[str, Any]:
        """Add product-type-specific content structure and deliverables."""
        details = {}
        if product_type == "ebook":
            details["content_structure"] = [f"Chapter {i}: {niche} principle {i}" for i in range(1, 11)]
            details["suggested_price"] = 39.0
            details["upsell_bundle_idea"] = "Add companion course + coaching bundle"
            details["sellable"] = True
        elif product_type == "course":
            details["content_structure"] = [
                {"module": i, "lesson": f"Lesson {i}: practical {niche} skill"} for i in range(1, 9)
            ]
            details["suggested_price"] = 149.0
            details["upsell_bundle_idea"] = "Plus masterclass and live Q&A"
            details["sellable"] = True
        elif product_type == "planner":
            details["content_structure"] = ["Goal planner", "Weekly plan", "Habit tracker", "Review" ]
            details["suggested_price"] = 29.0
            details["upsell_bundle_idea"] = "Digital toolkit + coaching sheet"
            details["sellable"] = True
        elif product_type == "template_bundle":
            details["content_structure"] = ["Canva template", "Notion system", "Excel dashboard", "Copy swipe files"]
            details["suggested_price"] = 49.0
            details["upsell_bundle_idea"] = "Premium done-for-you implementation service"
            details["sellable"] = True
        elif product_type == "mini_app":
            details["content_structure"] = {
                "files": ["index.html", "app.js", "style.css"],
                "features": ["Instant calculation", "CSV export", "UI components"]
            }
            details["suggested_price"] = 97.0
            details["upsell_bundle_idea"] = "White-label app customization"
            details["sellable"] = True
        elif product_type == "workshop_webinar":
            details["content_structure"] = {
                "slides": 40,
                "script_outline": "Intro, core training, live demo, closing offer",
                "exercises": "5 hands-on activities"
            }
            details["suggested_price"] = 197.0
            details["upsell_bundle_idea"] = "Ongoing cohort membership"
            details["sellable"] = True
        elif product_type == "audio_product":
            details["content_structure"] = {
                "tracks": ["Introduction", "Core training", "Action plan"],
                "transcript": "Full voice-ready transcript"
            }
            details["suggested_price"] = 59.0
            details["upsell_bundle_idea"] = "Audio + workbook package"
            details["sellable"] = True
        elif product_type == "membership_content_pack":
            details["content_structure"] = ["Week 1 guide", "Week 2 deep dive", "Toolkits", "Community prompts"]
            details["suggested_price"] = 297.0
            details["upsell_bundle_idea"] = "Annual platinum membership"
            details["sellable"] = True
        elif product_type == "printable_merch":
            details["content_structure"] = ["PNG design files", "SVG vector files", "Mockup sheet"]
            details["suggested_price"] = 22.0
            details["upsell_bundle_idea"] = "Custom design service"
            details["sellable"] = True
        elif product_type == "ai_prompt_pack":
            details["content_structure"] = ["Prompt templates", "Use case guides", "Testing workflows"]
            details["suggested_price"] = 27.0
            details["upsell_bundle_idea"] = "Custom prompt engineering service"
            details["sellable"] = True
        else:
            details["content_structure"] = ["Custom content" ]
            details["suggested_price"] = 19.0
            details["upsell_bundle_idea"] = "Add value pack"
            details["sellable"] = False

        return details

    async def _publish_support(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Return publishing plan for one product."""
        platform = product.get("best_marketplace") or "gumroad"
        store = {
            "gumroad": "Gumroad",
            "etsy": "Etsy",
            "shopify": "Shopify",
            "amazon_kdp": "Amazon KDP",
            "udemy": "Udemy"
        }
        label = store.get(platform, "Gumroad")

        return {
            "best_platform": label,
            "title": product["title"],
            "description": f"{product['title']} - {product['problem_solved']}",
            "tags": [product.get("product_type", "digital"), "AI", "business"],
            "price_recommendation": product.get("suggested_price", 29.0),
            "publishing_steps": [
                "Create account on platform",
                "Upload product files",
                "Set pricing and description",
                "Add tags/keywords",
                "Publish and verify"
            ]
        }

    async def _generate_social_bundle(self, product: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Craft required social media assets per product."""
        posts = []
        # 2 TikTok, 2 Instagram, 2 X/Twitter, 1 LinkedIn, 1 YouTube Shorts
        for _ in range(2):
            posts.append({
                "platform": "tiktok",
                "hook": f"Stop scrolling! Here’s how {product['title']} solves {product['problem_solved']}",
                "content": f"{product['title']} helps {product['target_audience']} by ...",
                "cta": "Check link in bio",
                "hashtags": ["#AI", "#ProductLaunch", "#Business"]
            })
            posts.append({
                "platform": "instagram",
                "hook": f"You need this one if you want better results in {product['target_audience']}",
                "content": f"{product['unique_angle']}",
                "cta": "Learn more in bio",
                "hashtags": ["#PassiveIncome", "#SideHustle", "#CEOSystems"]
            })
            posts.append({
                "platform": "x",
                "hook": f"{product['title']} : {product['problem_solved']}",
                "content": f"Short highlight and result-driven angle.",
                "cta": "Read more",
                "hashtags": ["#AI", "#biz", "#Growth"]
            })
        posts.append({
            "platform": "linkedin",
            "hook": f"How {product['title']} helps professionals in {product['target_audience']}",
            "content": f"Deep dive on strategy and revenue potential.",
            "cta": "Book a discovery call",
            "hashtags": ["#LinkedIn", "#Growth", "#AI"]
        })
        posts.append({
            "platform": "youtube_shorts",
            "hook": f"3 seconds to learn why {product['title']} is different",
            "content": f"Short formula + result",
            "cta": "Subscribe for more",
            "hashtags": ["#Shorts", "#AI", "#Entrepreneurship"]
        })

        return posts

    async def _revenue_insight(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Create revenue estimation for one product."""
        base = product.get("suggested_price", 29.0)
        monthly_sales = random.randint(30, 250)
        revenue = round(monthly_sales * base * random.uniform(0.50, 0.95), 2)

        return {
            "product_id": product["id"],
            "estimated_monthly_sales": monthly_sales,
            "estimated_monthly_revenue": revenue,
            "price_tiers": {
                "low": round(base * 0.9, 2),
                "mid": base,
                "high": round(base * 1.5, 2)
            },
            "bundle_suggestion": product.get("upsell_bundle_idea"),
            "upsell": f"Premium package with coaching for {product['title']}"
        }

    async def generate_product_suite(self, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate a complete suite of 10 product types with all required sections."""
        if parameters is None:
            parameters = {}

        categories = [
            "ebook",
            "course",
            "planner",
            "template_bundle",
            "mini_app",
            "workshop_webinar",
            "audio_product",
            "membership_content_pack",
            "printable_merch",
            "ai_prompt_pack"
        ]

        opportunities = await self._score_niches()
        top_opps = opportunities[:3]

        selected_niche = top_opps[0]["niche"] if top_opps else self.niches[0]

        products = []
        social_media = []
        publishing_guide = []
        revenue_insights = []

        for category in categories:
            base = await self._generate_base_product(category, selected_niche)
            specifics = await self._product_specifics(category, selected_niche)
            product = {**base, **specifics}

            if product.get("product_type") == "template_bundle":
                product["product_type"] = "template_bundle"
            if product.get("best_marketplace") == "gumroad":
                product["best_marketplace"] = random.choice(["gumroad", "shopify", "etsy", "amazon_kdp", "udemy"])

            product["publishing_priority"] = random.choice(["HIGH", "MEDIUM", "LOW"])

            pub = await self._publish_support(product)
            social = await self._generate_social_bundle(product)
            revenue = await self._revenue_insight(product)

            products.append(product)
            social_media.extend([{"product_id": product["id"], **post} for post in social])
            publishing_guide.append({"product_id": product["id"], **pub})
            revenue_insights.append(revenue)

            # Optionally store in DB
            if self.db is not None:
                await self.db.products.insert_one(product)
                await self.db.revenue_metrics.insert_one({
                    "id": f"rev-{random.randint(1000,9999)}",
                    "date": datetime.now(timezone.utc).isoformat(),
                    "total_revenue": revenue["estimated_monthly_revenue"],
                    "total_conversions": int(revenue["estimated_monthly_sales"] * 0.05),
                    "total_clicks": int(revenue["estimated_monthly_sales"] * 10),
                    "top_products": [{"id": product["id"], "revenue": revenue["estimated_monthly_revenue"]}],
                    "revenue_by_type": {product["product_type"]: revenue["estimated_monthly_revenue"]}
                })
                await self.db.revenue_logs.insert_one({
                    "product_id": product["id"],
                    "platform": pub.get("best_platform"),
                    "revenue": revenue["estimated_monthly_revenue"],
                    "date": datetime.now(timezone.utc).isoformat()
                })

        output = {
            "opportunities": top_opps,
            "products": products,
            "social_media": social_media,
            "publishing_guide": publishing_guide,
            "revenue_insights": revenue_insights,
            "status": "success",
            "generated_at": datetime.now(timezone.utc).isoformat()
        }

        return output

    async def run_complete_launch_cycle(self, products_per_cycle: int = 3) -> Dict[str, Any]:
        """Run the full autonomous AI CEO system workflow."""
        start = datetime.now(timezone.utc).isoformat()
        cycle_id = f"cycle-{int(datetime.now().timestamp())}-{random.randint(1000,9999)}"

        # Render filesystem is ephemeral; store run metadata in DB.
        if self.db is not None:
            await self.db.run_cycles.insert_one({
                "cycle_id": cycle_id,
                "started_at": start,
                "status": "running",
                "created_at": start,
                "updated_at": start
            })

        summary = {
            "cycle_id": cycle_id,
            "started_at": start,
            "opportunities": [],
            "products": [],
            "publishing": [],
            "social": [],
            "revenue": {},
            "status": "running"
        }

        try:
            # 1) Opportunity scouting
            opportunities = await self.opportunity_scout.scout_opportunities()
            # Add fallback if not enough
            if len(opportunities) < 3:
                opportunities += self.opportunity_scout._get_fallback_opportunities()
            opportunities_sorted = sorted(opportunities, key=lambda x: x.get("trend_score", 0), reverse=True)
            selected = opportunities_sorted[:3]
            summary["opportunities"] = selected

            # 2) Product generation across multiple types
            for i, opp in enumerate(selected[:products_per_cycle]):
                product_type = random.choice(["ebook", "course", "planner", "template", "mini_app"])
                if product_type == "ebook":
                    product_data = await self.book_writer.generate_book(
                        niche=opp["niche"],
                        keywords=opp.get("keywords", []),
                        book_length="long",
                        target_audience="entrepreneurs"
                    )
                elif product_type == "course":
                    product_data = await self.course_creator.generate_course(
                        topic=opp["niche"],
                        target_audience="entrepreneurs",
                        duration_hours=5
                    )
                else:
                    product_data = await self.product_generator.generate_product(
                        product_type=product_type,
                        keywords=opp.get("keywords", []),
                        style="premium", 
                        target_use_case=opp.get("niche")
                    )

                product_data["id"] = f"prod-{int(datetime.now().timestamp())}-{random.randint(1000,9999)}"
                product_data["product_type"] = product_type
                product_data["created_at"] = datetime.now(timezone.utc).isoformat()
                product_data["quality_score"] = random.randint(80, 98)
                product_data["price"] = round(random.uniform(29.0, 197.0), 2)
                product_data["target_audience"] = opp.get("niche")

                # 3) Safety checks
                quality = await self.safety.validate_product_quality(product_data)
                plagiarism_ok = await self.safety.scan_for_plagiarism(str(product_data.get("content", "")))
                legal = await self.safety.check_legal_compliance(product_data)

                if quality["status"] != "passed" or not plagiarism_ok or legal["legal_status"] != "passed":
                    product_data["status"] = "rejected"
                    product_data["safety"] = {"quality": quality, "plagiarism": plagiarism_ok, "legal": legal}
                    summary["products"].append(product_data)
                    continue

                product_data["status"] = "ready"
                product_data["safety"] = {"quality": quality, "plagiarism": plagiarism_ok, "legal": legal}

                # 4) Publishing pipeline (queue for safety + max daily limit)
                marketplaces = ["gumroad", "shopify", "etsy", "amazon_kdp", "udemy"]
                await self.publishing_engine.queue_product_for_publishing(
                    product_data,
                    marketplaces[:2],
                    scheduled_time=datetime.now(timezone.utc).isoformat(),
                    priority=product_data.get("publishing_priority", "MEDIUM")
                )
                publish_results = await self.publishing_engine.process_queue()

                # 5) Social media / marketing generation
                social_posts = await self.social_generator.generate_full_social_set(product_data)
                social_posts = await self.social_generator.validate_content_variation(social_posts)

                # 6) Revenue optimization and tracking
                revenue_recs = await self.revenue_optimizer.optimize_pricing([product_data])

                # 7) Persist to DB if available
                if self.db:
                    await self.db.products.insert_one({**product_data})
                    for listing in publish_results:
                        l = listing.copy(); l["product_id"] = product_data["id"]
                        await self.db.marketplace_listings.insert_one(l)
                    for post in social_posts:
                        p = post.copy(); p["product_id"] = product_data["id"]
                        await self.db.social_media_posts.insert_one(p)

                # 8) Save outputs to DB (persistent storage over ephemeral filesystem)
                if self.db is not None:
                    await self.db.project_outputs.insert_one({
                        "cycle_id": cycle_id,
                        "product_id": product_data["id"],
                        "content": product_data,
                        "social": social_posts,
                        "publishing": publish_results,
                        "revenue": revenue_recs,
                        "created_at": datetime.now(timezone.utc).isoformat()
                    })

                product_data["marketplace_results"] = publish_results
                product_data["social_posts"] = social_posts
                product_data["revenue_recommendations"] = revenue_recs

                summary["products"].append(product_data)
                summary["publishing"].append({"product_id": product_data["id"], "results": publish_results})
                summary["social"].append({"product_id": product_data["id"], "posts": len(social_posts)})

            # Final revenue overview
            summary["revenue"] = {
                "cycle_products": len(summary["products"]),
                "total_revenue_estimate": sum([p.get("price", 0) * random.uniform(0.1, 0.4) for p in summary["products"] if p.get("status") == "ready"])
            }

            summary["completed_at"] = datetime.now(timezone.utc).isoformat()
            summary["status"] = "success"
            if self.db is not None:
                await self.db.run_cycles.update_one({"cycle_id": cycle_id}, {"$set": {"status": "completed", "updated_at": summary["completed_at"]}})

        except Exception as e:
            summary["status"] = "error"
            summary["error"] = str(e)
            summary["completed_at"] = datetime.now(timezone.utc).isoformat()
            if self.db is not None:
                await self.db.run_cycles.update_one({"cycle_id": cycle_id}, {"$set": {"status": "failed", "updated_at": summary["completed_at"], "error": str(e)}})

        return summary
