"""
Publishing Engine (safe staggered publish)
"""
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from .marketplace_integrations import MarketplaceIntegrations
from .safety_layer import SafetyLayer

class PublishingEngine:
    def __init__(self, db=None):
        self.marketplace = MarketplaceIntegrations()
        self.safety = SafetyLayer()
        self.db = db

    async def schedule_publish(self, product: Dict[str, Any], marketplaces: List[str]) -> List[Dict[str, Any]]:
        """Queue and schedule products for staggered publishing."""
        results = []
        for platform in marketplaces:
            allowed = await self.safety.enforce_daily_publication_limit(platform)
            if not allowed:
                results.append({"marketplace": platform, "status": "skipped", "reason": "daily limit reached"})
                continue

            tos = await self.safety.check_platform_tos(product, platform)
            if tos.get("status") != "passed":
                results.append({"marketplace": platform, "status": "rejected", "reason": tos.get("reason")})
                continue

            try:
                listing = await self.marketplace.publish_to_marketplace(product, platform)
                results.append(listing)
            except Exception as e:
                results.append({"marketplace": platform, "status": "error", "reason": str(e)})

            await asyncio.sleep(1)

        return results

    async def queue_product_for_publishing(self, product: Dict[str, Any], marketplaces: List[str], scheduled_time=None, priority="MEDIUM") -> Dict[str, Any]:
        item = {
            "product_id": product.get("id"),
            "platforms": marketplaces,
            "scheduled_time": (scheduled_time or datetime.now(timezone.utc).isoformat()),
            "status": "queued",
            "priority": priority,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        if self.db is not None:
            await self.db.publishing_queue.insert_one(item)
        return item

    async def process_queue(self):
        """Process an active queue from DB."""
        if self.db is None:
            return []

        now_iso = datetime.now(timezone.utc).isoformat()
        entries = await self.db.publishing_queue.find({"status": "queued", "scheduled_time": {"$lte": now_iso}}).sort([("priority", -1), ("scheduled_time", 1)]).to_list(100)
        results = []

        for entry in entries:
            product = await self.db.products.find_one({"id": entry["product_id"]})
            if not product:
                await self.db.publishing_queue.update_one({"_id": entry["_id"]}, {"$set": {"status": "failed", "updated_at": datetime.now(timezone.utc).isoformat(), "error": "Product not found"}})
                continue

            platform_results = []
            for platform in entry.get("platforms", []):
                try:
                    listing = await self.marketplace.publish_to_marketplace(product, platform)
                    platform_results.append(listing)
                except Exception as e:
                    platform_results.append({"marketplace": platform, "status": "error", "reason": str(e)})

            await self.db.publishing_queue.update_one({"_id": entry["_id"]}, {"$set": {"status": "completed", "updated_at": datetime.now(timezone.utc).isoformat(), "results": platform_results}})
            results.append({"product_id": entry["product_id"], "platform_results": platform_results})

        return results

