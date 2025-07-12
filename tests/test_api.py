#!/usr/bin/env python3
"""
Comprehensive API testing script for Dustbin
Tests all API endpoints and functionality
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_api_endpoints():
    """Test all API endpoints"""
    print("🧪 Testing Dustbin API Endpoints")
    print("=" * 50)
    
    results = {}
    
    # Test 1: Create a paste
    print("\n📝 Testing: Create Paste")
    try:
        paste_data = {
            "title": "API Test Paste",
            "content": """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Test the function
for i in range(10):
    print(f"fib({i}) = {fibonacci(i)}")""",
            "language": "python",
            "expires_in": "1week",
            "is_public": True
        }
        
        response = requests.post(f"{BASE_URL}/pastes", json=paste_data)
        
        if response.status_code == 201:
            paste = response.json()
            paste_id = paste['id']
            print(f"✅ Created paste: {paste_id}")
            print(f"   URL: {paste['url']}")
            print(f"   Preview Available: {paste['preview_available']}")
            results['create_paste'] = {'success': True, 'paste_id': paste_id}
        else:
            print(f"❌ Failed to create paste: {response.status_code}")
            print(f"   Response: {response.text}")
            results['create_paste'] = {'success': False}
            return results
            
    except Exception as e:
        print(f"❌ Error creating paste: {e}")
        results['create_paste'] = {'success': False}
        return results
    
    # Test 2: Get the paste
    print("\n📖 Testing: Get Paste")
    try:
        response = requests.get(f"{BASE_URL}/pastes/{paste_id}")
        
        if response.status_code == 200:
            paste_data = response.json()
            print(f"✅ Retrieved paste: {paste_data['id']}")
            print(f"   Title: {paste_data['title']}")
            print(f"   Language: {paste_data['language']}")
            print(f"   Views: {paste_data['views']}")
            print(f"   Content Length: {paste_data['content_length']}")
            results['get_paste'] = {'success': True}
        else:
            print(f"❌ Failed to get paste: {response.status_code}")
            results['get_paste'] = {'success': False}
            
    except Exception as e:
        print(f"❌ Error getting paste: {e}")
        results['get_paste'] = {'success': False}
    
    # Test 3: List pastes
    print("\n📋 Testing: List Pastes")
    try:
        response = requests.get(f"{BASE_URL}/pastes?page=1&per_page=5&language=python")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Listed pastes: {len(data['pastes'])} items")
            print(f"   Total: {data['pagination']['total']}")
            print(f"   Pages: {data['pagination']['pages']}")
            if data['pastes']:
                print(f"   First paste: {data['pastes'][0]['id']}")
            results['list_pastes'] = {'success': True}
        else:
            print(f"❌ Failed to list pastes: {response.status_code}")
            results['list_pastes'] = {'success': False}
            
    except Exception as e:
        print(f"❌ Error listing pastes: {e}")
        results['list_pastes'] = {'success': False}
    
    # Test 4: Get languages
    print("\n🔤 Testing: Get Languages")
    try:
        response = requests.get(f"{BASE_URL}/languages")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrieved languages: {data['total_count']} languages")
            print(f"   Categories: {len(data['categories'])}")
            
            # Show some examples
            python_lang = next((l for l in data['languages'] if l['id'] == 'python'), None)
            if python_lang:
                print(f"   Python: {python_lang['name']} (preview: {python_lang['preview_supported']})")
            
            results['get_languages'] = {'success': True}
        else:
            print(f"❌ Failed to get languages: {response.status_code}")
            results['get_languages'] = {'success': False}
            
    except Exception as e:
        print(f"❌ Error getting languages: {e}")
        results['get_languages'] = {'success': False}
    
    # Test 5: Get statistics
    print("\n📊 Testing: Get Statistics")
    try:
        response = requests.get(f"{BASE_URL}/stats")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Retrieved statistics:")
            print(f"   Total Pastes: {data['total_pastes']}")
            print(f"   Public Pastes: {data['public_pastes']}")
            print(f"   Total Users: {data['total_users']}")
            print(f"   Recent (24h): {data['recent_pastes_24h']}")
            
            if data['top_languages']:
                print(f"   Top Language: {data['top_languages'][0]['language']} ({data['top_languages'][0]['count']} pastes)")
            
            results['get_stats'] = {'success': True}
        else:
            print(f"❌ Failed to get statistics: {response.status_code}")
            results['get_stats'] = {'success': False}
            
    except Exception as e:
        print(f"❌ Error getting statistics: {e}")
        results['get_stats'] = {'success': False}
    
    return results

def test_ai_endpoints():
    """Test AI-powered endpoints"""
    print("\n🤖 Testing AI Endpoints")
    print("=" * 30)
    
    ai_results = {}
    
    # Test AI Status
    print("\n🔍 Testing: AI Status")
    try:
        response = requests.get("http://127.0.0.1:5000/api/ai/status")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ AI Status: {data['status']}")
            print(f"   AI Enabled: {data['ai_enabled']}")
            print(f"   Available Models: {len(data['available_models'])}")
            print(f"   Features: {list(data['features'].keys())}")
            ai_results['ai_status'] = {'success': True, 'ai_enabled': data['ai_enabled']}
        else:
            print(f"❌ Failed to get AI status: {response.status_code}")
            ai_results['ai_status'] = {'success': False}
            
    except Exception as e:
        print(f"❌ Error getting AI status: {e}")
        ai_results['ai_status'] = {'success': False}
    
    # Test Language Detection
    print("\n🔍 Testing: Language Detection")
    try:
        test_code = """function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

