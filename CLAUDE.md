# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django 6.0 authentication project with custom user registration and profile management. Uses SQLite database and includes two main apps: `accounts` (authentication) and `home` (main content).

## Development Commands

### Run Development Server
```bash
python manage.py runserver
```

### Database Management
```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
```

### Testing
```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test accounts
python manage.py test home
```

### Django Shell
```bash
# Access Django shell for debugging/testing
python manage.py shell
```

### Virtual Environment
```bash
# Activate virtual environment (if not already active)
source .venv/bin/activate

# On Windows
.venv\Scripts\activate
```

## Project Architecture

### App Structure
- **accounts**: Handles user registration with custom signup form and UserProfile extension
- **home**: Main content/landing page views
- **django_project**: Project-level configuration (settings, URLs, WSGI/ASGI)
- **templates**: Shared HTML templates at project root level

### URL Routing Pattern
The project uses a hierarchical URL structure defined in `django_project/urls.py`:
- `/admin/` → Django admin interface
- `/accounts/` → Custom signup view (accounts.urls) + built-in auth views (login, logout, password management)
- `/` → Home page (home.urls)

Note: Both `accounts.urls` and `django.contrib.auth.urls` are included under `/accounts/` path.

### User Profile System
The project extends Django's built-in User model using a separate UserProfile model with a OneToOneField relationship rather than extending AbstractUser. This allows adding custom fields (like age) without replacing the User model.

Custom signup flow:
1. CustomUserCreationForm extends Django's UserCreationForm
2. Form includes additional age field not in base User model
3. On save, creates both User and linked UserProfile instances
4. UserProfile stores the age field

### Authentication Configuration
- `LOGIN_REDIRECT_URL = "/"` - redirects to home after login
- `LOGOUT_REDIRECT_URL = "/"` - redirects to home after logout
- Uses Django's built-in authentication views for login/logout
- Custom signup view in accounts app

### Template Organization
Templates stored at project root in `templates/` directory:
- `base.html` - Base template (likely contains common layout)
- `home.html` - Home page template
- `registration/login.html` - Login form
- `registration/signup.html` - Custom signup form

Settings configured with `DIRS: [BASE_DIR / "templates"]` to use project-level templates directory.

### Environment Configuration
- Uses python-decouple for environment variables (`.env` file exists)
- DEBUG setting loaded from environment with `config("DEBUG", default=True, cast=bool)`
- SECRET_KEY currently hardcoded (should be moved to .env for production)

## Important Notes

- Database: SQLite (db.sqlite3)
- Python version: 3.13 (based on .venv)
- Django version: 6.0
- `ALLOWED_HOSTS = ["*"]` - should be restricted for production
- Static files configured but no static directory currently exists in project root
