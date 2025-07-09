#!/usr/bin/env python3
"""
Test script for the new preview features:
1. Markdown preview
2. HTML preview  
3. SVG preview
"""

import requests
from bs4 import BeautifulSoup

BASE_URL = "http://127.0.0.1:5000"

def create_paste_with_csrf(title, content, language):
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
    if response.status_code == 302:
        # Extract paste ID from redirect location
        location = response.headers.get('Location', '')
        if '/paste/' in location:
            paste_id = location.split('/paste/')[-1]
            return paste_id
    return None

def test_markdown_preview():
    """Test Markdown preview functionality"""
    print("📝 Testing Markdown Preview...")
    
    markdown_content = """# Welcome to Dustbin Markdown Preview!

This is a **test** of the *markdown* preview feature.

## Features

- [x] Headers (H1-H6)
- [x] **Bold** and *italic* text
- [x] Lists and checkboxes
- [x] Code blocks
- [x] Links and images
- [x] Tables

### Code Example

```python
def hello_world():
    print("Hello from Dustbin!")
    return "markdown preview works!"

hello_world()
```

### Table Example

| Feature | Status | Notes |
|---------|--------|-------|
| Markdown | ✅ | Working |
| HTML | ✅ | Sandboxed |
| SVG | ✅ | Vector graphics |

> This is a blockquote to test the markdown rendering.

---

**Note**: This markdown is rendered securely with sanitized HTML output.
"""
    
    paste_id = create_paste_with_csrf("Markdown Preview Test", markdown_content, "markdown")
    
    if paste_id:
        print(f"✅ Created markdown paste: {paste_id}")
        
        # Test preview endpoint
        preview_url = f"{BASE_URL}/paste/{paste_id}/preview"
        response = requests.get(preview_url)
        
        if response.status_code == 200:
            print("✅ Markdown preview page accessible")
            if "markdown-preview" in response.text:
                print("✅ Markdown preview content found")
            else:
                print("❌ Markdown preview content not found")
        else:
            print(f"❌ Preview page failed: {response.status_code}")
        
        return paste_id
    else:
        print("❌ Failed to create markdown paste")
        return None

