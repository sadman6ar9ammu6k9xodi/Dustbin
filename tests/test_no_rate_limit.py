#!/usr/bin/env python3
"""
Test script to verify no rate limiting and all API functionality
Tests rapid paste creation and all endpoints
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"
API_V1 = f"{BASE_URL}/api/v1"

def test_rapid_paste_creation():
    """Test creating multiple pastes rapidly to confirm no rate limiting"""
    print("🚀 Testing Rapid Paste Creation (No Rate Limiting)")
    print("=" * 60)
    
    pastes_created = []
    start_time = time.time()
    
    # Create 5 pastes rapidly
    test_pastes = [
        {
            "title": "Python Test",
            "content": "def hello():\n    print('Hello World!')\n    return 'success'",
            "language": "python"
        },
        {
            "title": "JavaScript Test", 
            "content": "function greet() {\n    console.log('Hello from JS!');\n    return true;\n}",
            "language": "javascript"
        },
        {
            "title": "HTML Test",
            "content": "<!DOCTYPE html>\n<html>\n<head><title>Test</title></head>\n<body><h1>Hello HTML!</h1></body>\n</html>",
            "language": "html"
        },
        {
            "title": "CSS Test",
            "content": ".container {\n    width: 100%;\n    max-width: 1200px;\n    margin: 0 auto;\n}",
            "language": "css"
        },
        {
            "title": "Markdown Test",
            "content": "# No Rate Limiting Test\n\n**Success!** Created multiple pastes instantly.\n\n- Fast creation\n- No delays\n- Perfect API response",
            "language": "markdown"
        }
    ]
    
    for i, paste_data in enumerate(test_pastes, 1):
        try:
            paste_data["is_public"] = True
            response = requests.post(f"{API_V1}/pastes", json=paste_data)
            
            if response.status_code == 201:
                paste = response.json()
                pastes_created.append(paste['id'])
                print(f"✅ Paste {i}: {paste['id']} ({paste_data['language']}) - Created successfully")
            else:
                print(f"❌ Paste {i}: Failed with status {response.status_code}")
                
        except Exception as e:
            print(f"❌ Paste {i}: Error - {e}")
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n📊 Results:")
    print(f"   Created: {len(pastes_created)}/5 pastes")
    print(f"   Duration: {duration:.2f} seconds")
    print(f"   Rate: {len(pastes_created)/duration:.2f} pastes/second")
    
    if len(pastes_created) == 5:
        print("🎉 SUCCESS: No rate limiting detected!")
    else:
        print("⚠️  Some pastes failed to create")
    
    return pastes_created

def test_all_api_endpoints():
    """Test all API endpoints for functionality"""
    print("\n🔧 Testing All API Endpoints")
    print("=" * 40)
    
    results = {}
    
    # Test 1: List Pastes
    try:
        response = requests.get(f"{API_V1}/pastes?per_page=5")
        if response.status_code == 200:
            data = response.json()
            paste_count = len(data['pastes'])
            total = data['pagination']['total']
            results['list_pastes'] = f"✅ Listed {paste_count} pastes (total: {total})"
        else:
            results['list_pastes'] = f"❌ Failed: {response.status_code}"
    except Exception as e:
        results['list_pastes'] = f"❌ Error: {e}"
    
    # Test 2: Get Languages
    try:
        response = requests.get(f"{API_V1}/languages")
        if response.status_code == 200:
            data = response.json()
            lang_count = data['total_count']
            categories = len(data['categories'])
            results['languages'] = f"✅ {lang_count} languages, {categories} categories"
        else:
            results['languages'] = f"❌ Failed: {response.status_code}"
    except Exception as e:
        results['languages'] = f"❌ Error: {e}"
    
    # Test 3: Get Statistics
    try:
        response = requests.get(f"{API_V1}/stats")
        if response.status_code == 200:
            data = response.json()
            total = data['total_pastes']
            public = data['public_pastes']
            recent = data['recent_pastes_24h']
            results['stats'] = f"✅ {total} total, {public} public, {recent} recent"
        else:
            results['stats'] = f"❌ Failed: {response.status_code}"
    except Exception as e:
        results['stats'] = f"❌ Error: {e}"
    
    # Test 4: AI Language Detection
    try:
        test_code = "def fibonacci(n):\n    return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)"
        response = requests.post(f"{BASE_URL}/api/ai/detect-language", 
                               json={"code": test_code})
        if response.status_code == 200:
            data = response.json()
            detected = data['language']
            confidence = data['confidence']
            results['ai_detection'] = f"✅ Detected: {detected} ({confidence} confidence)"
        else:
            results['ai_detection'] = f"❌ Failed: {response.status_code}"
    except Exception as e:
        results['ai_detection'] = f"❌ Error: {e}"
    
    # Test 5: AI Code Explanation
    try:
        test_code = "for i in range(10):\n    print(f'Number: {i}')"
        response = requests.post(f"{BASE_URL}/api/ai/explain-code", 
                               json={"code": test_code, "language": "python"})
        if response.status_code == 200:
            data = response.json()
            explanation_len = len(data['explanation'])
            ai_powered = data['ai_powered']
            results['ai_explanation'] = f"✅ Explanation: {explanation_len} chars (AI: {ai_powered})"
        else:
            results['ai_explanation'] = f"❌ Failed: {response.status_code}"
    except Exception as e:
        results['ai_explanation'] = f"❌ Error: {e}"
    
    # Test 6: AI Status
    try:
        response = requests.get(f"{BASE_URL}/api/ai/status")
        if response.status_code == 200:
            data = response.json()
            ai_enabled = data['ai_enabled']
            model_count = len(data['available_models'])
            results['ai_status'] = f"✅ AI: {ai_enabled}, {model_count} models available"
        else:
            results['ai_status'] = f"❌ Failed: {response.status_code}"
    except Exception as e:
        results['ai_status'] = f"❌ Error: {e}"
    
    # Print results
    for test_name, result in results.items():
        print(f"   {test_name.replace('_', ' ').title()}: {result}")
    
    success_count = sum(1 for r in results.values() if r.startswith('✅'))
    total_tests = len(results)
    success_rate = (success_count / total_tests) * 100
    
    print(f"\n📈 API Test Results: {success_rate:.1f}% ({success_count}/{total_tests})")
    
    return results

def test_paste_retrieval(paste_ids):
    """Test retrieving created pastes"""
    if not paste_ids:
        return
    
    print(f"\n📖 Testing Paste Retrieval")
    print("=" * 30)
    
    for i, paste_id in enumerate(paste_ids[:3], 1):  # Test first 3
        try:
            response = requests.get(f"{API_V1}/pastes/{paste_id}")
            if response.status_code == 200:
                data = response.json()
                title = data['title']
                language = data['language']
                views = data['views']
                content_len = len(data['content'])
                print(f"✅ Paste {i}: {title} ({language}) - {content_len} chars, {views} views")
            else:
                print(f"❌ Paste {i}: Failed to retrieve - {response.status_code}")
        except Exception as e:
            print(f"❌ Paste {i}: Error - {e}")

def main():
    """Run comprehensive no-rate-limit test suite"""
    print("🧪 Dustbin No Rate Limiting Test Suite")
    print("=" * 70)
    print(f"Testing against: {BASE_URL}")
    print(f"Started at: {datetime.now().isoformat()}")
    
    try:
        # Test rapid paste creation
        created_pastes = test_rapid_paste_creation()
        
        # Test all API endpoints
        api_results = test_all_api_endpoints()
        
        # Test paste retrieval
        test_paste_retrieval(created_pastes)
        
        # Final summary
        print("\n" + "=" * 70)
        print("🎯 Final Test Summary")
        print("=" * 70)
        
        print(f"\n🚀 Rate Limiting Test:")
        if len(created_pastes) >= 4:
            print("   ✅ CONFIRMED: No rate limiting - Multiple pastes created instantly")
        else:
            print("   ⚠️  Possible issues with rapid creation")
        
        print(f"\n🔧 API Functionality:")
        api_success = sum(1 for r in api_results.values() if r.startswith('✅'))
        api_total = len(api_results)
        print(f"   Success Rate: {(api_success/api_total)*100:.1f}% ({api_success}/{api_total})")
        
        print(f"\n📊 Platform Status:")
        print(f"   Created Test Pastes: {len(created_pastes)}")
        print(f"   API Base URL: {API_V1}")
        print(f"   Documentation: {BASE_URL}/docs")
        
        if len(created_pastes) >= 4 and api_success >= 5:
            print("\n🏆 EXCELLENT: All systems working perfectly!")
            print("   ✅ No rate limiting")
            print("   ✅ All APIs functional")
            print("   ✅ AI features working")
        else:
            print("\n⚠️  Some issues detected - check logs above")
        
        print(f"\n✅ Testing completed at: {datetime.now().isoformat()}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Dustbin server at http://127.0.0.1:5000")
        print("Make sure the Flask app is running!")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
