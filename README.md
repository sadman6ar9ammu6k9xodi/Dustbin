# 🗑️ Dustbin - Advanced Pastebin Platform

A modern, feature-rich pastebin platform with AI-powered assistance, syntax highlighting, and comprehensive API support.

## ✨ Features

- 🎨 **Syntax Highlighting** - Support for 99+ programming languages
- 🤖 **AI Assistant** - Language detection, code explanation, and completion
- 📝 **Live Preview** - Markdown, HTML, and SVG preview functionality
- 🔗 **REST API** - Complete API system with comprehensive documentation
- ⏰ **Paste Expiration** - Set automatic deletion times (10 minutes to 1 month)
- 🔒 **Privacy Controls** - Public and private pastes
- 👤 **User Accounts** - Registration, login, and paste history
- 🔍 **Search** - Find public pastes by title or content
- 📱 **Mobile Friendly** - Responsive design works on all devices
- 🍴 **Fork Pastes** - Create copies of existing pastes
- 📊 **Statistics** - View counts and user stats
- 📥 **Download** - Save pastes as files
- 🚀 **Unlimited Creation** - No rate limiting restrictions

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/gpbot-org/Dustbin.git
   cd Dustbin
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**
   ```bash
   python create_db.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Web Interface: http://127.0.0.1:5000
   - API Documentation: http://127.0.0.1:5000/docs

## 🤖 AI Features Setup (Optional)

To enable full AI features (code completion, enhanced language detection):

1. **Get Hugging Face API Token**
   - Visit: https://huggingface.co/settings/tokens
   - Create a new token

2. **Set Environment Variable**
   ```bash
   export HUGGINGFACE_API_TOKEN=your_token_here
   ```

3. **Restart the application**
   ```bash
   python app.py
   ```

## 📁 Project Structure

```
Dustbin/
├── 📄 app.py                 # Main Flask application
├── 🤖 ai_helper.py          # AI integration module
├── 🗄️ create_db.py          # Database initialization
├── 📋 requirements.txt      # Python dependencies
├── 🎨 static/               # CSS, JS, and assets
├── 📄 templates/            # HTML templates
├── 🔧 highlight/            # Language configurations
├── 📚 docs/                 # Documentation files
│   ├── README.md
│   ├── API_SYSTEM.md
│   ├── FEATURES_IMPLEMENTED.md
│   └── PREVIEW_FEATURES.md
└── 🧪 tests/               # Test suite
    ├── test_all_apis.py    # Comprehensive API tests
    ├── test_ai_features.py # AI functionality tests
    ├── test_preview.py     # Preview feature tests
    ├── run_tests.py        # Test runner
    └── ...
```

## 🔗 API Usage

### Quick Examples

**Create a paste:**
```bash
curl -X POST http://127.0.0.1:5000/api/v1/pastes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Hello World",
    "content": "print(\"Hello from API!\")",
    "language": "python",
    "is_public": true
  }'
```

**Get paste content:**
```bash
curl http://127.0.0.1:5000/api/v1/pastes/abc123
```

**AI language detection:**
```bash
curl -X POST http://127.0.0.1:5000/api/ai/detect-language \
  -H "Content-Type: application/json" \
  -d '{"code": "function hello() { console.log(\"Hi!\"); }"}'
```

**Complete API documentation:** http://127.0.0.1:5000/docs

## 🧪 Testing

### Run All Tests
```bash
cd tests
python run_tests.py
```

### Run Specific Tests
```bash
# API functionality
python tests/test_all_apis.py

# AI features
python tests/test_ai_features.py

# Preview functionality
python tests/test_preview.py
```

### Test Results
- **Overall Success Rate**: 85.7% (6/7 test files passing)
- **API Tests**: 88.2% success rate (15/17 tests)
- **Core API**: 100% success rate (7/7 tests)
- **AI Features**: 85.7% success rate (6/7 tests)
- **Preview Features**: 100% success rate (all formats working)

## 📚 Documentation

- **API Documentation**: `/docs` - Interactive API reference
- **Feature Guide**: `docs/FEATURES_IMPLEMENTED.md`
- **Preview Guide**: `docs/PREVIEW_FEATURES.md`
- **API System**: `docs/API_SYSTEM.md`

## 🛠️ Development

### Adding New Languages

1. Edit `highlight/languages.json`
2. Add language configuration with Pygments lexer
3. Restart the application

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python tests/run_tests.py`
5. Submit a pull request

## 🔧 Configuration

### Environment Variables

- `HUGGINGFACE_API_TOKEN` - Enable full AI features
- `SECRET_KEY` - Flask secret key (auto-generated if not set)
- `DATABASE_URL` - Database connection string (defaults to SQLite)

### Features Toggle

- **Rate Limiting**: Removed for better UX
- **AI Features**: Work with/without API token
- **Preview**: Automatic for Markdown, HTML, SVG
- **Authentication**: Optional for most features

## 🎯 Use Cases

- **Developers**: Code sharing with syntax highlighting and AI assistance
- **Teams**: Collaborative code review and sharing
- **Education**: Teaching with live code examples and explanations
- **Documentation**: Markdown preview for README files and docs
- **Prototyping**: Quick HTML/CSS/SVG testing and sharing

## 🔮 Roadmap

- [ ] API key authentication
- [ ] Webhook support
- [ ] Bulk operations
- [ ] Advanced search with filters
- [ ] Official SDKs (Python, JavaScript, Go)
- [ ] Real-time collaborative editing
- [ ] More AI models integration

## 📄 License

This project is open source. See the repository for license details.

## 🤝 Support

- **Issues**: GitHub Issues
- **Documentation**: `/docs` endpoint
- **API Help**: Interactive docs at `/docs`

---

**Built with ❤️ for the developer community**
