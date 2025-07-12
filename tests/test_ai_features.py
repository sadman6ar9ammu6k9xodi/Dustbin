#!/usr/bin/env python3
"""
Test script for AI features in Dustbin
Tests language detection, code explanation, and completion
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_ai_status():
    """Test AI status endpoint"""
    print("🔍 Testing AI Status...")
    
    response = requests.get(f"{BASE_URL}/api/ai/status")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ AI Status: {data['status']}")
        print(f"   AI Enabled: {data['ai_enabled']}")
        print(f"   Available Models: {len(data['available_models'])}")
        print(f"   Features: {list(data['features'].keys())}")
        return data
    else:
        print(f"❌ AI Status failed: {response.status_code}")
        return None

def test_language_detection():
    """Test language detection with various code samples"""
    print("\n🔍 Testing Language Detection...")
    
    test_cases = [
        {
            "name": "Python",
            "code": """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))""",
            "expected": "python"
        },
        {
            "name": "JavaScript",
            "code": """function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

console.log(factorial(5));""",
            "expected": "javascript"
        },
        {
            "name": "HTML",
            "code": """<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h1>Hello World</h1>
</body>
</html>""",
            "expected": "html"
        },
        {
            "name": "CSS",
            "code": """.container {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
}""",
            "expected": "css"
        },
        {
            "name": "SQL",
            "code": """SELECT users.name, COUNT(posts.id) as post_count
FROM users
LEFT JOIN posts ON users.id = posts.user_id
WHERE users.active = 1
GROUP BY users.id
ORDER BY post_count DESC;""",
            "expected": "sql"
        }
    ]
    
    results = []
    for test_case in test_cases:
        response = requests.post(
            f"{BASE_URL}/api/ai/detect-language",
            headers={"Content-Type": "application/json"},
            json={"code": test_case["code"]}
        )
        
        if response.status_code == 200:
            data = response.json()
            detected = data.get("language", "unknown")
            confidence = data.get("confidence", "unknown")
            
            success = detected == test_case["expected"]
            status = "✅" if success else "⚠️"
            
            print(f"   {status} {test_case['name']}: {detected} ({confidence} confidence)")
            if not success:
                print(f"      Expected: {test_case['expected']}, Got: {detected}")
            
            results.append({
                "test": test_case["name"],
                "expected": test_case["expected"],
                "detected": detected,
                "success": success
            })
        else:
            print(f"   ❌ {test_case['name']}: API Error {response.status_code}")
            results.append({
                "test": test_case["name"],
                "expected": test_case["expected"],
                "detected": "error",
                "success": False
            })
    
    success_rate = sum(1 for r in results if r["success"]) / len(results) * 100
    print(f"\n   Success Rate: {success_rate:.1f}% ({sum(1 for r in results if r['success'])}/{len(results)})")
    
    return results

def test_code_explanation():
    """Test code explanation feature"""
    print("\n💡 Testing Code Explanation...")
    
    test_code = """def quicksort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)

# Example usage
numbers = [3, 6, 8, 10, 1, 2, 1]
sorted_numbers = quicksort(numbers)
print(sorted_numbers)"""
    
    response = requests.post(
        f"{BASE_URL}/api/ai/explain-code",
        headers={"Content-Type": "application/json"},
        json={"code": test_code, "language": "python"}
    )
    
    if response.status_code == 200:
        data = response.json()
        explanation = data.get("explanation", "No explanation")
        ai_powered = data.get("ai_powered", False)
        
        print(f"✅ Code Explanation Generated:")
        print(f"   AI Powered: {ai_powered}")
        print(f"   Explanation: {explanation}")
        return True
    else:
        print(f"❌ Code Explanation failed: {response.status_code}")
        return False

def test_code_completion():
    """Test code completion feature"""
    print("\n🪄 Testing Code Completion...")
    
    test_code = """def calculate_fibonacci(n):
    # This function calculates fibonacci numbers
    if n <= 1:
        return n
    # Add recursive case here"""
    
    response = requests.post(
        f"{BASE_URL}/api/ai/complete-code",
        headers={"Content-Type": "application/json"},
        json={"code": test_code, "language": "python"}
    )
    
    if response.status_code == 200:
        data = response.json()
        completion = data.get("completion")
        ai_powered = data.get("ai_powered", False)
        available = data.get("available", False)
        
        if available and completion:
            print(f"✅ Code Completion Generated:")
            print(f"   AI Powered: {ai_powered}")
            print(f"   Completion: {completion}")
            return True
        else:
            print(f"⚠️  Code Completion not available (requires HUGGINGFACE_API_TOKEN)")
            print(f"   AI Powered: {ai_powered}")
            return False
    else:
        print(f"❌ Code Completion failed: {response.status_code}")
        return False

def main():
    """Run all AI feature tests"""
    print("🤖 Testing Dustbin AI Features")
    print("=" * 50)
    
    try:
        # Test AI status
        ai_status = test_ai_status()
        if not ai_status:
            print("❌ AI system not available")
            return
        
        # Test language detection
        detection_results = test_language_detection()
        
        # Test code explanation
        explanation_success = test_code_explanation()
        
        # Test code completion
        completion_success = test_code_completion()
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 Test Summary:")
        print(f"   AI Status: {'✅ Ready' if ai_status['status'] == 'ready' else '❌ Error'}")
        print(f"   Language Detection: {'✅ Working' if detection_results else '❌ Failed'}")
        print(f"   Code Explanation: {'✅ Working' if explanation_success else '❌ Failed'}")
        print(f"   Code Completion: {'✅ Working' if completion_success else '⚠️ Limited (needs API token)'}")
        
        if ai_status['ai_enabled']:
            print("\n🎉 Full AI features are enabled!")
        else:
            print("\n💡 To enable full AI features:")
            print("   1. Get a Hugging Face API token from: https://huggingface.co/settings/tokens")
            print("   2. Set HUGGINGFACE_API_TOKEN environment variable")
            print("   3. Restart the application")
        
        print("\n✅ AI feature testing completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Dustbin server at http://127.0.0.1:5000")
        print("Make sure the Flask app is running!")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
