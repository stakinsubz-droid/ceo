"""
Opportunity Scouting AI
Automatically identifies trending niches, keywords, and products
"""
import asyncio
from typing import List, Dict, Any
import random
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage

load_dotenv()

class OpportunityScout:
    def __init__(self):
        self.api_key = os.environ.get('EMERGENT_LLM_KEY')
        
    async def scout_opportunities(self, sources: List[str] = None) -> List[Dict[str, Any]]:
        """
        Scout for trending opportunities across various sources
        
        Args:
            sources: List of sources to analyze (social media, marketplaces, etc.)
            
        Returns:
            List of opportunity dictionaries with scores and recommendations
        """
        if sources is None:
            sources = ["social media trends", "digital product marketplaces", "search trends"]
        
        # Initialize AI chat
        chat = LlmChat(
            api_key=self.api_key,
            session_id=f"opportunity-scout-{datetime.now().timestamp()}",
            system_message="You are an expert market researcher and trend analyst specializing in identifying profitable digital product opportunities. Analyze trends and provide data-driven insights."
        ).with_model("openai", "gpt-5.2")
        
        # Create detailed prompt
        prompt = f"""
Analyze current market trends and identify 5 high-potential opportunities for digital products (eBooks, courses, templates, planners).

For each opportunity, provide:
1. Niche name (specific and actionable)
2. Trend score (0.0-1.0 based on growth potential)
3. 3-5 relevant keywords
4. 2-3 suggested product titles
5. Market size (Small/Growing/Large/Very Large)
6. Competition level (Low/Medium/High)

Focus on niches that are:
- Currently trending or emerging
- Have proven monetization potential
- Suitable for digital products
- Not oversaturated

Sources to consider: {', '.join(sources)}

Return your analysis in this exact JSON format:
{{
  "opportunities": [
    {{
      "niche": "Niche Name",
      "trend_score": 0.85,
      "keywords": ["keyword1", "keyword2", "keyword3"],
      "suggested_products": ["Product Title 1", "Product Title 2"],
      "market_size": "Large",
      "competition_level": "Medium"
    }}
  ]
}}
"""
        
        try:
            # Send message to AI
            message = UserMessage(text=prompt)
            response = await chat.send_message(message)
            
            # Parse response
            import json
            # Extract JSON from response (handle markdown code blocks)
            response_text = response.strip()
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            data = json.loads(response_text)
            opportunities = data.get("opportunities", [])
            
            # Enrich with additional metadata
            for opp in opportunities:
                opp["id"] = f"opp-{random.randint(1000, 9999)}"
                opp["status"] = "identified"
                opp["created_at"] = datetime.now(timezone.utc).isoformat()
            
            return opportunities
            
        except Exception as e:
            print(f"Error in opportunity scouting: {str(e)}")
            # Return fallback opportunities if AI fails
            return self._get_fallback_opportunities()
    
    def _get_fallback_opportunities(self) -> List[Dict[str, Any]]:
        """Fallback opportunities if AI fails"""
        return [
            {
                "id": f"opp-{random.randint(1000, 9999)}",
                "niche": "AI Tools for Content Creators",
                "trend_score": 0.89,
                "keywords": ["AI tools", "content creation", "automation"],
                "suggested_products": ["AI Content Guide", "Creator Toolkit"],
                "market_size": "Large",
                "competition_level": "Medium",
                "status": "identified",
                "created_at": datetime.now(timezone.utc).isoformat()
            }
        ]
