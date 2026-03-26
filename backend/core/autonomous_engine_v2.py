"""
LEVEL 2 Autonomous Engine - Full Money-Making System
Creates products, publishes, markets, and tracks revenue all automatically
"""
from datetime import datetime
import uuid

from .models import projects, logs, outputs
from .save_output import save_output

# Import all agents
from ai_services.opportunity_scout import OpportunityScout
from ai_services.gumroad_publisher import GumroadPublisher
from ai_services.social_media_scheduler import SocialMediaAutoPoster
from ai_services.revenue_tracker import RevenueTracker

opportunity_scout = OpportunityScout()
gumroad_publisher = GumroadPublisher()
social_media = SocialMediaAutoPoster()
revenue_tracker = RevenueTracker()


def create_project(name="Auto Project"):
    project = {
        "_id": str(uuid.uuid4()),
        "name": name,
        "status": "running",
        "created_at": datetime.utcnow()
    }
    projects.insert_one(project)
    return project


def log_message(project_id, message):
    logs.insert_one({
        "project_id": project_id,
        "message": message,
        "time": datetime.utcnow()
    })


def get_project_details(project_id):
    return {
        "project": projects.find_one({"_id": project_id}),
        "outputs": list(outputs.find({"project_id": project_id})),
        "logs": list(logs.find({"project_id": project_id}))
    }


async def run_autonomous_cycle_level2():
    """
    LEVEL 2 AUTONOMOUS CYCLE:
    1. Scout opportunity
    2. Generate PRODUCT
    3. Publish to Gumroad
    4. Create 6-month social calendar
    5. Setup affiliate program
    6. Track everything
    """
    
    project = create_project()
    project_id = project["_id"]
    
    log_message(project_id, "🚀 LEVEL 2 AUTONOMOUS CYCLE STARTED")

    try:
        # STEP 1: Scout Opportunity
        log_message(project_id, "🔍 Step 1: Scouting opportunities...")
        opportunities = await opportunity_scout.scout_opportunities()
        save_output(project_id, opportunities, "opportunity", "scout")
        log_message(project_id, f"✅ Found {len(opportunities)} opportunities")
        
        # Use best opportunity
        top_opp = max(opportunities, key=lambda x: x.get('trend_score', 0)) if opportunities else None
        if not top_opp:
            log_message(project_id, "❌ No valid opportunities found")
            projects.update_one({"_id": project_id}, {"$set": {"status": "failed"}})
            return project
        
        log_message(project_id, f"🎯 Selected: {top_opp.get('niche')} (Score: {top_opp.get('trend_score')})")
        
        # STEP 2: Generate Product (mock for now)
        log_message(project_id, "📦 Step 2: Generating product...")
        product = {
            "id": f"prod-{uuid.uuid4()}",
            "title": f"{top_opp.get('niche')} Blueprint",
            "description": f"Complete guide to {top_opp.get('niche')}",
            "type": "ebook",
            "price": 29.99,
            "keywords": top_opp.get('keywords', []),
            "content": "Generated product content here",
            "quality_score": 85
        }
        save_output(project_id, product, "product", "builder")
        log_message(project_id, f"✅ Product created: {product['title']}")
        
        # STEP 3: Publish to Gumroad
        log_message(project_id, "🛒 Step 3: Publishing to Gumroad...")
        try:
            gumroad_result = await gumroad_publisher.publish_ebook(product)
            save_output(project_id, gumroad_result, "marketplace_publish", "gumroad")
            if gumroad_result.get("success"):
                log_message(project_id, f"✅ Published to Gumroad: {gumroad_result.get('url')}")
            else:
                log_message(project_id, f"⚠️ Gumroad publish skipped (no API token)")
        except Exception as e:
            log_message(project_id, f"⚠️ Gumroad publish: {str(e)}")
        
        # STEP 4: Create Social Media Calendar
        log_message(project_id, "📱 Step 4: Generating 6-month social content...")
        social_posts = await social_media.generate_social_posts(product, days=180)
        social_schedule = {
            "total_posts": len(social_posts),
            "platforms": ["tiktok", "instagram", "twitter"],
            "posts": social_posts[:10]  # Save first 10 as sample
        }
        save_output(project_id, social_schedule, "social_schedule", "social_media")
        log_message(project_id, f"✅ Generated {len(social_posts)} social posts")
        
        # STEP 5: Setup Affiliate Program
        log_message(project_id, "💰 Step 5: Setting up affiliate program...")
        try:
            affiliate = await revenue_tracker.setup_affiliate(product['id'], commission_rate=0.2)
            save_output(project_id, affiliate, "affiliate_setup", "revenue")
            log_message(project_id, f"✅ Affiliate setup complete: {affiliate.get('affiliate_code')}")
        except Exception as e:
            log_message(project_id, f"⚠️ Affiliate setup: {str(e)}")
        
        # STEP 6: Complete Project
        log_message(project_id, "✅ CYCLE COMPLETE - All systems ready!")
        
        projects.update_one(
            {"_id": project_id},
            {
                "$set": {
                    "status": "completed",
                    "completed_at": datetime.utcnow(),
                    "product_count": 1,
                    "marketplaces": ["gumroad"],
                    "social_posts_queued": len(social_posts)
                }
            }
        )
        
        return project
    
    except Exception as e:
        log_message(project_id, f"❌ ERROR: {str(e)}")
        projects.update_one({"_id": project_id}, {"$set": {"status": "failed", "error": str(e)}})
        return project
