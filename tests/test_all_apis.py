#!/usr/bin/env python3
"""
Comprehensive API test suite for Dustbin
Tests ALL API endpoints with detailed validation
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"
API_V1 = f"{BASE_URL}/api/v1"
AI_API = f"{BASE_URL}/api"

class APITester:
    def __init__(self):
        self.results = {}
        self.created_pastes = []
        self.session = requests.Session()
    
    def log_test(self, test_name, success, details=""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if details:
            print(f"      {details}")
        
        self.results[test_name] = {
            'success': success,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        return success
    
    def test_core_api_endpoints(self):
        """Test all core API endpoints"""
        print("\n🔧 Testing Core API Endpoints")
        print("=" * 40)
        
        # Test 1: Create Paste (Anonymous)
        print("\n📝 Testing Paste Creation")
        try:
            paste_data = {
                "title": "Comprehensive API Test",
                "content": """# API Test Paste

This is a test paste created via API to validate all functionality.

## Features Tested:
- Paste creation
- Content retrieval
- Language detection
- AI assistance

```python
def test_api():
    print("Testing Dustbin API!")
    return {"status": "success", "features": ["paste", "ai", "preview"]}

test_api()
```

**Created**: {datetime.now().isoformat()}
""",
                "language": "markdown",
                "expires_in": "1week",
                "is_public": True
            }
            
            response = self.session.post(f"{API_V1}/pastes", json=paste_data)
            
            if response.status_code == 201:
                paste = response.json()
                paste_id = paste['id']
                self.created_pastes.append(paste_id)
                
                # Validate response structure
                required_fields = ['id', 'title', 'language', 'created_at', 'url', 'raw_url', 'api_url']
                missing_fields = [f for f in required_fields if f not in paste]
                
                if missing_fields:
                    self.log_test("Create Paste", False, f"Missing fields: {missing_fields}")
                else:
                    self.log_test("Create Paste", True, f"Created paste {paste_id}")
                    
            else:
                self.log_test("Create Paste", False, f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            self.log_test("Create Paste", False, f"Exception: {e}")
        
        # Test 2: Get Specific Paste
        if self.created_pastes:
            print("\n📖 Testing Paste Retrieval")
            try:
                paste_id = self.created_pastes[0]
                response = self.session.get(f"{API_V1}/pastes/{paste_id}")
                
                if response.status_code == 200:
                    paste_data = response.json()
                    
                    # Validate response structure
                    required_fields = ['id', 'title', 'content', 'language', 'created_at', 'views', 'urls']
                    missing_fields = [f for f in required_fields if f not in paste_data]
                    
                    if missing_fields:
                        self.log_test("Get Paste", False, f"Missing fields: {missing_fields}")
                    else:
                        content_length = len(paste_data['content'])
                        self.log_test("Get Paste", True, f"Retrieved {content_length} chars, {paste_data['views']} views")
                        
                else:
                    self.log_test("Get Paste", False, f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_test("Get Paste", False, f"Exception: {e}")
        
        # Test 3: List Pastes with Pagination
        print("\n📋 Testing Paste Listing")
        try:
            # Test basic listing
            response = self.session.get(f"{API_V1}/pastes?page=1&per_page=5")
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                if 'pastes' in data and 'pagination' in data:
                    paste_count = len(data['pastes'])
                    total = data['pagination']['total']
                    self.log_test("List Pastes", True, f"Listed {paste_count} pastes, total: {total}")
                else:
                    self.log_test("List Pastes", False, "Missing pastes or pagination in response")
                    
            else:
                self.log_test("List Pastes", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("List Pastes", False, f"Exception: {e}")
        
        # Test 4: List Pastes with Filters
        print("\n🔍 Testing Paste Filtering")
        try:
            # Test language filter
            response = self.session.get(f"{API_V1}/pastes?language=markdown&per_page=3")
            
            if response.status_code == 200:
                data = response.json()
                markdown_pastes = [p for p in data['pastes'] if p['language'] == 'markdown']
                
                if len(markdown_pastes) == len(data['pastes']):
                    self.log_test("Filter by Language", True, f"Found {len(markdown_pastes)} markdown pastes")
                else:
                    self.log_test("Filter by Language", False, "Filter not working correctly")
                    
            else:
                self.log_test("Filter by Language", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Filter by Language", False, f"Exception: {e}")
        
        # Test 5: Search Pastes
        print("\n🔎 Testing Paste Search")
        try:
            response = self.session.get(f"{API_V1}/pastes?search=API&per_page=5")
            
            if response.status_code == 200:
                data = response.json()
                search_results = len(data['pastes'])
                self.log_test("Search Pastes", True, f"Found {search_results} results for 'API'")
            else:
                self.log_test("Search Pastes", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Search Pastes", False, f"Exception: {e}")
        
        # Test 6: Get Languages
        print("\n🔤 Testing Languages Endpoint")
        try:
            response = self.session.get(f"{API_V1}/languages")
            
            if response.status_code == 200:
                data = response.json()
                
                if 'languages' in data and 'categories' in data and 'total_count' in data:
                    lang_count = data['total_count']
                    categories = len(data['categories'])
                    self.log_test("Get Languages", True, f"{lang_count} languages, {categories} categories")
                else:
                    self.log_test("Get Languages", False, "Missing required fields in response")
                    
            else:
                self.log_test("Get Languages", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Get Languages", False, f"Exception: {e}")
        
        # Test 7: Get Statistics
        print("\n📊 Testing Statistics Endpoint")
        try:
            response = self.session.get(f"{API_V1}/stats")
            
            if response.status_code == 200:
                data = response.json()
                
                required_fields = ['total_pastes', 'public_pastes', 'total_users', 'top_languages', 'features']
                missing_fields = [f for f in required_fields if f not in data]
                
                if missing_fields:
                    self.log_test("Get Statistics", False, f"Missing fields: {missing_fields}")
                else:
                    total = data['total_pastes']
                    public = data['public_pastes']
                    users = data['total_users']
                    self.log_test("Get Statistics", True, f"{total} total, {public} public, {users} users")
                    
            else:
                self.log_test("Get Statistics", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Get Statistics", False, f"Exception: {e}")
    
    def test_ai_endpoints(self):
        """Test all AI-powered endpoints"""
        print("\n🤖 Testing AI Endpoints")
        print("=" * 30)
        
        # Test 1: AI Status
        print("\n🔍 Testing AI Status")
        try:
            response = self.session.get(f"{AI_API}/ai/status")
            
            if response.status_code == 200:
                data = response.json()
                
                required_fields = ['ai_enabled', 'available_models', 'features', 'status']
                missing_fields = [f for f in required_fields if f not in data]
                
                if missing_fields:
                    self.log_test("AI Status", False, f"Missing fields: {missing_fields}")
                else:
                    ai_enabled = data['ai_enabled']
                    model_count = len(data['available_models'])
                    feature_count = len(data['features'])
                    self.log_test("AI Status", True, f"AI: {ai_enabled}, {model_count} models, {feature_count} features")
                    
            else:
                self.log_test("AI Status", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("AI Status", False, f"Exception: {e}")
        
        # Test 2: Language Detection
        print("\n🔍 Testing Language Detection")
        test_cases = [
            {
                "name": "Python Code",
                "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
                "expected": "python"
            },
            {
                "name": "JavaScript Code", 
                "code": "function factorial(n) {\n    return n <= 1 ? 1 : n * factorial(n - 1);\n}",
                "expected": "javascript"
            },
            {
                "name": "HTML Code",
                "code": "<!DOCTYPE html>\n<html>\n<head><title>Test</title></head>\n<body><h1>Hello</h1></body>\n</html>",
                "expected": "html"
            }
        ]
        
        detection_success = 0
        for test_case in test_cases:
            try:
                response = self.session.post(f"{AI_API}/ai/detect-language", 
                                           json={"code": test_case["code"]})
                
                if response.status_code == 200:
                    data = response.json()
                    detected = data.get('language', 'unknown')
                    confidence = data.get('confidence', 'unknown')
                    
                    success = detected == test_case['expected']
                    if success:
                        detection_success += 1
                    
                    self.log_test(f"Detect {test_case['name']}", success, 
                                f"Expected: {test_case['expected']}, Got: {detected} ({confidence})")
                else:
                    self.log_test(f"Detect {test_case['name']}", False, f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Detect {test_case['name']}", False, f"Exception: {e}")
        
        # Overall detection success rate
        detection_rate = (detection_success / len(test_cases)) * 100
        self.log_test("Language Detection Overall", detection_success > 0, 
                     f"{detection_rate:.1f}% success rate ({detection_success}/{len(test_cases)})")
        
        # Test 3: Code Explanation
        print("\n💡 Testing Code Explanation")
        try:
            test_code = """def quicksort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)"""
            
            response = self.session.post(f"{AI_API}/ai/explain-code", 
                                       json={"code": test_code, "language": "python"})
            
            if response.status_code == 200:
                data = response.json()
                
                if 'explanation' in data and 'ai_powered' in data:
                    explanation_length = len(data['explanation'])
                    ai_powered = data['ai_powered']
                    self.log_test("Code Explanation", True, 
                                f"{explanation_length} chars, AI: {ai_powered}")
                else:
                    self.log_test("Code Explanation", False, "Missing required fields")
                    
            else:
                self.log_test("Code Explanation", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Code Explanation", False, f"Exception: {e}")
        
        # Test 4: Code Completion
        print("\n🪄 Testing Code Completion")
        try:
            test_code = """def calculate_fibonacci(n):
    # This function calculates fibonacci numbers
    if n <= 1:
        return n
    # Add recursive case here"""
            
            response = self.session.post(f"{AI_API}/ai/complete-code", 
                                       json={"code": test_code, "language": "python"})
            
            if response.status_code == 200:
                data = response.json()
                
                if 'ai_powered' in data and 'available' in data:
                    ai_powered = data['ai_powered']
                    available = data['available']
                    completion = data.get('completion', 'None')
                    
                    # Success if endpoint works, regardless of AI availability
                    self.log_test("Code Completion", True, 
                                f"AI: {ai_powered}, Available: {available}, Completion: {bool(completion)}")
                else:
                    self.log_test("Code Completion", False, "Missing required fields")
                    
            else:
                self.log_test("Code Completion", False, f"HTTP {response.status_code}")
                
        except Exception as e:
            self.log_test("Code Completion", False, f"Exception: {e}")
    
    def test_error_handling(self):
        """Test error handling and edge cases"""
        print("\n⚠️  Testing Error Handling")
        print("=" * 30)
        
        # Test 1: Invalid Paste ID
        try:
            response = self.session.get(f"{API_V1}/pastes/invalid_id_12345")
            expected_status = 404
            
            success = response.status_code == expected_status
            self.log_test("Invalid Paste ID", success, 
                         f"Expected {expected_status}, got {response.status_code}")
                         
        except Exception as e:
            self.log_test("Invalid Paste ID", False, f"Exception: {e}")
        
        # Test 2: Invalid JSON in Create Paste
        try:
            response = self.session.post(f"{API_V1}/pastes", 
                                       json={"invalid": "missing required fields"})
            expected_status = 400
            
            success = response.status_code == expected_status
            self.log_test("Invalid Create Data", success, 
                         f"Expected {expected_status}, got {response.status_code}")
                         
        except Exception as e:
            self.log_test("Invalid Create Data", False, f"Exception: {e}")
        
        # Test 3: Empty AI Request
        try:
            response = self.session.post(f"{AI_API}/ai/detect-language", json={})
            expected_status = 400
            
            success = response.status_code == expected_status
            self.log_test("Empty AI Request", success, 
                         f"Expected {expected_status}, got {response.status_code}")
                         
        except Exception as e:
            self.log_test("Empty AI Request", False, f"Exception: {e}")
    
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🚀 Dustbin Comprehensive API Test Suite")
        print("=" * 60)
        print(f"Testing against: {BASE_URL}")
        print(f"Started at: {datetime.now().isoformat()}")
        
        # Run all test categories
        self.test_core_api_endpoints()
        self.test_ai_endpoints()
        self.test_error_handling()
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate test results summary"""
        print("\n" + "=" * 60)
        print("📊 Comprehensive Test Results Summary")
        print("=" * 60)
        
        # Categorize results
        categories = {
            "Core API": ["Create Paste", "Get Paste", "List Pastes", "Filter by Language", 
                        "Search Pastes", "Get Languages", "Get Statistics"],
            "AI Features": ["AI Status", "Detect Python Code", "Detect JavaScript Code", 
                           "Detect HTML Code", "Language Detection Overall", "Code Explanation", "Code Completion"],
            "Error Handling": ["Invalid Paste ID", "Invalid Create Data", "Empty AI Request"]
        }
        
        for category, tests in categories.items():
            print(f"\n🔧 {category}:")
            category_results = []
            
            for test in tests:
                if test in self.results:
                    result = self.results[test]
                    status = "✅ PASS" if result['success'] else "❌ FAIL"
                    print(f"   {test}: {status}")
                    category_results.append(result['success'])
                else:
                    print(f"   {test}: ⚪ NOT RUN")
            
            if category_results:
                success_rate = (sum(category_results) / len(category_results)) * 100
                print(f"   📈 Success Rate: {success_rate:.1f}% ({sum(category_results)}/{len(category_results)})")
        
        # Overall statistics
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results.values() if r['success'])
        overall_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"\n🎯 Overall Results:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests}")
        print(f"   Failed: {total_tests - passed_tests}")
        print(f"   Success Rate: {overall_rate:.1f}%")
        
        # Performance rating
        if overall_rate >= 95:
            print("🏆 EXCELLENT! All systems working perfectly!")
        elif overall_rate >= 85:
            print("🎉 GREAT! Most features working well!")
        elif overall_rate >= 70:
            print("👍 GOOD! Core functionality working!")
        else:
            print("⚠️  NEEDS ATTENTION! Several issues detected!")
        
        print(f"\n📚 API Documentation: {BASE_URL}/docs")
        print(f"🔗 Created Test Pastes: {len(self.created_pastes)}")
        if self.created_pastes:
            print(f"   Example: {BASE_URL}/paste/{self.created_pastes[0]}")
        
        print("\n✅ Comprehensive API testing completed!")

def main():
    """Run the comprehensive API test suite"""
    try:
        tester = APITester()
        tester.run_all_tests()
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Dustbin server at http://127.0.0.1:5000")
        print("Make sure the Flask app is running!")
    except Exception as e:
        print(f"❌ Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
