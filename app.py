import os
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Optional
from pygments import highlight
from pygments.lexers import get_lexer_by_name, get_all_lexers
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import secrets
import string
import markdown
import bleach

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///dustbin.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    pastes = db.relationship('Paste', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Paste(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    title = db.Column(db.String(200), nullable=True)
    content = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(50), default='text')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    is_public = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    views = db.Column(db.Integer, default=0)

    def __init__(self, **kwargs):
        super(Paste, self).__init__(**kwargs)
        if not self.id:
            self.id = self.generate_id()

    def generate_id(self):
        """Generate a random 8-character ID"""
        chars = string.ascii_letters + string.digits
        return ''.join(secrets.choice(chars) for _ in range(8))

    def is_expired(self):
        if self.expires_at:
            return datetime.utcnow() > self.expires_at
        return False

    def get_highlighted_content(self):
        """Return syntax highlighted content"""
        try:
            # Get the correct Pygments lexer for this language
            pygments_lexer = get_pygments_lexer_for_language(self.language)
            lexer = get_lexer_by_name(pygments_lexer)
            formatter = HtmlFormatter(style='default', cssclass='highlight', linenos=True)
            return highlight(self.content, lexer, formatter)
        except ClassNotFound:
            # Fallback to plain text
            formatter = HtmlFormatter(style='default', cssclass='highlight', linenos=True)
            lexer = get_lexer_by_name('text')
            return highlight(self.content, lexer, formatter)

    def get_markdown_preview(self):
        """Return rendered Markdown content"""
        if self.language.lower() in ['markdown', 'md']:
            # Configure markdown with safe extensions
            md = markdown.Markdown(extensions=[
                'codehilite',
                'fenced_code',
                'tables',
                'toc',
                'nl2br'
            ])
            html = md.convert(self.content)
            # Sanitize HTML to prevent XSS
            allowed_tags = [
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'p', 'br', 'strong', 'em', 'u', 's', 'del',
                'ul', 'ol', 'li', 'blockquote', 'pre', 'code',
                'table', 'thead', 'tbody', 'tr', 'th', 'td',
                'a', 'img', 'hr', 'div', 'span'
            ]
            allowed_attributes = {
                'a': ['href', 'title'],
                'img': ['src', 'alt', 'title', 'width', 'height'],
                'code': ['class'],
                'div': ['class'],
                'span': ['class'],
                'pre': ['class']
            }
            return bleach.clean(html, tags=allowed_tags, attributes=allowed_attributes)
        return None

    def is_previewable(self):
        """Check if paste can be previewed"""
        return self.language.lower() in ['markdown', 'md', 'html', 'svg']

    def get_preview_type(self):
        """Get the type of preview available"""
        lang = self.language.lower()
        if lang in ['markdown', 'md']:
            return 'markdown'
        elif lang == 'html':
            return 'html'
        elif lang == 'svg':
            return 'svg'
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_stats():
    """Inject global statistics into templates"""
    try:
        total_pastes = Paste.query.count()
        total_users = User.query.count()
        return dict(total_pastes=total_pastes, total_users=total_users)
    except Exception:
        # Return default values if database is not ready
        return dict(total_pastes=0, total_users=0)

# Forms
class PasteForm(FlaskForm):
    title = StringField('Title (optional)', validators=[Optional(), Length(max=200)])
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={"rows": 20})
    language = SelectField('Language', choices=[], default='text')
    expires_in = SelectField('Expires in', choices=[
        ('never', 'Never'),
        ('10m', '10 minutes'),
        ('1h', '1 hour'),
        ('1d', '1 day'),
        ('1w', '1 week'),
        ('1M', '1 month')
    ], default='never')
    is_public = BooleanField('Public paste', default=True)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

