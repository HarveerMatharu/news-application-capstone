# News Application - Django Capstone Project

A comprehensive Django-based news application with role-based access control, RESTful API, email notifications, and social media integration.

## 📋 Features

- **Role-Based Access Control**: Three user roles (Reader, Editor, Journalist) with specific permissions
- **RESTful API**: Full CRUD operations with JWT authentication
- **Subscription System**: Readers can subscribe to publishers and journalists
- **Article Approval Workflow**: Editors approve articles before publication
- **Email Notifications**: Automatic email alerts to subscribers when articles are approved
- **Social Media Integration**: Automatic posting to X (formerly Twitter) upon article approval
- **Newsletter Management**: Curated collections of articles

## 🛠️ Technology Stack

- **Framework**: Django 5.0.1
- **API**: Django REST Framework 3.14.0
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: MariaDB (MySQL)
- **Email**: Django Email Backend
- **Social Media**: X (Twitter) API v2

## 📦 Installation

### Prerequisites

- Python 3.10+
- MariaDB 10.5+ (or MySQL 8.0+)
- pip
- virtualenv (recommended)

### Step 1: Clone & Setup Virtual Environment

```bash
# Create project directory
mkdir news_application
cd news_application

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Database Setup

```bash
# Create MariaDB database
mysql -u root -p
```

```sql
CREATE DATABASE news_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'news_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON news_db.* TO 'news_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Step 4: Configure Settings

Update `news_project/settings.py` with your database credentials and other settings:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'news_db',
        'USER': 'news_user',
        'PASSWORD': 'your_secure_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

Configure email settings (use console backend for development):

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Configure X (Twitter) API credentials (optional):

```python
TWITTER_BEARER_TOKEN = 'your-bearer-token'
```

### Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Setup Groups & Permissions

```bash
python manage.py setup_groups
```

### Step 7: Create Superuser

```bash
python manage.py createsuperuser
```

### Step 8: Run Development Server

```bash
python manage.py runserver
```

Access the application at: `http://localhost:8000`

## 📚 API Documentation

### Authentication

#### Obtain JWT Token
```http
POST /api/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

**Response:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Use Token in Requests
```http
GET /api/articles/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Article Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/articles/` | List all approved articles | All authenticated users |
| GET | `/api/articles/subscribed/` | User's subscribed content | Readers only |
| GET | `/api/articles/<id>/` | Single article detail | All authenticated users |
| POST | `/api/articles/` | Create new article | Journalists only |
| PUT | `/api/articles/<id>/` | Update article | Editors & Journalists |
| DELETE | `/api/articles/<id>/` | Delete article | Editors & Journalists |
| POST | `/api/articles/<id>/approve/` | Approve article | Editors only |

### Newsletter Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/newsletters/` | List all newsletters | All authenticated users |
| GET | `/api/newsletters/<id>/` | Single newsletter detail | All authenticated users |
| POST | `/api/newsletters/` | Create newsletter | Editors & Journalists |
| PUT | `/api/newsletters/<id>/` | Update newsletter | Editors & Journalists |
| DELETE | `/api/newsletters/<id>/` | Delete newsletter | Editors & Journalists |

### Example API Calls

#### Create Article (Journalist)
```bash
curl -X POST http://localhost:8000/api/articles/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Breaking News",
    "content": "This is the article content...",
    "publisher_id": 1
  }'
```

#### Approve Article (Editor)
```bash
curl -X POST http://localhost:8000/api/articles/1/approve/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### Get Subscribed Articles (Reader)
```bash
curl http://localhost:8000/api/articles/subscribed/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 👥 User Roles & Permissions

### Reader
- View approved articles
- View newsletters
- Subscribe to publishers and journalists
- Access subscribed content

### Journalist
- All Reader permissions
- Create articles
- Edit own articles
- Delete own articles
- Create newsletters
- Edit own newsletters

### Editor
- View all articles (approved and unapproved)
- Approve articles
- Edit any article
- Delete any article
- Edit any newsletter
- Delete any newsletter

## 🧪 Running Tests

```bash
# Run all tests
python manage.py test news

# Run with coverage
coverage run --source='news' manage.py test news
coverage report
```

### Test Coverage

The test suite includes:
- User model and role assignment tests
- Article API endpoint tests
- Subscription functionality tests
- Newsletter API tests
- Signal functionality tests (email & Twitter)
- JWT authentication tests

## 🗂️ Project Structure

```
news_application/
├── news_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── news/
│   ├── migrations/
│   ├── management/
│   │   └── commands/
│   │       └── setup_groups.py
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── tasks.py
│   ├── admin.py
│   ├── urls.py
│   └── tests.py
├── requirements.txt
└── README.md
```

## 🔧 Configuration

### Email Configuration

For production, use SMTP:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### X (Twitter) API Setup

1. Create a Twitter Developer account
2. Create an app and generate credentials
3. Add credentials to settings:

```python
TWITTER_BEARER_TOKEN = 'your-bearer-token'
```

## 📝 Implementation Notes

### Signals vs View-Based Logic

This project uses **Django Signals** (Option 1) for article approval notifications:
- `post_save` signal on Article model
- Automatically sends emails to subscribers
- Automatically posts to X (Twitter)
- Keeps views clean and follows separation of concerns

### Database Normalization

The database schema is normalized to 3NF:
- Users table with role-based fields
- Articles table with foreign keys
- Publishers table with many-to-many relationships
- Newsletters table with many-to-many to articles
- Subscription tables (through relationships)

### Security Considerations

- JWT authentication with token expiration
- Role-based access control at API level
- Permission checks at view level
- CSRF protection enabled
- SQL injection protection (Django ORM)

## 👨‍💻 Author

Harveer Matharu
