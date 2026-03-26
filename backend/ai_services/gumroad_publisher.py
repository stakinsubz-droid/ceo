"""
Gumroad Auto-Publisher
Automatically publishes products to Gumroad marketplace
"""
import os
from datetime import datetime
import requests
from typing import Dict, Any

GUMROAD_API_URL = "https://api.gumroad.com/v2"
GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN")


class GumroadPublisher:
    """Auto-publish products to Gumroad"""
    
    def __init__(self):
        self.token = GUMROAD_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    async def publish_ebook(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Publish eBook to Gumroad"""
        try:
            # Create product on Gumroad
            payload = {
                "name": product["title"],
                "description": product["description"],
                "price": product.get("price", 29.99),
                "content": product.get("content", ""),
                "file_name": f"{product['title'].replace(' ', '_')}.pdf",
                "is_published": True
            }
            
            response = requests.post(
                f"{GUMROAD_API_URL}/products",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "platform": "gumroad",
                    "product_id": data.get("product", {}).get("id"),
                    "url": data.get("product", {}).get("url"),
                    "published_at": datetime.utcnow().isoformat()
                }
            else:
                return {
                    "success": False,
                    "error": response.text
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def publish_course(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Publish course as bundle to Gumroad"""
        try:
            payload = {
                "name": product["title"],
                "description": product["description"],
                "price": product.get("price", 49.99),
                "is_published": True,
                "type": "bundle"
            }
            
            response = requests.post(
                f"{GUMROAD_API_URL}/products",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "platform": "gumroad",
                    "product_id": data.get("product", {}).get("id"),
                    "url": data.get("product", {}).get("url"),
                    "published_at": datetime.utcnow().isoformat()
                }
            else:
                return {"success": False, "error": response.text}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_sales(self, product_id: str) -> Dict[str, Any]:
        """Get sales data for product"""
        try:
            response = requests.get(
                f"{GUMROAD_API_URL}/products/{product_id}/sales",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "sales": response.json().get("sales", [])
                }
            return {"success": False}
        except Exception as e:
            return {"success": False, "error": str(e)}
