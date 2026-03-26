from fastapi import APIRouter
from .models import projects, outputs, logs
from .autonomous_engine import run_autonomous_cycle, get_project_details
from ai_services.gumroad_publisher import GumroadPublisher
from ai_services.social_media_scheduler import SocialMediaAutoPoster
from ai_services.revenue_tracker import RevenueTracker
from ai_services.scaling_engine import ScalingEngine
from ai_services.self_improving_loop import SelfImprovingLoop

router = APIRouter()

# Initialize services
gumroad = GumroadPublisher()
social_poster = SocialMediaAutoPoster()
revenue = RevenueTracker()
scaler = ScalingEngine()
improver = SelfImprovingLoop()


# ===== ORIGINAL ENDPOINTS =====

@router.get("/projects")
def get_projects():
    return list(projects.find({}, {"_id": 1, "name": 1, "status": 1}))


@router.get("/projects/{project_id}")
def get_project(project_id: str):
    return get_project_details(project_id)


@router.post("/run")
def run():
    project = run_autonomous_cycle()
    return {"status": "started", "project_id": project["_id"]}


# ===== LEVEL 2: MARKETPLACE =====

@router.post("/publish/gumroad/{product_id}")
async def publish_to_gumroad(product_id: str):
    """Publish product to Gumroad marketplace"""
    product = outputs.find_one({"_id": product_id, "type": "product"})
    if not product:
        return {"error": "Product not found"}
    
    result = await gumroad.publish_ebook(product.get("data", {}))
    
    # Save result
    outputs.insert_one({
        "project_id": product.get("project_id"),
        "type": "marketplace_publish",
        "data": result,
        "agent": "gumroad",
        "created_at": datetime.utcnow()
    })
    
    return result


# ===== LEVEL 2: SOCIAL MEDIA =====

@router.post("/social/generate/{product_id}")
async def generate_social_content(product_id: str, days: int = 90):
    """Generate 6-month social media content calendar"""
    product = outputs.find_one({"_id": product_id, "type": "product"})
    if not product:
        return {"error": "Product not found"}
    
    posts = await social_poster.generate_social_posts(product.get("data", {}), days)
    
    # Save schedule
    outputs.insert_one({
        "project_id": product.get("project_id"),
        "type": "social_schedule",
        "data": {"total_posts": len(posts), "posts": posts},
        "agent": "social_media",
        "created_at": datetime.utcnow()
    })
    
    return {
        "success": True,
        "total_posts": len(posts),
        "coverage_days": days,
        "platforms": ["tiktok", "instagram", "twitter"]
    }


@router.get("/social/schedule/{project_id}")
def get_social_schedule(project_id: str):
    """Get scheduled social posts"""
    schedule = outputs.find_one({"project_id": project_id, "type": "social_schedule"})
    return schedule.get("data", {}) if schedule else {"error": "No schedule found"}


# ===== LEVEL 2: REVENUE =====

@router.post("/revenue/record/{product_id}")
async def record_sale(product_id: str, amount: float, source: str):
    """Record a product sale"""
    result = await revenue.record_sale(product_id, amount, source)
    return result


@router.get("/revenue/metrics/{product_id}")
async def get_metrics(product_id: str, days: int = 30):
    """Get revenue metrics for product"""
    return await revenue.get_revenue_metrics(product_id, days)


@router.get("/revenue/all-metrics")
async def get_all_metrics(days: int = 30):
    """Get all revenue metrics"""
    return await revenue.get_revenue_metrics(None, days)


@router.get("/revenue/optimize/{product_id}")
async def get_price_optimization(product_id: str):
    """Get pricing optimization recommendation"""
    return await revenue.optimize_pricing(product_id)


@router.post("/affiliate/setup/{product_id}")
async def setup_affiliate(product_id: str, commission_rate: float = 0.2):
    """Setup affiliate program"""
    return await revenue.setup_affiliate(product_id, commission_rate)


@router.get("/revenue/leaderboard")
async def get_leaderboard(limit: int = 10):
    """Get top products by revenue"""
    return await revenue.get_leaderboard(limit)


# ===== LEVEL 2: SCALING =====

@router.post("/scale/configure")
async def configure_scaling(projects_per_day: int = 5):
    """Configure scaling to run N projects per day"""
    return await scaler.scale_up(projects_per_day)


@router.get("/scale/status")
async def get_scaling_status():
    """Get scaling configuration and status"""
    return await scaler.get_scaling_status()


@router.post("/scale/schedule/{num_projects}")
async def schedule_projects(num_projects: int):
    """Schedule N projects across the day"""
    schedule = await scaler.schedule_projects(num_projects)
    return {"schedule": schedule}


@router.post("/scale/run-parallel")
async def run_parallel_projects(num_projects: int = 5):
    """Run multiple projects in parallel"""
    projects_list = await scaler.schedule_projects(num_projects)
    results = await scaler.run_parallel_projects(projects_list)
    return results


# ===== LEVEL 2: SELF-IMPROVEMENT =====

@router.get("/improve/analysis")
async def get_performance_analysis():
    """Analyze AI performance and get insights"""
    return await improver.analyze_performance()


@router.get("/improve/recommendations")
async def get_recommendations():
    """Get optimization recommendations"""
    return await improver.recommend_optimizations()


@router.post("/improve/apply")
async def apply_optimization(optimization: str):
    """Apply a specific optimization"""
    return await improver.apply_learning({"optimization": optimization})


@router.get("/improve/metrics")
async def get_improvement_metrics():
    """Get improvement trends over time"""
    return await improver.get_improvement_metrics()


# ===== HEALTH CHECK =====

@router.get("/health")
def health():
    return {
        "status": "healthy",
        "services": [
            "gumroad_publisher",
            "social_media_scheduler",
            "revenue_tracker",
            "scaling_engine",
            "self_improving_loop"
        ]
    }


from datetime import datetime
