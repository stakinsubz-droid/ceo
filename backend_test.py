#!/usr/bin/env python3
"""
CEO System Backend API Testing Suite
Tests all critical endpoints for the autonomous AI company generation platform
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, List

class CEOSystemTester:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.api_base = f"{self.base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})

    def log_test(self, name: str, success: bool, details: str = ""):
        """Log test result"""
        self.tests_run += 1
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
        if details:
            print(f"    {details}")
        
        if success:
            self.tests_passed += 1
        else:
            self.failed_tests.append({"test": name, "details": details})

    def test_endpoint(self, method: str, endpoint: str, expected_status: int = 200, 
                     data: Dict = None, test_name: str = None) -> tuple:
        """Generic endpoint tester"""
        if not test_name:
            test_name = f"{method} {endpoint}"
        
        url = f"{self.api_base}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data)
            else:
                raise ValueError(f"Unsupported method: {method}")

            success = response.status_code == expected_status
            
            if success:
                try:
                    response_data = response.json()
                    self.log_test(test_name, True, f"Status: {response.status_code}")
                    return True, response_data
                except json.JSONDecodeError:
                    self.log_test(test_name, True, f"Status: {response.status_code} (No JSON response)")
                    return True, {}
            else:
                error_msg = f"Expected {expected_status}, got {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f" - {error_detail.get('detail', 'No error detail')}"
                except:
                    error_msg += f" - Response: {response.text[:200]}"
                
                self.log_test(test_name, False, error_msg)
                return False, {}

        except requests.exceptions.RequestException as e:
            self.log_test(test_name, False, f"Request failed: {str(e)}")
            return False, {}

    def test_system_health(self):
        """Test system health endpoint"""
        print("\n🏥 Testing System Health...")
        success, data = self.test_endpoint('GET', '/system/health', test_name="System Health Check")
        
        if success and data:
            # Verify health response structure
            required_fields = ['status', 'timestamp', 'services']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                self.log_test("Health Response Structure", False, f"Missing fields: {missing_fields}")
            else:
                self.log_test("Health Response Structure", True, f"Status: {data.get('status')}")
                
                # Check services status
                services = data.get('services', {})
                for service, status in services.items():
                    service_ok = status in ['connected', 'operational', 'unavailable (demo mode)']
                    self.log_test(f"Service: {service}", service_ok, f"Status: {status}")

    def test_dashboard_stats(self):
        """Test dashboard statistics endpoint"""
        print("\n📊 Testing Dashboard Stats...")
        success, data = self.test_endpoint('GET', '/dashboard/stats', test_name="Dashboard Stats")
        
        if success and data:
            # Verify stats structure
            required_fields = ['total_products', 'products_today', 'total_revenue', 
                             'revenue_today', 'pending_tasks', 'active_opportunities']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                self.log_test("Stats Response Structure", False, f"Missing fields: {missing_fields}")
            else:
                self.log_test("Stats Response Structure", True, 
                            f"Products: {data.get('total_products')}, Revenue: ${data.get('total_revenue', 0):.2f}")

    def test_products_endpoints(self):
        """Test products CRUD operations"""
        print("\n📦 Testing Products Endpoints...")
        
        # Test GET products
        success, products = self.test_endpoint('GET', '/products?limit=10', test_name="Get Products List")
        
        if success:
            self.log_test("Products List Type", isinstance(products, list), 
                         f"Returned {len(products)} products")
        
        # Test create product
        product_data = {
            "title": "Test Product",
            "description": "A test product for API testing",
            "product_type": "ebook",
            "price": 19.99,
            "tags": ["test", "api"]
        }
        
        success, created_product = self.test_endpoint('POST', '/products', 201, product_data, 
                                                    "Create Product")
        
        if success and created_product:
            product_id = created_product.get('id')
            if product_id:
                # Test get specific product
                self.test_endpoint('GET', f'/products/{product_id}', test_name="Get Specific Product")
                
                # Test update product status
                self.test_endpoint('PUT', f'/products/{product_id}/status?status=published', 
                                 test_name="Update Product Status")

    def test_opportunities_endpoints(self):
        """Test opportunities endpoints"""
        print("\n🔍 Testing Opportunities Endpoints...")
        
        # Test GET opportunities
        success, opportunities = self.test_endpoint('GET', '/opportunities?limit=5', 
                                                  test_name="Get Opportunities List")
        
        if success:
            self.log_test("Opportunities List Type", isinstance(opportunities, list), 
                         f"Returned {len(opportunities)} opportunities")

    def test_ai_scout_opportunities(self):
        """Test AI opportunity scouting"""
        print("\n🤖 Testing AI Scout Opportunities...")
        
        success, data = self.test_endpoint('POST', '/ai/scout-opportunities', 
                                         test_name="AI Scout Opportunities")
        
        if success and data:
            expected_fields = ['success', 'task_id', 'opportunities_found']
            missing_fields = [field for field in expected_fields if field not in data]
            
            if missing_fields:
                self.log_test("Scout Response Structure", False, f"Missing fields: {missing_fields}")
            else:
                self.log_test("Scout Response Structure", True, 
                            f"Found {data.get('opportunities_found')} opportunities")

    def test_ai_generate_book(self):
        """Test AI book generation"""
        print("\n📚 Testing AI Book Generation...")
        
        book_request = {
            "niche": "productivity",
            "keywords": ["productivity", "efficiency", "time management"],
            "book_length": "medium",
            "target_audience": "professionals"
        }
        
        success, data = self.test_endpoint('POST', '/ai/generate-book', 200, book_request,
                                         "AI Generate Book")
        
        if success and data:
            expected_fields = ['success', 'task_id', 'product']
            missing_fields = [field for field in expected_fields if field not in data]
            
            if missing_fields:
                self.log_test("Book Generation Response", False, f"Missing fields: {missing_fields}")
            else:
                product = data.get('product', {})
                self.log_test("Book Generation Response", True, 
                            f"Created: {product.get('title', 'Unknown')}")

    def test_ai_optimize_revenue(self):
        """Test AI revenue optimization"""
        print("\n💰 Testing AI Revenue Optimization...")
        
        success, data = self.test_endpoint('POST', '/ai/optimize-revenue', 
                                         test_name="AI Revenue Optimization")
        
        if success and data:
            if 'recommendations' in data:
                self.log_test("Revenue Optimization Response", True, "Recommendations generated")
            else:
                self.log_test("Revenue Optimization Response", False, "No recommendations in response")

    def test_ai_affiliate_program(self):
        """Test AI affiliate program generation"""
        print("\n🤝 Testing AI Affiliate Program...")
        
        success, data = self.test_endpoint('POST', '/ai/generate-affiliate-program', 
                                         test_name="AI Generate Affiliate Program")
        
        if success and data:
            if 'program' in data:
                self.log_test("Affiliate Program Response", True, "Program generated")
            else:
                self.log_test("Affiliate Program Response", False, "No program in response")

    def test_analytics_insights(self):
        """Test analytics insights endpoint"""
        print("\n📈 Testing Analytics Insights...")
        
        success, data = self.test_endpoint('GET', '/analytics/insights', 
                                         test_name="Analytics Insights")
        
        if success and data:
            if 'insights' in data:
                insights = data['insights']
                has_kpis = 'kpis' in insights
                has_forecast = 'revenue_forecast' in insights
                has_recommendations = 'recommendations' in insights
                
                self.log_test("Analytics Insights Structure", 
                            has_kpis and has_forecast and has_recommendations,
                            f"KPIs: {has_kpis}, Forecast: {has_forecast}, Recommendations: {has_recommendations}")
            else:
                self.log_test("Analytics Insights Response", False, "No insights in response")

    def test_launch_product_one_click(self):
        """Test the new Launch Product One-Click endpoint"""
        print("\n🚀 Testing Launch Product One-Click...")
        
        launch_request = {
            "niche": "productivity",
            "product_type": "ebook",
            "auto_publish": True,
            "generate_social": True
        }
        
        success, data = self.test_endpoint('POST', '/launch-product', 200, launch_request,
                                         "Launch Product One-Click")
        
        if success and data:
            expected_fields = ['success', 'stages', 'product']
            missing_fields = [field for field in expected_fields if field not in data]
            
            if missing_fields:
                self.log_test("Launch Product Response", False, f"Missing fields: {missing_fields}")
            else:
                stages = data.get('stages', {})
                product = data.get('product', {})
                self.log_test("Launch Product Response", True, 
                            f"Success: {data.get('success')}, Product: {product.get('title', 'Unknown')}")
                
                # Check individual stages
                for stage_name in ['scout', 'generate', 'publish']:
                    if stage_name in stages:
                        stage_success = stages[stage_name].get('success', False)
                        self.log_test(f"Launch Stage: {stage_name}", stage_success, 
                                    f"Stage completed: {stage_success}")

    def test_gumroad_integration(self):
        """Test Gumroad integration endpoints"""
        print("\n🛒 Testing Gumroad Integration...")
        
        # Test get Gumroad products
        success, data = self.test_endpoint('GET', '/gumroad/products', 
                                         test_name="Get Gumroad Products")
        
        if success and data:
            if 'success' in data:
                self.log_test("Gumroad Products Response", data.get('success'), 
                            f"Connected: {data.get('success')}")
            
        # Test get Gumroad sales
        success, data = self.test_endpoint('GET', '/gumroad/sales', 
                                         test_name="Get Gumroad Sales")
        
        if success and data:
            if 'success' in data:
                self.log_test("Gumroad Sales Response", data.get('success'), 
                            f"Sales data available: {data.get('success')}")

    def test_youtube_shorts_generation(self):
        """Test YouTube Shorts script generation"""
        print("\n🎬 Testing YouTube Shorts Generation...")
        
        # First create a test product to use
        product_data = {
            "title": "Test Product for Shorts",
            "description": "A test product for YouTube Shorts generation",
            "product_type": "ebook",
            "price": 19.99
        }
        
        success, created_product = self.test_endpoint('POST', '/products', 201, product_data, 
                                                    "Create Product for Shorts Test")
        
        if success and created_product:
            product_id = created_product.get('id')
            if product_id:
                shorts_request = {
                    "product_id": product_id,
                    "num_scripts": 3
                }
                
                success, data = self.test_endpoint('POST', '/social/youtube-shorts', 200, 
                                                 shorts_request, "Generate YouTube Shorts")
                
                if success and data:
                    expected_fields = ['success', 'shorts_generated', 'shorts']
                    missing_fields = [field for field in expected_fields if field not in data]
                    
                    if missing_fields:
                        self.log_test("YouTube Shorts Response", False, f"Missing fields: {missing_fields}")
                    else:
                        shorts_count = data.get('shorts_generated', 0)
                        self.log_test("YouTube Shorts Response", True, 
                                    f"Generated {shorts_count} shorts scripts")

    def test_social_campaign_creation(self):
        """Test Social Media Campaign creation"""
        print("\n📱 Testing Social Campaign Creation...")
        
        # First create a test product to use
        product_data = {
            "title": "Test Product for Campaign",
            "description": "A test product for social campaign",
            "product_type": "course",
            "price": 49.99
        }
        
        success, created_product = self.test_endpoint('POST', '/products', 201, product_data, 
                                                    "Create Product for Campaign Test")
        
        if success and created_product:
            product_id = created_product.get('id')
            if product_id:
                campaign_request = {
                    "product_id": product_id,
                    "platforms": ["twitter", "instagram", "tiktok"],
                    "posts_per_platform": 2
                }
                
                success, data = self.test_endpoint('POST', '/social/campaign', 200, 
                                                 campaign_request, "Create Social Campaign")
                
                if success and data:
                    expected_fields = ['success', 'campaign']
                    missing_fields = [field for field in expected_fields if field not in data]
                    
                    if missing_fields:
                        self.log_test("Social Campaign Response", False, f"Missing fields: {missing_fields}")
                    else:
                        campaign = data.get('campaign', {})
                        total_posts = campaign.get('total_posts', 0)
                        self.log_test("Social Campaign Response", True, 
                                    f"Created campaign with {total_posts} posts")

    def test_realtime_analytics(self):
        """Test Real-time Analytics endpoint"""
        print("\n📊 Testing Real-time Analytics...")
        
        success, data = self.test_endpoint('GET', '/analytics/realtime', 
                                         test_name="Real-time Analytics")
        
        if success and data:
            expected_fields = ['timestamp', 'products', 'revenue', 'traffic', 'gumroad']
            missing_fields = [field for field in expected_fields if field not in data]
            
            if missing_fields:
                self.log_test("Real-time Analytics Response", False, f"Missing fields: {missing_fields}")
            else:
                products = data.get('products', {})
                revenue = data.get('revenue', {})
                self.log_test("Real-time Analytics Response", True, 
                            f"Products: {products.get('total', 0)}, Revenue: ${revenue.get('total', 0)}")

    def test_revenue_breakdown(self):
        """Test Revenue Breakdown endpoint"""
        print("\n💰 Testing Revenue Breakdown...")
        
        success, data = self.test_endpoint('GET', '/analytics/revenue-breakdown', 
                                         test_name="Revenue Breakdown")
        
        if success and data:
            expected_fields = ['by_product_type', 'by_marketplace', 'projections']
            missing_fields = [field for field in expected_fields if field not in data]
            
            if missing_fields:
                self.log_test("Revenue Breakdown Response", False, f"Missing fields: {missing_fields}")
            else:
                projections = data.get('projections', {})
                self.log_test("Revenue Breakdown Response", True, 
                            f"Projections available: {len(projections)} periods")

    def test_ai_tasks_endpoints(self):
        """Test AI tasks management"""
        print("\n⚙️ Testing AI Tasks Endpoints...")
        
        # Test GET AI tasks
        success, tasks = self.test_endpoint('GET', '/ai/tasks?limit=10', 
                                          test_name="Get AI Tasks")
        
        if success:
            self.log_test("AI Tasks List Type", isinstance(tasks, list), 
                         f"Returned {len(tasks)} tasks")

    def run_all_tests(self):
        """Run all test suites"""
        print("🚀 Starting CEO System Backend API Tests")
        print(f"Testing against: {self.base_url}")
        print("=" * 60)
        
        # Core system tests
        self.test_system_health()
        self.test_dashboard_stats()
        
        # CRUD operations
        self.test_products_endpoints()
        self.test_opportunities_endpoints()
        self.test_ai_tasks_endpoints()
        
        # AI functionality tests
        self.test_ai_scout_opportunities()
        self.test_ai_generate_book()
        self.test_ai_optimize_revenue()
        self.test_ai_affiliate_program()
        self.test_analytics_insights()
        
        # Print summary
        print("\n" + "=" * 60)
        print("🏁 TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {len(self.failed_tests)}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.failed_tests:
            print("\n❌ FAILED TESTS:")
            for test in self.failed_tests:
                print(f"  - {test['test']}: {test['details']}")
        
        return len(self.failed_tests) == 0

def main():
    # Get backend URL from environment
    import os
    backend_url = "https://leadership-portal-4.preview.emergentagent.com"
    
    print(f"🎯 CEO System Backend Testing")
    print(f"Backend URL: {backend_url}")
    
    tester = CEOSystemTester(backend_url)
    success = tester.run_all_tests()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())