from fastapi import APIRouter
from datetime import datetime
from ai_services.youtube_shorts_automator import YouTubeShortsAutomator
from ai_services.email_list_builder import EmailListBuilder
from ai_services.customer_support_ai import CustomerSupportAI
from ai_services.advanced_analytics import AdvancedAnalytics
from ai_services.competitor_analyzer import CompetitorAnalyzer
from ai_services.enterprise_scaler import EnterpriseScaler
from .models import outputs

router = APIRouter()

# Initialize services
youtube = YouTubeShortsAutomator()
email_builder = EmailListBuilder()
support_ai = CustomerSupportAI()
analytics = AdvancedAnalytics()
competitor = CompetitorAnalyzer()
enterprise = EnterpriseScaler()


# ===== YOUTUBE SHORTS AUTOMATION =====

@router.post("/youtube/generate-shorts/{product_id}")
async def generate_youtube_shorts(product_id: str, days: int = 30):
    """Generate 30 daily YouTube Shorts scripts"""
    product = outputs.find_one({"_id": product_id, "type": "product"})
    if not product:
        return {"error": "Product not found"}
    
    scripts = await youtube.generate_shorts_script(product.get("data", {}), days)
    
    return {
        "success": True,
        "total_shorts": len(scripts),
        "shorts_per_day": 1,
        "coverage_days": days,
        "duration_seconds": 60,
        "scripts_sample": scripts[:5]
    }


@router.post("/youtube/schedule-uploads/{product_id}")
async def schedule_youtube_uploads(product_id: str):
    """Schedule daily YouTube Shorts uploads"""
    product = outputs.find_one({"_id": product_id, "type": "product"})
    if not product:
        return {"error": "Product not found"}
    
    scripts = await youtube.generate_shorts_script(product.get("data", {}), 30)
    schedule = await youtube.schedule_daily_upload(scripts)
    
    return schedule


# ===== EMAIL LIST AUTOMATION =====

@router.post("/email/create-list/{product_id}")
async def create_email_list(product_id: str):
    """Create email list for product"""
    product = outputs.find_one({"_id": product_id, "type": "product"})
    if not product:
        return {"error": "Product not found"}
    
    email_list = await email_builder.create_email_list(product.get("data", {}))
    
    return email_list


@router.post("/email/generate-sequence/{product_id}")
async def generate_email_sequence(product_id: str, days: int = 30):
    """Generate 30-day email sequence"""
    product = outputs.find_one({"_id": product_id, "type": "product"})
    if not product:
        return {"error": "Product not found"}
    
    emails = await email_builder.generate_email_sequence(product.get("data", {}), days)
    
    return {
        "success": True,
        "total_emails": len(emails),
        "campaign_days": days,
        "emails": emails
    }


@router.post("/email/activate-sequence/{list_id}")
async def activate_email_sequence(list_id: str):
    """Activate automated email sequence"""
    # Mock implementation - would integrate with actual service
    return {
        "success": True,
        "list_id": list_id,
        "status": "active",
        "emails_scheduled": 8
    }


@router.get("/email/metrics/{list_id}")
async def get_email_metrics(list_id: str):
    """Get email campaign metrics"""
    return await email_builder.get_email_metrics(list_id)


# ===== CUSTOMER SUPPORT AI =====

@router.post("/support/create-bot/{product_id}")
async def create_support_bot(product_id: str):
    """Create AI support chatbot"""
    product = outputs.find_one({"_id": product_id, "type": "product"})
    if not product:
        return {"error": "Product not found"}
    
    bot = await support_ai.create_support_bot(product.get("data", {}))
    
    return bot


@router.post("/support/handle-message/{bot_id}")
async def handle_support_message(bot_id: str, message: str, customer_id: str = None):
    """Handle customer support message"""
    return await support_ai.handle_customer_message(bot_id, message, customer_id)


@router.get("/support/analytics/{bot_id}")
async def get_support_analytics(bot_id: str = None):
    """Get support bot analytics"""
    return await support_ai.get_support_analytics(bot_id)


@router.get("/support/help-articles/{product_id}")
async def get_help_articles(product_id: str):
    """Get auto-generated help articles"""
    product = outputs.find_one({"_id": product_id, "type": "product"})
    if not product:
        return {"error": "Product not found"}
    
    articles = await support_ai.create_help_articles(product.get("data", {}))
    
    return {"articles": articles}