# Helper functions
def load_language_config():
    """Load language configuration from JSON file"""
    try:
        with open('highlight/languages.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Fallback to basic languages if JSON file is missing
        return {
            "languages": [
                {"id": "text", "name": "Plain Text", "pygments_lexer": "text", "category": "text"},
                {"id": "python", "name": "Python", "pygments_lexer": "python", "category": "programming"},
                {"id": "javascript", "name": "JavaScript", "pygments_lexer": "javascript", "category": "web"},
                {"id": "html", "name": "HTML", "pygments_lexer": "html", "category": "web"},
                {"id": "css", "name": "CSS", "pygments_lexer": "css", "category": "web"},
                {"id": "json", "name": "JSON", "pygments_lexer": "json", "category": "data"}
            ],
            "categories": {"text": "Text", "programming": "Programming", "web": "Web", "data": "Data"}
        }

def get_language_choices():
    """Get list of available programming languages from JSON config"""
    config = load_language_config()
    languages = []

    # Group languages by category
    categories = {}
    for lang in config['languages']:
        category = lang.get('category', 'other')
        if category not in categories:
            categories[category] = []
        categories[category].append((lang['id'], lang['name']))

    # Add languages in order: text first, then by category
    if 'text' in categories:
        languages.extend(categories['text'])
        del categories['text']

    # Add other categories
    for category_id in sorted(categories.keys()):
        languages.extend(sorted(categories[category_id], key=lambda x: x[1]))

    return languages

def get_pygments_lexer_for_language(language_id):
    """Get the Pygments lexer name for a language ID"""
    config = load_language_config()
    for lang in config['languages']:
        if lang['id'] == language_id:
            return lang['pygments_lexer']
    return 'text'  # fallback



def calculate_expiry(expires_in):
    """Calculate expiry datetime based on selection"""
    if expires_in == 'never':
        return None
    
    now = datetime.utcnow()
    if expires_in == '10m':
        return now + timedelta(minutes=10)
    elif expires_in == '1h':
        return now + timedelta(hours=1)
    elif expires_in == '1d':
        return now + timedelta(days=1)
    elif expires_in == '1w':
        return now + timedelta(weeks=1)
    elif expires_in == '1M':
        return now + timedelta(days=30)
    return None

# Routes
@app.route('/')
def index():
    """Homepage with recent public pastes"""
    recent_pastes = Paste.query.filter_by(is_public=True).filter(
        (Paste.expires_at.is_(None)) | (Paste.expires_at > datetime.utcnow())
    ).order_by(Paste.created_at.desc()).limit(10).all()
    return render_template('index.html', pastes=recent_pastes)

@app.route('/new', methods=['GET', 'POST'])
def new_paste():
    """Create a new paste"""
    form = PasteForm()
    form.language.choices = get_language_choices()

    if form.validate_on_submit():
        paste = Paste(
            title=form.title.data or None,
            content=form.content.data,
            language=form.language.data,
            expires_at=calculate_expiry(form.expires_in.data),
            is_public=form.is_public.data,
            user_id=current_user.id if current_user.is_authenticated else None
        )
        db.session.add(paste)
        db.session.commit()
        flash('Paste created successfully!', 'success')
        return redirect(url_for('view_paste', paste_id=paste.id))

    return render_template('new_paste.html', form=form)

@app.route('/paste/<paste_id>')
def view_paste(paste_id):
    """View a specific paste"""
    paste = Paste.query.get_or_404(paste_id)

    # Check if paste is expired
    if paste.is_expired():
        abort(404)

    # Check if paste is private and user has access
    if not paste.is_public:
        if not current_user.is_authenticated or current_user.id != paste.user_id:
            abort(404)

    # Increment view count
    paste.views += 1
    db.session.commit()

    return render_template('view_paste.html', paste=paste)

@app.route('/paste/<paste_id>/raw')
def raw_paste(paste_id):
    """View raw paste content"""
    paste = Paste.query.get_or_404(paste_id)

    if paste.is_expired():
        abort(404)

    if not paste.is_public:
        if not current_user.is_authenticated or current_user.id != paste.user_id:
            abort(404)

    return paste.content, 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route('/paste/<paste_id>/preview')
def preview_paste(paste_id):
    """Preview paste content (Markdown, HTML, SVG)"""
    paste = Paste.query.get_or_404(paste_id)

    if paste.is_expired():
        abort(404)

    if not paste.is_public:
        if not current_user.is_authenticated or current_user.id != paste.user_id:
            abort(404)

    if not paste.is_previewable():
        abort(404)

    preview_type = paste.get_preview_type()

    if preview_type == 'markdown':
        markdown_html = paste.get_markdown_preview()
        return render_template('preview_markdown.html', paste=paste, markdown_html=markdown_html)

    elif preview_type == 'html':
        # For HTML, render in a sandboxed iframe
        return render_template('preview_html.html', paste=paste)

    elif preview_type == 'svg':
        # For SVG, render directly
        return render_template('preview_svg.html', paste=paste)

    abort(404)

@app.route('/paste/<paste_id>/preview/render')
def render_preview(paste_id):
    """Render HTML/SVG content in iframe"""
    paste = Paste.query.get_or_404(paste_id)

    if paste.is_expired():
        abort(404)

    if not paste.is_public:
        if not current_user.is_authenticated or current_user.id != paste.user_id:
            abort(404)

    preview_type = paste.get_preview_type()

    if preview_type == 'html':
        # Sanitize HTML content
        allowed_tags = [
            'html', 'head', 'body', 'title', 'meta', 'link', 'style',
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'br', 'hr',
            'strong', 'em', 'u', 's', 'del', 'ins', 'sub', 'sup',
            'ul', 'ol', 'li', 'dl', 'dt', 'dd', 'blockquote', 'pre', 'code',
            'table', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td', 'caption',
            'div', 'span', 'section', 'article', 'header', 'footer', 'nav', 'aside',
            'a', 'img', 'figure', 'figcaption', 'details', 'summary'
        ]
        allowed_attributes = {
            '*': ['class', 'id', 'style'],
            'a': ['href', 'title', 'target'],
            'img': ['src', 'alt', 'title', 'width', 'height'],
            'meta': ['charset', 'name', 'content'],
            'link': ['rel', 'href', 'type'],
        }
        clean_html = bleach.clean(paste.content, tags=allowed_tags, attributes=allowed_attributes)
        return Response(clean_html, mimetype='text/html')

    elif preview_type == 'svg':
        # For SVG, ensure it's valid SVG content
        content = paste.content.strip()
        if not content.startswith('<svg'):
            content = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">{content}</svg>'
        return Response(content, mimetype='image/svg+xml')

    abort(404)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        flash('Invalid username or password', 'error')

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists', 'error')
        elif User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'error')
        else:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/my-pastes')