console.log(factorial(5));"""
        
        response = requests.post("http://127.0.0.1:5000/api/ai/detect-language", 
                               json={"code": test_code})
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Language Detection:")
            print(f"   Detected: {data['language']}")
            print(f"   Confidence: {data['confidence']}")
            print(f"   Suggestions: {len(data['suggestions'])} alternatives")
            ai_results['language_detection'] = {'success': True}
        else:
            print(f"❌ Failed language detection: {response.status_code}")
            ai_results['language_detection'] = {'success': False}
            
    except Exception as e:
        print(f"❌ Error in language detection: {e}")
        ai_results['language_detection'] = {'success': False}
    
    # Test Code Explanation
    print("\n💡 Testing: Code Explanation")
    try:
        test_code = """def quicksort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)"""
        
        response = requests.post("http://127.0.0.1:5000/api/ai/explain-code", 
                               json={"code": test_code, "language": "python"})
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Code Explanation:")
            print(f"   AI Powered: {data['ai_powered']}")
            print(f"   Explanation: {data['explanation'][:100]}...")
            ai_results['code_explanation'] = {'success': True}
        else:
            print(f"❌ Failed code explanation: {response.status_code}")
            ai_results['code_explanation'] = {'success': False}
            
    except Exception as e:
        print(f"❌ Error in code explanation: {e}")
        ai_results['code_explanation'] = {'success': False}
    
    # Test Code Completion
    print("\n🪄 Testing: Code Completion")
    try:
        test_code = """def fibonacci(n):
    # Calculate fibonacci number
    if n <= 1:
        return n
    # Add recursive case here"""
        
        response = requests.post("http://127.0.0.1:5000/api/ai/complete-code", 
                               json={"code": test_code, "language": "python"})
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Code Completion:")
            print(f"   AI Powered: {data['ai_powered']}")
            print(f"   Available: {data['available']}")
            if data['completion']:
                print(f"   Completion: {data['completion'][:50]}...")
            else:
                print(f"   Note: Requires HUGGINGFACE_API_TOKEN for full features")
            ai_results['code_completion'] = {'success': True}
        else:
            print(f"❌ Failed code completion: {response.status_code}")
            ai_results['code_completion'] = {'success': False}
            
    except Exception as e:
        print(f"❌ Error in code completion: {e}")
        ai_results['code_completion'] = {'success': False}
    
    return ai_results

def main():
    """Run comprehensive API tests"""
    print("🚀 Dustbin API Comprehensive Test Suite")
    print("=" * 60)
    
    try:
        # Test main API endpoints
        api_results = test_api_endpoints()
        
        # Test AI endpoints
        ai_results = test_ai_endpoints()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 Test Results Summary")
        print("=" * 60)
        
        print("\n🔧 Core API Endpoints:")
        for test, result in api_results.items():
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            print(f"   {test.replace('_', ' ').title()}: {status}")
        
        print("\n🤖 AI Endpoints:")
        for test, result in ai_results.items():
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            print(f"   {test.replace('_', ' ').title()}: {status}")
        
        # Overall success rate
        total_tests = len(api_results) + len(ai_results)
        passed_tests = sum(1 for r in api_results.values() if r['success']) + \
                      sum(1 for r in ai_results.values() if r['success'])
        
        success_rate = (passed_tests / total_tests) * 100
        
        print(f"\n🎯 Overall Success Rate: {success_rate:.1f}% ({passed_tests}/{total_tests})")
        
        if success_rate >= 90:
            print("🎉 Excellent! API is working great!")
        elif success_rate >= 70:
            print("👍 Good! Most features are working.")
        else:
            print("⚠️  Some issues detected. Check the logs above.")
        
        print(f"\n📚 API Documentation: http://127.0.0.1:5000/docs")
        print("✅ API testing completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Dustbin server at http://127.0.0.1:5000")
        print("Make sure the Flask app is running!")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