# ===== ADVANCED ANALYTICS & A/B TESTING =====

@router.post("/analytics/ab-test/price/{product_id}")
async def ab_test_price(product_id: str, price_a: float, price_b: float):
    """A/B test different prices"""
    experiment = await analytics.run_price_ab_test(product_id, price_a, price_b)
    return experiment


@router.post("/analytics/ab-test/copy/{product_id}")
async def ab_test_copy(product_id: str, copy_a: str, copy_b: str):
    """A/B test different marketing copy"""
    experiment = await analytics.run_copy_ab_test(product_id, copy_a, copy_b)
    return experiment


@router.post("/analytics/ab-test/design/{product_id}")
async def ab_test_design(product_id: str, design_a: str, design_b: str):
    """A/B test different designs"""
    experiment = await analytics.run_design_ab_test(product_id, design_a, design_b)
    return experiment


@router.get("/analytics/test-results/{experiment_id}")
async def get_test_results(experiment_id: str):
    """Get A/B test results and winner"""
    return await analytics.get_test_results(experiment_id)


@router.get("/analytics/product/{product_id}")
async def get_product_analytics(product_id: str, days: int = 30):
    """Get comprehensive product analytics"""
    return await analytics.get_product_analytics(product_id, days)


@router.get("/analytics/funnel/{product_id}")
async def get_funnel_analytics(product_id: str):
    """Get conversion funnel analysis"""
    return await analytics.get_funnel_analytics(product_id)


@router.get("/analytics/cohorts/{product_id}")
async def get_cohort_analysis(product_id: str):
    """Get customer cohort analysis"""
    return await analytics.get_cohort_analysis(product_id)


# ===== COMPETITOR ANALYSIS =====

@router.get("/competitors/analyze/{competitor_name}")
async def analyze_competitor(competitor_name: str, url: str = None):
    """Analyze a specific competitor"""
    return await competitor.analyze_competitor(competitor_name, url)


@router.get("/competitors/market-gaps/{niche}")
async def find_market_gaps(niche: str):
    """Find underserved market segments"""
    return await competitor.find_market_gaps(niche)


@router.get("/competitors/sentiment/{competitor_name}")
async def get_customer_sentiment(competitor_name: str, source: str = "reviews"):
    """Analyze customer sentiment about competitor"""
    return await competitor.analyze_customer_sentiment(competitor_name, source)


@router.get("/competitors/underpriced-markets")
async def get_underpriced_markets():
    """Find underpriced market opportunities"""
    return await competitor.find_underpriced_markets()


@router.get("/competitors/intelligence/{niche}")
async def get_competitive_intelligence(niche: str):
    """Get full competitive landscape"""
    return await competitor.get_competitive_intelligence(niche)


# ===== ENTERPRISE SCALING =====

@router.post("/enterprise/enable-scaling")
async def enable_enterprise_scaling(
    projects_per_day: int = 50,
    concurrent_workers: int = 10,
    batch_size: int = 5
):
    """Enable enterprise-grade scaling"""
    config = {
        "projects_per_day": projects_per_day,
        "concurrent_workers": concurrent_workers,
        "batch_size": batch_size
    }
    return await enterprise.enable_enterprise_scaling(config)


@router.get("/enterprise/status")
async def get_enterprise_status():
    """Get enterprise scaling status"""
    return await enterprise.get_enterprise_status()


@router.post("/enterprise/run-cycle/{num_projects}")
async def run_enterprise_cycle(num_projects: int = 50):
    """Run large-scale autonomous cycles"""
    return await enterprise.run_enterprise_cycle(num_projects)


@router.get("/enterprise/performance")
async def get_enterprise_performance(days: int = 7):
    """Get enterprise performance metrics"""
    return await enterprise.get_performance_metrics(days)


# ===== HEALTH CHECK =====

@router.get("/health/level3")
def health_level3():
    return {
        "status": "healthy",
        "version": "LEVEL 3 - Enterprise",
        "services": [
            "youtube_shorts",
            "email_list_builder",
            "customer_support_ai",
            "advanced_analytics",
            "competitor_analyzer",
            "enterprise_scaler"
        ]
    }