@login_required
def my_pastes():
    """View user's pastes"""
    pastes = Paste.query.filter_by(user_id=current_user.id).order_by(
        Paste.created_at.desc()
    ).all()
    return render_template('my_pastes.html', pastes=pastes)

@app.route('/paste/<paste_id>/delete', methods=['POST'])
@login_required
def delete_paste(paste_id):
    """Delete a paste"""
    paste = Paste.query.get_or_404(paste_id)

    # Check if user owns the paste
    if current_user.id != paste.user_id:
        abort(403)

    db.session.delete(paste)
    db.session.commit()
    flash('Paste deleted successfully!', 'success')
    return redirect(url_for('my_pastes'))

@app.route('/paste/<paste_id>/fork')
def fork_paste(paste_id):
    """Fork a paste (create a copy)"""
    original_paste = Paste.query.get_or_404(paste_id)

    # Check if paste is expired or private
    if original_paste.is_expired():
        abort(404)

    if not original_paste.is_public:
        if not current_user.is_authenticated or current_user.id != original_paste.user_id:
            abort(404)

    # Pre-fill the form with original paste data
    form = PasteForm()
    form.language.choices = get_language_choices()
    form.title.data = f"Fork of {original_paste.title}" if original_paste.title else "Forked Paste"
    form.content.data = original_paste.content
    form.language.data = original_paste.language

    return render_template('new_paste.html', form=form, is_fork=True, original_id=paste_id)

@app.route('/api/paste/<paste_id>')
def api_paste(paste_id):
    """API endpoint to get paste data as JSON"""
    paste = Paste.query.get_or_404(paste_id)

    if paste.is_expired():
        abort(404)

    if not paste.is_public:
        if not current_user.is_authenticated or current_user.id != paste.user_id:
            abort(404)

    return jsonify({
        'id': paste.id,
        'title': paste.title,
        'content': paste.content,
        'language': paste.language,
        'created_at': paste.created_at.isoformat(),
        'expires_at': paste.expires_at.isoformat() if paste.expires_at else None,
        'is_public': paste.is_public,
        'views': paste.views,
        'author': paste.author.username if paste.author else None
    })

@app.route('/search')
def search():
    """Search pastes"""
    query = request.args.get('q', '').strip()
    if not query:
        return render_template('search.html', pastes=[], query='')

    # Search in public pastes only
    pastes = Paste.query.filter(
        Paste.is_public == True,
        (Paste.expires_at.is_(None)) | (Paste.expires_at > datetime.utcnow()),
        (Paste.title.contains(query)) | (Paste.content.contains(query))
    ).order_by(Paste.created_at.desc()).limit(50).all()

    return render_template('search.html', pastes=pastes, query=query)



@app.route('/languages')
def languages():
    """Show available languages and their categories"""
    config = load_language_config()
    return render_template('languages.html', config=config)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
