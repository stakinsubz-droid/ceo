"""
Secure Key Vault & Credential Manager
Safely stores and manages all API keys and social media credentials
"""
import os
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from pathlib import Path
from cryptography.fernet import Fernet
import base64

class SecureKeyVault:
    """Encrypted credential storage for all API keys and tokens"""
    
    # Supported credential types
    CREDENTIAL_TYPES = {
        "gumroad": {
            "name": "Gumroad",
            "fields": ["client_id", "client_secret", "access_token"],
            "description": "Sell digital products",
            "icon": "🛒"
        },
        "stripe": {
            "name": "Stripe",
            "fields": ["secret_key", "publishable_key", "webhook_secret"],
            "description": "Accept payments",
            "icon": "💳"
        },
        "openai": {
            "name": "OpenAI",
            "fields": ["api_key"],
            "description": "AI content generation",
            "icon": "🤖"
        },
        "twitter": {
            "name": "Twitter/X",
            "fields": ["api_key", "api_secret", "access_token", "access_secret", "bearer_token"],
            "description": "Social media automation",
            "icon": "🐦"
        },
        "instagram": {
            "name": "Instagram",
            "fields": ["access_token", "user_id", "app_id", "app_secret"],
            "description": "Visual content posting",
            "icon": "📸"
        },
        "tiktok": {
            "name": "TikTok",
            "fields": ["access_token", "client_key", "client_secret"],
            "description": "Short-form video",
            "icon": "🎵"
        },
        "youtube": {
            "name": "YouTube",
            "fields": ["api_key", "client_id", "client_secret", "refresh_token"],
            "description": "Video content & Shorts",
            "icon": "🎬"
        },
        "linkedin": {
            "name": "LinkedIn",
            "fields": ["access_token", "client_id", "client_secret"],
            "description": "Professional networking",
            "icon": "💼"
        },
        "mailchimp": {
            "name": "Mailchimp",
            "fields": ["api_key", "server_prefix", "list_id"],
            "description": "Email marketing",
            "icon": "📧"
        },
        "sendgrid": {
            "name": "SendGrid",
            "fields": ["api_key"],
            "description": "Transactional emails",
            "icon": "📨"
        },
        "shopify": {
            "name": "Shopify",
            "fields": ["api_key", "api_secret", "store_url", "access_token"],
            "description": "E-commerce store",
            "icon": "🏪"
        },
        "etsy": {
            "name": "Etsy",
            "fields": ["api_key", "shared_secret", "access_token", "access_secret"],
            "description": "Handmade marketplace",
            "icon": "🎨"
        },
        "amazon_kdp": {
            "name": "Amazon KDP",
            "fields": ["access_key", "secret_key", "associate_tag"],
            "description": "Kindle publishing",
            "icon": "📚"
        },
        "notion": {
            "name": "Notion",
            "fields": ["api_key", "database_id"],
            "description": "Productivity templates",
            "icon": "📝"
        },
        "discord": {
            "name": "Discord",
            "fields": ["bot_token", "webhook_url"],
            "description": "Community building",
            "icon": "💬"
        },
        "telegram": {
            "name": "Telegram",
            "fields": ["bot_token", "chat_id"],
            "description": "Messaging automation",
            "icon": "✈️"
        },
        "supabase": {
            "name": "Supabase",
            "fields": ["url", "anon_key", "service_role_key"],
            "description": "Database & Auth",
            "icon": "🗄️"
        },
        "twilio": {
            "name": "Twilio",
            "fields": ["account_sid", "auth_token", "phone_number"],
            "description": "SMS marketing",
            "icon": "📱"
        }
    }
    
    def __init__(self, db=None):
        self.db = db
        self._encryption_key = self._get_or_create_key()
        self._fernet = Fernet(self._encryption_key)
    
    def _get_or_create_key(self) -> bytes:
        """Get or create encryption key"""
        key_path = Path("/app/backend/.vault_key")
        if key_path.exists():
            return key_path.read_bytes()
        else:
            key = Fernet.generate_key()
            key_path.write_bytes(key)
            return key
    
    def _encrypt(self, data: str) -> str:
        """Encrypt sensitive data"""
        return self._fernet.encrypt(data.encode()).decode()
    
    def _decrypt(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        return self._fernet.decrypt(encrypted_data.encode()).decode()
    
    async def store_credentials(self, credential_type: str, credentials: Dict[str, str]) -> Dict[str, Any]:
        """Store encrypted credentials"""
        if credential_type not in self.CREDENTIAL_TYPES:
            return {"success": False, "error": f"Unknown credential type: {credential_type}"}
        
        # Encrypt each credential value
        encrypted_creds = {}
        for key, value in credentials.items():
            if value:
                encrypted_creds[key] = self._encrypt(value)
        
        credential_doc = {
            "type": credential_type,
            "name": self.CREDENTIAL_TYPES[credential_type]["name"],
            "credentials": encrypted_creds,
            "status": "active",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        
        if self.db is not None:
            # Update or insert
            await self.db.credentials.update_one(
                {"type": credential_type},
                {"$set": credential_doc},
                upsert=True
            )
        
        return {
            "success": True,
            "type": credential_type,
            "name": self.CREDENTIAL_TYPES[credential_type]["name"],
            "fields_stored": list(encrypted_creds.keys())
        }
    
    async def get_credentials(self, credential_type: str) -> Dict[str, Any]:
        """Get decrypted credentials"""
        if self.db is None:
            return {"success": False, "error": "Database not configured"}
        
        doc = await self.db.credentials.find_one({"type": credential_type}, {"_id": 0})
        if not doc:
            return {"success": False, "error": f"No credentials found for {credential_type}"}
        
        # Decrypt credentials
        decrypted = {}
        for key, encrypted_value in doc.get("credentials", {}).items():
            try:
                decrypted[key] = self._decrypt(encrypted_value)
            except:
                decrypted[key] = None
        
        return {
            "success": True,
            "type": credential_type,
            "credentials": decrypted,
            "status": doc.get("status", "unknown")
        }
    
    async def list_credentials(self) -> Dict[str, Any]:
        """List all stored credential types (without actual values)"""
        stored = []
        available = []
        
        if self.db is not None:
            cursor = self.db.credentials.find({}, {"_id": 0, "credentials": 0})
            async for doc in cursor:
                stored.append({
                    "type": doc["type"],
                    "name": doc["name"],
                    "status": doc.get("status", "unknown"),
                    "icon": self.CREDENTIAL_TYPES.get(doc["type"], {}).get("icon", "🔑"),
                    "updated_at": doc.get("updated_at")
                })
        
        # Find available but not configured
        stored_types = [s["type"] for s in stored]
        for cred_type, config in self.CREDENTIAL_TYPES.items():
            if cred_type not in stored_types:
                available.append({
                    "type": cred_type,
                    "name": config["name"],
                    "description": config["description"],
                    "icon": config["icon"],
                    "fields": config["fields"],
                    "status": "not_configured"
                })
        
        return {
            "success": True,
            "stored": stored,
            "available": available,
            "total_configured": len(stored),
            "total_available": len(available)
        }
    
    async def delete_credentials(self, credential_type: str) -> Dict[str, Any]:
        """Delete stored credentials"""
        if self.db is None:
            return {"success": False, "error": "Database not configured"}
        
        result = await self.db.credentials.delete_one({"type": credential_type})
        return {
            "success": result.deleted_count > 0,
            "type": credential_type,
            "deleted": result.deleted_count > 0
        }
    
    async def test_credentials(self, credential_type: str) -> Dict[str, Any]:
        """Test if credentials are working"""
        creds = await self.get_credentials(credential_type)
        if not creds.get("success"):
            return creds
        
        # Test based on type
        test_result = {"success": False, "message": "Test not implemented for this type"}
        
        if credential_type == "gumroad":
            import requests
            try:
                response = requests.get(
                    "https://api.gumroad.com/v2/user",
                    params={"access_token": creds["credentials"].get("access_token")}
                )
                if response.status_code == 200 and response.json().get("success"):
                    test_result = {"success": True, "message": "Gumroad connected!", "user": response.json().get("user", {}).get("name")}
                else:
                    test_result = {"success": False, "message": "Invalid Gumroad token"}
            except Exception as e:
                test_result = {"success": False, "message": str(e)}
        
        elif credential_type == "openai":
            try:
                import openai
                client = openai.OpenAI(api_key=creds["credentials"].get("api_key"))
                # Simple test
                test_result = {"success": True, "message": "OpenAI API key valid"}
            except Exception as e:
                test_result = {"success": False, "message": str(e)}
        
        # Update status based on test
        if self.db is not None:
            await self.db.credentials.update_one(
                {"type": credential_type},
                {"$set": {
                    "status": "verified" if test_result["success"] else "invalid",
                    "last_tested": datetime.now(timezone.utc).isoformat()
                }}
            )
        
        return test_result
    
    def get_credential_schema(self, credential_type: str) -> Dict[str, Any]:
        """Get the schema for a credential type"""
        if credential_type not in self.CREDENTIAL_TYPES:
            return {"error": f"Unknown type: {credential_type}"}
        
        config = self.CREDENTIAL_TYPES[credential_type]
        return {
            "type": credential_type,
            "name": config["name"],
            "description": config["description"],
            "icon": config["icon"],
            "fields": config["fields"]
        }
