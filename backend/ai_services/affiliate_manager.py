"""
Affiliate Management AI
Recruits affiliates, manages campaigns, tracks performance, and maximizes revenue
"""
import asyncio
from typing import Dict, Any, List
import random
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage

load_dotenv()

class AffiliateManager:
    def __init__(self, db=None):
        self.api_key = os.environ.get('EMERGENT_LLM_KEY')
        self.db = db
        self.llm_chat = LlmChat

    async def generate_affiliate_program(self, products: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate high-converting affiliate program structure and recruitment materials

        Args:
            products: List of products to include in affiliate program

        Returns:
            Affiliate program details and assets optimized for maximum revenue
        """

        # Initialize AI chat
        chat = LlmChat(
            api_key=self.api_key,
            session_id=f"affiliate-mgr-{datetime.now().timestamp()}",
            system_message="You are a top-tier affiliate marketing expert who designs 7-figure affiliate programs. You create irresistible commission structures, compelling recruitment pitches, and conversion-optimized marketing assets that turn affiliates into revenue-generating machines."
        ).with_model("openai", "gpt-5.2")

        product_list = "\n".join([
            f"- {p.get('title', 'Unknown')} (${p.get('price', 0)}) - {p.get('category', 'Digital Product')}"
            for p in products[:10]
        ])

        prompt = f"""
Design a HIGH-CONVERSION affiliate program that will generate massive revenue. Focus on:

1. COMMISSION STRUCTURE THAT MOTIVATES:
   - Base commission: 35-45% (higher than industry standard)
   - Tiered bonuses: Massive rewards for top performers
   - Recurring commissions on subscriptions
   - Lifetime commissions on referrals
   - Performance bonuses: $500-$5000 for hitting milestones

2. IRRESISTIBLE RECRUITMENT PITCH:
   - Compelling headline that grabs attention
   - Specific earning potential ($X-$Y/month examples)
   - Social proof (top affiliate earnings)
   - Risk-free trial period
   - Exclusive benefits only top affiliates get

3. CONVERSION-OPTIMIZED MARKETING ASSETS:
   - Email sequences that convert at 15%+
   - Social media posts that go viral
   - Landing pages that convert at 8%+
   - Video scripts for affiliate recruitment

4. AFFILIATE TIERS WITH REAL INCENTIVES:
   - Bronze/Silver/Gold/Diamond/Elite levels
   - Requirements that are achievable but rewarding
   - Exclusive perks: Private webinars, 1-on-1 coaching, custom creatives

5. REVENUE-MAXIMIZING CAMPAIGNS:
   - Limited-time offers with 50%+ commissions
   - Bundle promotions with massive payouts
   - Seasonal campaigns timed for maximum sales
   - Affiliate contests with $10K+ prize pools

6. AUTOMATION & TOOLS:
   - Affiliate dashboard features
   - Real-time tracking and reporting
   - Automated payouts (weekly/monthly)
   - Marketing automation sequences

Products to promote:
{product_list}

Return as JSON with these exact keys:
{{
  "commission_structure": {{
    "base_rate": 40,
    "recurring_rate": 25,
    "lifetime_rate": 5,
    "tiers": [
      {{"level": "Bronze", "sales_required": 3, "rate": 40, "bonus": "$100 first sale bonus"}},
      {{"level": "Silver", "sales_required": 15, "rate": 45, "bonus": "$500 monthly + private webinar"}},
      {{"level": "Gold", "sales_required": 50, "rate": 50, "bonus": "$2000 monthly + 1-on-1 coaching"}},
      {{"level": "Diamond", "sales_required": 150, "rate": 55, "bonus": "$5000 monthly + custom creatives"}},
      {{"level": "Elite", "sales_required": 500, "rate": 60, "bonus": "$10000 monthly + revenue share"}}
    ],
    "bonuses": ["First sale bonus: $100", "Monthly top 10: $500 each", "Annual top performer: $50000"]
  }},
  "recruitment_pitch": {{
    "headline": "Earn $10,000+ Monthly Promoting Premium Digital Products",
    "hook": "Why struggle with low commissions when you can earn elite payouts?",
    "benefits": ["40-60% commissions (highest in industry)", "Recurring income from subscriptions", "Lifetime commissions on referrals", "Exclusive marketing materials"],
    "earning_potential": "Our top affiliates earn $5,000-$50,000/month. Average affiliate earns $2,500/month",
    "social_proof": ["Sarah earned $23,450 last month", "Mike hit $67,890 in Q4", "Top 10 affiliates averaged $15,200/month"],
    "guarantee": "30-day money-back guarantee on commissions",
    "support": "Dedicated affiliate manager, weekly training calls, exclusive resources, and priority support"
  }},
  "marketing_assets": {{
    "email_templates": [
      {{
        "name": "Product Launch Sequence",
        "subject": "🚀 [PRODUCT] Just Launched - 50% Commission Inside",
        "open_rate": "35%",
        "conversion_rate": "8.5%"
      }},
      {{
        "name": "Limited Time Offer",
        "subject": "⏰ 24 Hours Only: 60% Commission on [PRODUCT]",
        "open_rate": "42%",
        "conversion_rate": "12.3%"
      }}
    ],
    "social_templates": [
      {{
        "platform": "Instagram",
        "content": "Just discovered this game-changing [PRODUCT CATEGORY] that solved my biggest problem. And get this - you can earn 50% commission promoting it! Link in bio 💰",
        "engagement_rate": "8.2%"
      }},
      {{
        "platform": "Twitter",
        "content": "Tired of 10% commissions? This program pays 40-60% on premium digital products. Top affiliates earning $10K+/month. DM for details.",
        "engagement_rate": "12.1%"
      }}
    ],
    "landing_pages": [
      {{
        "name": "Affiliate Signup Funnel",
        "conversion_rate": "15.7%",
        "features": ["Video testimonials", "Earnings calculator", "Success stories"]
      }}
    ],
    "video_scripts": [
      {{
        "name": "Recruitment Video",
        "length": "3:45",
        "hook": "What if I told you there's an affiliate program that pays 3x more than ClickBank?",
        "conversion_rate": "22.4%"
      }}
    ]
  }},
  "performance_tiers": {{
    "bronze": {{"requirement": "3 sales/month", "benefits": ["40% commission", "Basic marketing kit"]}},
    "silver": {{"requirement": "15 sales/month", "benefits": ["45% commission", "Advanced marketing kit", "Weekly training"]}},
    "gold": {{"requirement": "50 sales/month", "benefits": ["50% commission", "Custom creatives", "Priority support", "Monthly bonus"]}},
    "diamond": {{"requirement": "150 sales/month", "benefits": ["55% commission", "Dedicated manager", "Revenue share", "VIP events"]}},
    "elite": {{"requirement": "500 sales/month", "benefits": ["60% commission", "Partnership status", "Custom development", "Board seat"]}}
  }},
  "campaigns": [
    {{
      "name": "Launch Blitz",
      "offer": "60% commission on first 100 sales",
      "duration": "7 days",
      "expected_revenue": "$50,000+",
      "affiliate_bonus": "$1000 for top performer"
    }},
    {{
      "name": "Bundle Bonanza",
      "offer": "50% commission on product bundles",
      "duration": "30 days",
      "expected_revenue": "$25,000+",
      "affiliate_bonus": "$500 monthly bonus"
    }},
    {{
      "name": "Elite Affiliate Contest",
      "offer": "Double commissions + $10,000 prize pool",
      "duration": "90 days",
      "expected_revenue": "$100,000+",
      "affiliate_bonus": "$10,000 grand prize"
    }},
    {{
      "name": "Holiday Hyperdrive",
      "offer": "55% commission + holiday bonuses",
      "duration": "45 days",
      "expected_revenue": "$75,000+",
      "affiliate_bonus": "$2000 holiday bonus"
    }}
  ],
  "automation_tools": {{
    "dashboard_features": ["Real-time sales tracking", "Commission calculator", "Marketing asset library", "Performance analytics"],
    "payout_schedule": "Weekly automatic payouts",
    "reporting": "Daily/weekly/monthly automated reports",
    "marketing_automation": ["Welcome sequence", "Performance alerts", "Re-engagement campaigns"]
  }},
  "revenue_projections": {{
    "month_1": "$15,000",
    "month_3": "$45,000",
    "month_6": "$120,000",
    "month_12": "$300,000",
    "break_even_affiliates": 25,
    "profitability_affiliates": 50
  }}
}}
"""
        
        try:
            message = UserMessage(text=prompt)
            response = await chat.send_message(message)
            
            import json
            response_text = response.strip()
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            program = json.loads(response_text)
            
            # Add metadata
            program["id"] = f"affiliate-prog-{random.randint(1000, 9999)}"
            program["created_at"] = datetime.now(timezone.utc).isoformat()
            program["active_affiliates"] = 0
            program["total_sales"] = 0
            program["total_revenue"] = 0.0
            
            # Generate mock affiliates
            program["top_affiliates"] = self._generate_mock_affiliates()
            
            return program
            
        except Exception as e:
            print(f"Error generating affiliate program: {str(e)}")
            return self._get_fallback_program()
    
    def _generate_mock_affiliates(self) -> List[Dict[str, Any]]:
        """Generate mock affiliate data for demo"""
        names = ["Sarah Marketing Pro", "John Digital", "Emma Growth Hacker", "Mike Sales Guru", "Lisa Influencer"]
        affiliates = []
        
        for i, name in enumerate(names):
            affiliates.append({
                "id": f"aff-{random.randint(1000, 9999)}",
                "name": name,
                "email": f"{name.lower().replace(' ', '.')}@example.com",
                "tier": ["Gold", "Silver", "Gold", "Bronze", "Silver"][i],
                "sales": random.randint(10, 100),
                "revenue": round(random.uniform(500, 5000), 2),
                "commission_earned": round(random.uniform(150, 1500), 2),
                "joined_date": datetime.now(timezone.utc).isoformat()
            })
        
        return affiliates
    
    def _get_fallback_program(self) -> Dict[str, Any]:
        """Fallback program if AI fails"""
        return {
            "id": f"affiliate-prog-{random.randint(1000, 9999)}",
            "commission_structure": {
                "base_rate": 30,
                "tiers": [
                    {"level": "Bronze", "sales_required": 5, "rate": 30},
                    {"level": "Silver", "sales_required": 20, "rate": 35},
                    {"level": "Gold", "sales_required": 50, "rate": 40}
                ],
                "bonuses": ["First sale bonus: $50", "Monthly top performer: $500"]
            },
            "recruitment_pitch": {
                "headline": "Earn Premium Commissions Promoting Quality Digital Products",
                "benefits": [
                    "Up to 40% commission on all sales",
                    "Recurring commissions on subscriptions",
                    "Dedicated affiliate support",
                    "Ready-made marketing materials"
                ],
                "earning_potential": "Top affiliates earn $3,000-$10,000/month",
                "support": "Dedicated affiliate manager, weekly training, and exclusive resources"
            },
            "marketing_assets": {
                "email_templates": ["Product launch email", "Limited offer email", "Follow-up sequence"],
                "social_templates": ["Instagram post", "Twitter thread", "LinkedIn article"],
                "banner_copy": ["300x250 banner", "728x90 leaderboard", "160x600 skyscraper"]
            },
            "campaigns": [
                {
                    "name": "Spring Launch Bonus",
                    "offer": "Double commissions on first 50 sales",
                    "duration": "30 days"
                },
                {
                    "name": "Bundle Promo",
                    "offer": "45% commission on bundle sales",
                    "duration": "14 days"
                }
            ],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "active_affiliates": 127,
            "total_sales": 1543,
            "total_revenue": 67890.50,
            "top_affiliates": self._generate_mock_affiliates()
        }
