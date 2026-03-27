"""
Gumroad Auto-Publisher
Automatically publishes products to Gumroad marketplace

NOTE: Gumroad API v2 does NOT support product creation via API.
Products must be created manually via Gumroad dashboard.
This module helps manage existing products and track sales.
"""
import os
from datetime import datetime, timezone
import requests
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

GUMROAD_API_URL = "https://api.gumroad.com/v2"


class GumroadPublisher:
    """Gumroad integration for product management and sales tracking"""
    
    def __init__(self):
        self.access_token = os.environ.get("GUMROAD_ACCESS_TOKEN")
        
    async def publish_ebook(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate Gumroad product listing info.
        
        NOTE: Gumroad API does NOT support product creation.
        This generates a draft with instructions for manual upload.
        """
        if not self.access_token:
            return {"success": False, "error": "GUMROAD_ACCESS_TOKEN not configured"}
        
        # Generate product listing template for manual creation
        listing = {
            "success": True,
            "note": "Gumroad requires manual product creation via dashboard",
            "platform": "gumroad",
            "product_template": {
                "name": product.get("title", "Untitled Product"),
                "description": product.get("description", ""),
                "price": product.get("price", 9.99),
                "type": "ebook"
            },
            "instructions": [
                "1. Go to https://gumroad.com/products/new",
                "2. Copy the product details above",
                "3. Upload your product file",
                "4. Click Publish",
                "5. Come back here to track sales!"
            ],
            "dashboard_url": "https://gumroad.com/products/new",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        return listing
    
    async def publish_course(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Generate course listing template for Gumroad"""
        if not self.access_token:
            return {"success": False, "error": "GUMROAD_ACCESS_TOKEN not configured"}
        
        listing = {
            "success": True,
            "note": "Gumroad requires manual product creation via dashboard",
            "platform": "gumroad",
            "product_template": {
                "name": product.get("title", "Untitled Course"),
                "description": product.get("description", ""),
                "price": product.get("price", 49.99),
                "type": "course"
            },
            "instructions": [
                "1. Go to https://gumroad.com/products/new",
                "2. Copy the product details above",
                "3. Upload course content",
                "4. Click Publish",
                "5. Come back here to track sales!"
            ],
            "dashboard_url": "https://gumroad.com/products/new",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        return listing
    
    async def get_products(self) -> Dict[str, Any]:
        """Get all products from Gumroad account"""
        if not self.access_token:
            return {"success": False, "error": "GUMROAD_ACCESS_TOKEN not configured"}
            
        try:
            response = requests.get(
                f"{GUMROAD_API_URL}/products",
                params={"access_token": self.access_token}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return {
                        "success": True,
                        "products": data.get("products", [])
                    }
                return {"success": False, "error": data.get("message", "Unknown error")}
            return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_sales(self, product_id: str = None) -> Dict[str, Any]:
        """Get sales data from Gumroad"""
        if not self.access_token:
            return {"success": False, "error": "GUMROAD_ACCESS_TOKEN not configured"}
            
        try:
            params = {"access_token": self.access_token}
            if product_id:
                params["product_id"] = product_id
                
            response = requests.get(
                f"{GUMROAD_API_URL}/sales",
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return {
                        "success": True,
                        "sales": data.get("sales", [])
                    }
                return {"success": False, "error": data.get("message", "Unknown error")}
            return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_user(self) -> Dict[str, Any]:
        """Get Gumroad user/account info"""
        if not self.access_token:
            return {"success": False, "error": "GUMROAD_ACCESS_TOKEN not configured"}
            
        try:
            response = requests.get(
                f"{GUMROAD_API_URL}/user",
                params={"access_token": self.access_token}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return {
                        "success": True,
                        "user": data.get("user", {})
                    }
                return {"success": False, "error": data.get("message", "Unknown error")}
            return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