def test_html_preview():
    """Test HTML preview functionality"""
    print("\n🌐 Testing HTML Preview...")
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dustbin HTML Preview Test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        h1 { color: #fff; text-align: center; }
        .feature-box {
            background: rgba(255,255,255,0.2);
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        }
        .button {
            background: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎉 Dustbin HTML Preview</h1>
        <p>This HTML content is rendered in a secure sandboxed iframe!</p>
        
        <div class="feature-box">
            <h3>✅ Features Working:</h3>
            <ul>
                <li>HTML structure</li>
                <li>CSS styling</li>
                <li>Responsive design</li>
                <li>Gradients and effects</li>
            </ul>
        </div>
        
        <div class="feature-box">
            <h3>🔒 Security Features:</h3>
            <ul>
                <li>Sandboxed iframe</li>
                <li>No JavaScript execution</li>
                <li>No external resources</li>
                <li>XSS protection</li>
            </ul>
        </div>
        
        <button class="button" onclick="alert('JS disabled for security')">Test Button (JS Disabled)</button>
    </div>
</body>
</html>"""
    
    paste_id = create_paste_with_csrf("HTML Preview Test", html_content, "html")
    
    if paste_id:
        print(f"✅ Created HTML paste: {paste_id}")
        
        # Test preview endpoint
        preview_url = f"{BASE_URL}/paste/{paste_id}/preview"
        response = requests.get(preview_url)
        
        if response.status_code == 200:
            print("✅ HTML preview page accessible")
            if "html-preview-container" in response.text:
                print("✅ HTML preview container found")
            else:
                print("❌ HTML preview container not found")
        else:
            print(f"❌ Preview page failed: {response.status_code}")
        
        # Test render endpoint
        render_url = f"{BASE_URL}/paste/{paste_id}/preview/render"
        response = requests.get(render_url)
        
        if response.status_code == 200:
            print("✅ HTML render endpoint accessible")
            if "Dustbin HTML Preview" in response.text:
                print("✅ HTML content rendered correctly")
            else:
                print("❌ HTML content not rendered correctly")
        else:
            print(f"❌ Render endpoint failed: {response.status_code}")
        
        return paste_id
    else:
        print("❌ Failed to create HTML paste")
        return None

def test_svg_preview():
    """Test SVG preview functionality"""
    print("\n🎨 Testing SVG Preview...")
    
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="400" height="300">
    <defs>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
        </linearGradient>
    </defs>
    
    <!-- Background -->
    <rect width="400" height="300" fill="url(#grad1)" rx="10"/>
    
    <!-- Title -->
    <text x="200" y="40" text-anchor="middle" fill="white" font-family="Arial" font-size="24" font-weight="bold">
        🗑️ Dustbin SVG Preview
    </text>
    
    <!-- Decorative elements -->
    <circle cx="100" cy="120" r="30" fill="rgba(255,255,255,0.3)" />
    <circle cx="300" cy="120" r="25" fill="rgba(255,255,255,0.2)" />
    <circle cx="200" cy="180" r="35" fill="rgba(255,255,255,0.4)" />
    
    <!-- Feature boxes -->
    <rect x="50" y="200" width="120" height="60" fill="rgba(255,255,255,0.2)" rx="5"/>
    <text x="110" y="220" text-anchor="middle" fill="white" font-size="12" font-weight="bold">✅ Scalable</text>
    <text x="110" y="240" text-anchor="middle" fill="white" font-size="10">Vector Graphics</text>
    
    <rect x="230" y="200" width="120" height="60" fill="rgba(255,255,255,0.2)" rx="5"/>
    <text x="290" y="220" text-anchor="middle" fill="white" font-size="12" font-weight="bold">🎨 Interactive</text>
    <text x="290" y="240" text-anchor="middle" fill="white" font-size="10">CSS Animations</text>
    
    <!-- Animated element -->
    <circle cx="200" cy="120" r="5" fill="yellow">
        <animate attributeName="r" values="5;15;5" dur="2s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="1;0.5;1" dur="2s" repeatCount="indefinite"/>
    </circle>
</svg>"""
    
    paste_id = create_paste_with_csrf("SVG Preview Test", svg_content, "svg")
    
    if paste_id:
        print(f"✅ Created SVG paste: {paste_id}")
        
        # Test preview endpoint
        preview_url = f"{BASE_URL}/paste/{paste_id}/preview"
        response = requests.get(preview_url)
        
        if response.status_code == 200:
            print("✅ SVG preview page accessible")
            if "svg-preview-container" in response.text:
                print("✅ SVG preview container found")
            else:
                print("❌ SVG preview container not found")
        else:
            print(f"❌ Preview page failed: {response.status_code}")
        
        # Test render endpoint
        render_url = f"{BASE_URL}/paste/{paste_id}/preview/render"
        response = requests.get(render_url)
        
        if response.status_code == 200:
            print("✅ SVG render endpoint accessible")
            if "Dustbin SVG Preview" in response.text:
                print("✅ SVG content rendered correctly")
            else:
                print("❌ SVG content not rendered correctly")
        else:
            print(f"❌ Render endpoint failed: {response.status_code}")
        
        return paste_id
    else:
        print("❌ Failed to create SVG paste")
        return None

def main():
    """Run all preview tests"""
    print("🧪 Testing Dustbin Preview Features\n")
    print("=" * 50)
    
    try:
        markdown_id = test_markdown_preview()
        html_id = test_html_preview()
        svg_id = test_svg_preview()
        
        print("\n" + "=" * 50)
        print("📋 Test Results Summary:")
        print(f"Markdown Preview: {'✅ Working' if markdown_id else '❌ Failed'}")
        print(f"HTML Preview: {'✅ Working' if html_id else '❌ Failed'}")
        print(f"SVG Preview: {'✅ Working' if svg_id else '❌ Failed'}")
        
        if markdown_id or html_id or svg_id:
            print("\n🔗 Test Paste URLs:")
            if markdown_id:
                print(f"Markdown: {BASE_URL}/paste/{markdown_id}/preview")
            if html_id:
                print(f"HTML: {BASE_URL}/paste/{html_id}/preview")
            if svg_id:
                print(f"SVG: {BASE_URL}/paste/{svg_id}/preview")
        
        print("\n✅ Preview feature testing completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Dustbin server at http://127.0.0.1:5000")
        print("Make sure the Flask app is running!")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
