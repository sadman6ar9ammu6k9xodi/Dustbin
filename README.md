# Dustbin - Simple Pastebin Service

A modern, feature-rich pastebin service built with Python Flask. Share code snippets, logs, and text with syntax highlighting, expiration options, and user accounts.

## Features

- 🎨 **Syntax Highlighting** - Support for 100+ programming languages
- ⏰ **Paste Expiration** - Set automatic deletion times (10 minutes to 1 month)
- 🔒 **Privacy Controls** - Public and private pastes
- 👤 **User Accounts** - Registration, login, and paste history
- 🔍 **Search** - Find public pastes by title or content
- 📱 **Mobile Friendly** - Responsive design works on all devices
- 🍴 **Fork Pastes** - Create copies of existing pastes
- 📊 **Statistics** - View counts and user stats
- 🔗 **API Access** - JSON API for paste data
- 📥 **Download** - Save pastes as files

## Quick Start

1. **Clone and setup**:
   ```bash
   git clone <repository>
   cd dustbin
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Visit** http://127.0.0.1:5000

## Configuration

Edit the `.env` file to configure:

- `SECRET_KEY` - Flask secret key (change in production!)
- `DATABASE_URL` - Database connection string
- `FLASK_ENV` - Environment (development/production)
- `FLASK_DEBUG` - Debug mode (True/False)

## API Endpoints

- `GET /api/paste/<id>` - Get paste data as JSON
- `GET /paste/<id>/raw` - Get raw paste content

## File Structure

```
dustbin/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env               # Environment configuration
├── templates/         # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── new_paste.html
│   ├── view_paste.html
│   ├── login.html
│   ├── register.html
│   ├── my_pastes.html
│   └── search.html
└── static/           # Static assets
    └── css/
        └── style.css
```

## Database Schema

### Users
- `id` - Primary key
- `username` - Unique username
- `email` - User email
- `password_hash` - Hashed password
- `created_at` - Registration date

### Pastes
- `id` - 8-character unique ID
- `title` - Optional paste title
- `content` - Paste content
- `language` - Programming language for highlighting
- `created_at` - Creation timestamp
- `expires_at` - Optional expiration time
- `is_public` - Public/private flag
- `user_id` - Owner (optional)
- `views` - View count

## Technologies Used

- **Backend**: Python Flask
- **Database**: SQLAlchemy (SQLite by default)
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Syntax Highlighting**: Pygments
- **Frontend**: Bootstrap 5
- **Icons**: Font Awesome

## Development

To contribute or modify:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Security Notes

- Change the `SECRET_KEY` in production
- Use a proper database (PostgreSQL/MySQL) for production
- Consider rate limiting for public instances
- Implement CSRF protection (included via Flask-WTF)
- Use HTTPS in production

## Deployment

For production deployment:

1. Use a production WSGI server (gunicorn, uWSGI)
2. Set up a reverse proxy (nginx, Apache)
3. Use a production database
4. Configure proper logging
5. Set up SSL/TLS certificates
6. Consider using a CDN for static assets

Example with gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```
