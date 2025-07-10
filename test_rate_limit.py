#!/usr/bin/env python3
"""
Test basic paste creation functionality (rate limiting removed)
"""

import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "http://127.0.0.1:5000"

def get_csrf_token():
    """Get CSRF token from the new paste form"""
    response = requests.get(f"{BASE_URL}/new")
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_input = soup.find('input', {'name': 'csrf_token'})
    if csrf_input:
        return csrf_input.get('value')
    return None

def create_paste_with_csrf(title, content, language='python'):
    """Create a paste with proper CSRF token"""
    session = requests.Session()
    
    # Get the form page to extract CSRF token
    response = session.get(f"{BASE_URL}/new")
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_input = soup.find('input', {'name': 'csrf_token'})
    
    if not csrf_input:
        print("❌ Could not find CSRF token")
        return None
    
    csrf_token = csrf_input.get('value')
    
    # Submit the form with CSRF token
    paste_data = {
        'csrf_token': csrf_token,
        'title': title,
        'content': content,
        'language': language,
        'expires_in': 'never',
        'is_public': True
    }
    
    response = session.post(f"{BASE_URL}/new", data=paste_data, allow_redirects=False)
    return response

def test_paste_creation():
    """Test basic paste creation functionality"""
    print("🔍 Testing Paste Creation (No Rate Limiting)...")

    # Create first paste
    print("\n📝 Creating first paste...")
    response1 = create_paste_with_csrf("First Paste", "print('First paste')")

    if response1:
        print(f"First paste response: {response1.status_code}")
        if response1.status_code == 302:
            print("✅ First paste created successfully (redirected)")
        else:
            print(f"❌ Unexpected status code: {response1.status_code}")

    # Create second paste immediately
    print("\n📝 Creating second paste...")
    response2 = create_paste_with_csrf("Second Paste", "print('Second paste - should work')")

    if response2:
        print(f"Second paste response: {response2.status_code}")
        if response2.status_code == 302:
            print("✅ Second paste created successfully (no rate limiting)")
        else:
            print(f"❌ Unexpected status code: {response2.status_code}")

    # Summary
    print("\n" + "="*50)
    if response1 and response2 and response1.status_code == 302 and response2.status_code == 302:
        print("✅ Paste creation is working correctly (no rate limiting)!")
    else:
        print("❌ Paste creation may have issues")

if __name__ == "__main__":
    print("🧪 Testing Dustbin Paste Creation (No Rate Limiting)\n")
    print("=" * 50)

    try:
        test_paste_creation()

        print("\n" + "=" * 50)
        print("✅ All tests completed!")

    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Dustbin server at http://127.0.0.1:5000")
        print("Make sure the Flask app is running!")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
