#!/usr/bin/env python3
"""
Test script for the new Dustbin features:
1. Rate limiting (1 post per IP per 24 hours)
2. JSON-based language configuration
3. Improved syntax highlighting
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_rate_limit():
    """Test the rate limiting functionality"""
    print("🔍 Testing Rate Limiting...")
    
    # Check initial rate limit status
    response = requests.get(f"{BASE_URL}/api/rate-limit")
    print(f"Initial rate limit status: {response.json()}")
    
    # Create first paste
    paste_data = {
        'title': 'Rate Limit Test 1',
        'content': 'print("First paste")',
        'language': 'python',
        'expires_in': 'never',
        'is_public': True
    }
    
    response = requests.post(f"{BASE_URL}/new", data=paste_data, allow_redirects=False)
    print(f"First paste creation status: {response.status_code}")
    
    # Check rate limit status after first paste
    response = requests.get(f"{BASE_URL}/api/rate-limit")
    print(f"Rate limit after first paste: {response.json()}")
    
    # Try to create second paste (should be blocked)
    paste_data['title'] = 'Rate Limit Test 2'
    paste_data['content'] = 'print("Second paste - should be blocked")'
    
    response = requests.post(f"{BASE_URL}/new", data=paste_data, allow_redirects=False)
    print(f"Second paste creation status: {response.status_code}")
    
    # Check final rate limit status
    response = requests.get(f"{BASE_URL}/api/rate-limit")
    print(f"Final rate limit status: {response.json()}")

def test_language_config():
    """Test the JSON-based language configuration"""
    print("\n🎨 Testing Language Configuration...")
    
    # Test languages page
    response = requests.get(f"{BASE_URL}/languages")
    print(f"Languages page status: {response.status_code}")
    
    # Check if popular languages are available
    response = requests.get(f"{BASE_URL}/new")
    content = response.text
    
    popular_languages = ['python', 'javascript', 'html', 'css', 'java', 'cpp', 'rust', 'go']
    found_languages = []
    
    for lang in popular_languages:
        if f'value="{lang}"' in content:
            found_languages.append(lang)
    
    print(f"Found popular languages: {found_languages}")
    print(f"Total found: {len(found_languages)}/{len(popular_languages)}")

def test_syntax_highlighting():
    """Test improved syntax highlighting"""
    print("\n✨ Testing Syntax Highlighting...")
    
    # Create a paste with Python code
    paste_data = {
        'title': 'Syntax Highlighting Test',
        'content': '''def fibonacci(n):
    """Generate Fibonacci sequence up to n"""
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a + b
    print()

# Test the function
fibonacci(100)''',
        'language': 'python',
        'expires_in': 'never',
        'is_public': True
    }
    
    response = requests.post(f"{BASE_URL}/new", data=paste_data, allow_redirects=False)
    
    if response.status_code == 302:  # Redirect to paste view
        paste_url = response.headers.get('Location')
        if paste_url:
            # Get the paste content
            response = requests.get(paste_url)
            content = response.text
            
            # Check for syntax highlighting elements
            highlighting_indicators = [
                'class="highlight"',
                'class="linenos"',
                'language-badge',
                '<span class='  # Pygments adds span elements for syntax highlighting
            ]
            
            found_indicators = []
            for indicator in highlighting_indicators:
                if indicator in content:
                    found_indicators.append(indicator)
            
            print(f"Syntax highlighting indicators found: {found_indicators}")
            print(f"Highlighting working: {'✅' if len(found_indicators) >= 2 else '❌'}")
        else:
            print("❌ Could not get paste URL")
    else:
        print(f"❌ Failed to create paste: {response.status_code}")

def main():
    """Run all tests"""
    print("🧪 Testing Dustbin New Features\n")
    print("=" * 50)
    
    try:
        test_rate_limit()
        test_language_config()
        test_syntax_highlighting()
        
        print("\n" + "=" * 50)
        print("✅ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Dustbin server at http://127.0.0.1:5000")
        print("Make sure the Flask app is running!")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    main()
