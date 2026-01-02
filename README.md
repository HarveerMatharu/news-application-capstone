# News Application - Django Capstone Project

A comprehensive Django-based news application with role-based access control, RESTful API, email notifications, and subscription system.

## Features

- **Custom User Model** with 3 roles: Reader, Editor, Journalist
- **Article Management** with approval workflow
- **Newsletter Management** - curated article collections
- **Publisher Management** - organize journalists and editors
- **Subscription System** - readers subscribe to publishers/journalists
- **RESTful API** with JWT authentication
- **Django Signals** for email and Twitter notifications
- **Web Interface** with responsive design
- **Comprehensive Unit Tests** (20+ tests)

## Technology Stack

- Django 5.0.1
- Django REST Framework 3.14.0
- MariaDB / SQLite
- JWT Authentication (Simple JWT)
- Docker
- Sphinx Documentation

## Project Structure

```
news_project/
├── news_project/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── news/                  # Main application
│   ├── models.py         # User, Article, Publisher, Newsletter models
│   ├── views.py          # API ViewSets
│   ├── web_views.py      # Web interface views
│   ├── serializers.py    # DRF serializers
│   ├── permissions.py    # Role-based permissions
│   ├── tasks.py          # Email and Twitter notification tasks
│   ├── urls.py           # URL routing
│   ├── admin.py          # Admin configuration
│   ├── tests.py          # Unit tests
│   ├── templates/        # HTML templates (13 files)
│   ├── static/           # CSS and static files
│   └── management/       # Custom management commands
├── docs/                  # Sphinx documentation
├── Dockerfile            # Docker configuration
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

### Prerequisites

- Python 3.11+
- MariaDB (or SQLite for development)
- Git
- Docker (optional)

### Option 1: Local Installation with Virtual Environment

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd news_project
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure database**

**For MariaDB (Production):**
```sql
CREATE DATABASE news_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'news_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON news_db.* TO 'news_user'@'localhost';
FLUSH PRIVILEGES;
```

Update `news_project/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'news_db',
        'USER': 'news_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

**For SQLite (Development):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Setup groups and permissions**
```bash
python manage.py setup_groups
```

7. **Create superuser**
```bash
python manage.py createsuperuser
```
Set the role to EDITOR via admin panel after creation.

8. **Run the development server**
```bash
python manage.py runserver
```

Access the application at: `http://localhost:8000`

### Option 2: Docker Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd news_project
```

2. **Build Docker image**
```bash
docker build -t news-app .
```

3. **Run Docker container**
```bash
docker run -p 8000:8000 news-app
```

Access the application at: `http://localhost:8000`

**Note:** Docker setup uses SQLite by default. For production with MariaDB, use Docker Compose (configuration not included).

## Configuration

### Environment Variables

For production, create a `.env` file (not tracked in Git):

```env
SECRET_KEY=your-secret-key-here
DATABASE_PASSWORD=your-database-password
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
TWITTER_BEARER_TOKEN=your-twitter-api-token
```

Update `settings.py` to use environment variables:
```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
```

### Test Users

After running setup_groups, create test users via admin panel:

- **editor1** (Role: EDITOR) - Can approve articles, manage content
- **journalist1** (Role: JOURNALIST) - Can create articles and newsletters
- **reader1** (Role: READER) - Can view content and manage subscriptions

Suggested password for testing: `testpass123`

## API Documentation

### Authentication

