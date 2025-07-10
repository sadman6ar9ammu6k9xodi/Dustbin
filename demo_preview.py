#!/usr/bin/env python3
"""
Demo script to showcase the preview features
Creates sample pastes for demonstration
"""

import requests
from bs4 import BeautifulSoup

BASE_URL = "http://127.0.0.1:5000"

def get_csrf_and_create_paste(title, content, language):
    """Create a paste with CSRF token (for authenticated users only due to rate limiting)"""
    session = requests.Session()
    
    # Get CSRF token
    response = session.get(f"{BASE_URL}/new")
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_input = soup.find('input', {'name': 'csrf_token'})
    
    if not csrf_input:
        return None
    
    csrf_token = csrf_input.get('value')
    
    # Create paste
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
        location = response.headers.get('Location', '')
        if '/paste/' in location:
            return location.split('/paste/')[-1]
    return None

def create_demo_content():
    """Create demo content for each preview type"""
    
    # Markdown demo
    markdown_demo = """# 🗑️ Dustbin Preview Demo

Welcome to **Dustbin's** new preview functionality! This demonstrates the *Markdown* rendering capabilities.

## ✨ Features

- [x] **Live Markdown Preview** - See rendered output instantly
- [x] **Syntax Highlighting** - Code blocks with proper highlighting  
- [x] **Security** - Sanitized HTML output prevents XSS
- [x] **Responsive Design** - Works on mobile and desktop

## 📝 Code Example

```python
def dustbin_preview():
    print("🎉 Markdown preview is working!")
    return {"status": "awesome", "feature": "preview"}

# Test the function
result = dustbin_preview()
print(f"Result: {result}")
```

## 📊 Comparison Table

| Feature | Before | After |
|---------|--------|-------|
| Markdown | Code only | ✅ Live preview |
| HTML | Code only | ✅ Sandboxed preview |
| SVG | Code only | ✅ Vector preview |

> **Note**: All previews are rendered securely with proper sanitization and sandboxing.

---

### 🔗 Links and More

- [Dustbin GitHub](https://github.com/gpbot-org/Dustbin)
- **Bold text** and *italic text*
- `inline code` and code blocks

**Try switching between Preview and Source tabs above!**
"""

    # HTML demo
    html_demo = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dustbin HTML Preview Demo</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        h1 { text-align: center; margin-bottom: 30px; }
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .feature-card {
            background: rgba(255,255,255,0.2);
            padding: 20px;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.3);
        }
        .demo-button {
            background: #4CAF50;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        .demo-button:hover {
            background: #45a049;
            transform: translateY(-2px);
        }
        .warning {
            background: rgba(255,193,7,0.2);
            border: 1px solid rgba(255,193,7,0.5);
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 Dustbin HTML Preview Demo</h1>
        
        <div class="warning">
            <strong>🔒 Security Notice:</strong> This HTML is rendered in a secure sandboxed iframe. 
            JavaScript is disabled for security reasons.
        </div>
        
        <div class="feature-grid">
            <div class="feature-card">
                <h3>✅ Working Features</h3>
                <ul>
                    <li>HTML structure</li>
                    <li>CSS styling & animations</li>
                    <li>Responsive grid layouts</li>
                    <li>Gradients & effects</li>
                    <li>Custom fonts</li>
                </ul>
            </div>
            
            <div class="feature-card">
                <h3>🔒 Security Features</h3>
                <ul>
                    <li>Sandboxed iframe</li>
                    <li>No JavaScript execution</li>
                    <li>XSS protection</li>
                    <li>Content sanitization</li>
                    <li>Safe rendering</li>
                </ul>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <button class="demo-button" onclick="alert('JavaScript is disabled for security!')">
                Test Button (JS Disabled)
            </button>
        </div>
        
        <p style="text-align: center; margin-top: 20px; opacity: 0.8;">
            This demonstrates Dustbin's ability to safely preview HTML content!
        </p>
    </div>
</body>
</html>"""

    # SVG demo
    svg_demo = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 400" width="500" height="400">
    <defs>
        <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
        </linearGradient>
        <radialGradient id="circleGrad" cx="50%" cy="50%" r="50%">
            <stop offset="0%" style="stop-color:#ffffff;stop-opacity:0.8" />
            <stop offset="100%" style="stop-color:#ffffff;stop-opacity:0.2" />
        </radialGradient>
    </defs>
    
    <!-- Background -->
    <rect width="500" height="400" fill="url(#bgGrad)" rx="15"/>
    
    <!-- Title -->
    <text x="250" y="50" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="28" font-weight="bold">
        🎨 Dustbin SVG Preview
    </text>
    
    <!-- Subtitle -->
    <text x="250" y="80" text-anchor="middle" fill="rgba(255,255,255,0.8)" font-family="Arial, sans-serif" font-size="16">
        Scalable Vector Graphics with Live Preview
    </text>
    
    <!-- Animated circles -->
    <circle cx="150" cy="150" r="25" fill="url(#circleGrad)">
        <animate attributeName="r" values="25;35;25" dur="3s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.8;0.4;0.8" dur="3s" repeatCount="indefinite"/>
    </circle>
    
    <circle cx="350" cy="150" r="30" fill="url(#circleGrad)">
        <animate attributeName="r" values="30;20;30" dur="2s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.6;1;0.6" dur="2s" repeatCount="indefinite"/>
    </circle>
    
    <!-- Feature boxes -->
    <rect x="50" y="200" width="180" height="80" fill="rgba(255,255,255,0.2)" rx="10" stroke="rgba(255,255,255,0.4)" stroke-width="2"/>
    <text x="140" y="225" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="14" font-weight="bold">
        ✅ Vector Graphics
    </text>
    <text x="140" y="245" text-anchor="middle" fill="rgba(255,255,255,0.9)" font-family="Arial, sans-serif" font-size="12">
        • Infinite scalability
    </text>
    <text x="140" y="260" text-anchor="middle" fill="rgba(255,255,255,0.9)" font-family="Arial, sans-serif" font-size="12">
        • CSS animations
    </text>
    <text x="140" y="275" text-anchor="middle" fill="rgba(255,255,255,0.9)" font-family="Arial, sans-serif" font-size="12">
        • Interactive elements
    </text>
    
    <rect x="270" y="200" width="180" height="80" fill="rgba(255,255,255,0.2)" rx="10" stroke="rgba(255,255,255,0.4)" stroke-width="2"/>
    <text x="360" y="225" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="14" font-weight="bold">
        🔧 Features
    </text>
    <text x="360" y="245" text-anchor="middle" fill="rgba(255,255,255,0.9)" font-family="Arial, sans-serif" font-size="12">
        • Live preview
    </text>
    <text x="360" y="260" text-anchor="middle" fill="rgba(255,255,255,0.9)" font-family="Arial, sans-serif" font-size="12">
        • Download support
    </text>
    <text x="360" y="275" text-anchor="middle" fill="rgba(255,255,255,0.9)" font-family="Arial, sans-serif" font-size="12">
        • Responsive design
    </text>
    
    <!-- Animated path -->
    <path d="M 100 320 Q 250 300 400 320" stroke="rgba(255,255,255,0.6)" stroke-width="3" fill="none">
        <animate attributeName="stroke-dasharray" values="0,1000;1000,0;0,1000" dur="4s" repeatCount="indefinite"/>
    </path>
    
    <!-- Footer -->
    <text x="250" y="360" text-anchor="middle" fill="rgba(255,255,255,0.7)" font-family="Arial, sans-serif" font-size="14">
        Try the download button to save this SVG!
    </text>
</svg>"""

    return {
        'markdown': ('Markdown Preview Demo', markdown_demo),
        'html': ('HTML Preview Demo', html_demo),
        'svg': ('SVG Preview Demo', svg_demo)
    }

def main():
    print("🎨 Dustbin Preview Demo")
    print("=" * 40)
    print("This script demonstrates the new preview features.")
    print("Note: Due to rate limiting, you may need to create pastes manually.")
    print()
    
    demos = create_demo_content()
    
    print("📋 Demo Content Created:")
    print()
    
    for content_type, (title, content) in demos.items():
        print(f"🔹 {content_type.upper()}: {title}")
        print(f"   Length: {len(content)} characters")
        print(f"   Language: {content_type}")
        print()
    
    print("🌐 To test the preview features:")
    print("1. Go to http://127.0.0.1:5000/new")
    print("2. Copy one of the demo contents above")
    print("3. Select the appropriate language (markdown/html/svg)")
    print("4. Create the paste")
    print("5. Click the 'Preview' button to see the rendered output!")
    print()
    print("✨ Features to test:")
    print("- Markdown: Live rendering with syntax highlighting")
    print("- HTML: Secure sandboxed preview with CSS styling")
    print("- SVG: Vector graphics with animations and download")

if __name__ == "__main__":
    main()
