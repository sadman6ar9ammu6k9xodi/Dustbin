#!/usr/bin/env python3
"""
Test rate limiting functionality
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

def test_rate_limiting():
    """Test the rate limiting functionality"""
    print("🔍 Testing Rate Limiting with CSRF...")
    
    # Check initial status
    response = requests.get(f"{BASE_URL}/api/rate-limit")
    print(f"Initial status: {response.json()}")
    
    # Create first paste
    print("\n📝 Creating first paste...")
    response1 = create_paste_with_csrf("First Paste", "print('First paste')")
    
    if response1:
        print(f"First paste response: {response1.status_code}")
        if response1.status_code == 302:
            print("✅ First paste created successfully (redirected)")
        else:
            print(f"❌ Unexpected status code: {response1.status_code}")
    
    # Check status after first paste
    response = requests.get(f"{BASE_URL}/api/rate-limit")
    status_after_first = response.json()
    print(f"Status after first paste: {status_after_first}")
    
    # Try to create second paste
    print("\n📝 Attempting second paste...")
    response2 = create_paste_with_csrf("Second Paste", "print('Second paste - should be blocked')")
    
    if response2:
        print(f"Second paste response: {response2.status_code}")
        if response2.status_code == 200:
            # Check if the response contains an error message
            if "Rate limit exceeded" in response2.text:
                print("✅ Second paste correctly blocked by rate limit")
            else:
                print("❌ Second paste was not blocked (rate limiting not working)")
        elif response2.status_code == 302:
            print("❌ Second paste was created (rate limiting not working)")
    
    # Final status check
    response = requests.get(f"{BASE_URL}/api/rate-limit")
    final_status = response.json()
    print(f"Final status: {final_status}")
    
    # Summary
    print("\n" + "="*50)
    if not status_after_first['can_post']:
        print("✅ Rate limiting is working correctly!")
    else:
        print("❌ Rate limiting may not be working as expected")

if __name__ == "__main__":
    try:
        test_rate_limiting()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Dustbin server")
        print("Make sure the Flask app is running at http://127.0.0.1:5000")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