**Obtain JWT Token:**
```http
POST /api/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}

Response:
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Use Token:**
```http
Authorization: Bearer <access_token>
```

### Main API Endpoints

**Articles:**
- `GET /api/articles/` - List all approved articles
- `GET /api/articles/subscribed/` - Articles from subscriptions (readers)
- `GET /api/articles/<id>/` - Article detail
- `POST /api/articles/` - Create article (journalists)
- `PUT /api/articles/<id>/` - Update article
- `DELETE /api/articles/<id>/` - Delete article
- `POST /api/articles/<id>/approve/` - Approve article (editors)

**Newsletters:**
- `GET /api/newsletters/` - List all newsletters
- `GET /api/newsletters/<id>/` - Newsletter detail
- `POST /api/newsletters/` - Create newsletter (journalists/editors)
- `PUT /api/newsletters/<id>/` - Update newsletter
- `DELETE /api/newsletters/<id>/` - Delete newsletter

**Publishers:**
- `GET /api/publishers/` - List all publishers
- `GET /api/publishers/<id>/` - Publisher detail

**Users & Subscriptions:**
- `GET /api/users/me/` - Current user info
- `POST /api/users/<id>/subscribe_publisher/` - Subscribe to publisher
- `POST /api/users/<id>/subscribe_journalist/` - Subscribe to journalist

## Web Interface

### Main Pages

- `/` - Article list (role-based filtering)
- `/articles/subscribed/` - Personalized feed (readers)
- `/articles/pending/` - Pending approval (editors)
- `/articles/create/` - Create article (journalists)
- `/articles/<id>/` - Article detail
- `/newsletters/` - Newsletter list
- `/publishers/` - Publisher list
- `/subscriptions/` - Manage subscriptions (readers)

### User Roles

**Reader:**
- View approved articles and newsletters
- Subscribe to publishers and journalists
- View personalized article feed
- Cannot create content

**Journalist:**
- Create, edit, delete own articles
- Create, edit, delete own newsletters
- View all articles
- Cannot approve articles

**Editor:**
- View all articles (approved and pending)
- Approve articles
- Edit and delete any article
- Edit and delete any newsletter
- Cannot create articles (not a journalist)

## Testing

Run all tests:
```bash
python manage.py test news
```

Run with coverage:
```bash
pip install coverage
coverage run --source='.' manage.py test news
coverage report
```

Expected output: 20+ tests passing

## Documentation

Sphinx documentation is available in the `docs/` directory.

**View documentation:**
Open `docs/_build/html/index.html` in your browser.

**Rebuild documentation:**
```bash
cd docs
make html  # or .\make.bat html on Windows
```

## Django Signals

The application uses Django signals for automated notifications:

**Article Approval Signal:**
When an editor approves an article (`approved=True`):
1. Email notifications sent to all subscribers
2. Article posted to Twitter (if API credentials configured)

**Configuration:**
Update `news/tasks.py` with your email and Twitter credentials.

## Database Schema

**Main Models:**
- **User** - Custom user with role field and subscription relationships
- **Article** - News articles with approval workflow
- **Publisher** - Organizations with editors and journalists
- **Newsletter** - Curated collections of articles

**Relationships:**
- User → Articles (one-to-many as author)
- User → Publishers (many-to-many as subscribers)
- User → Journalists (many-to-many as subscribers)
- Publisher → Articles (one-to-many)
- Newsletter → Articles (many-to-many)

Database normalized to 3NF (Third Normal Form).

## Deployment Notes

### Security Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` in settings.py
- [ ] Set `DEBUG = False`
- [ ] Update `ALLOWED_HOSTS`
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS
- [ ] Configure proper database backup
- [ ] Set up proper email backend (not console)
- [ ] Configure Twitter API credentials
- [ ] Review and update CORS settings if needed

### Static Files

Collect static files for production:
```bash
python manage.py collectstatic
```

### Database Migrations

Always run migrations on deployment:
```bash
python manage.py migrate
```

## Troubleshooting

**Issue: mysqlclient installation fails**
- Solution: Install system dependencies first (on Ubuntu):
  ```bash
  sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
  ```

**Issue: Sphinx documentation fails to build**
- Solution: Temporarily switch to SQLite in settings.py when building docs

**Issue: Docker container can't connect to MariaDB**
- Solution: Use Docker Compose or configure Docker network properly


## License

Created as part of HyperionDev Django Backend Development Course (Level 3).

## Author

Harveer Matharu
January 2026

## Acknowledgments

- HyperionDev for course materials and project specifications
- Django and Django REST Framework documentation
