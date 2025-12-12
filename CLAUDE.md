# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django 6.0 authentication project with custom user model extending AbstractUser. Uses SQLite database and includes two main apps: `accounts` (custom authentication with UserProfile model) and `home` (main content).

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

### Custom User Model
The project uses a custom user model (`UserProfile`) that extends `AbstractUser`. This is configured via `AUTH_USER_MODEL = "accounts.UserProfile"` in settings.

**IMPORTANT**: This project replaces Django's default User model entirely. Do not use `django.contrib.auth.models.User` directly.

Custom fields added to UserProfile:
- `age` - PositiveIntegerField (optional)
- `phone` - CharField max_length=15 (optional)

Custom signup flow:
1. CustomUserCreationForm extends Django's UserCreationForm
2. Form's Meta.model points to UserProfile (not User)
3. Includes fields: email, username, age, first_name, last_name, phone, password1, password2
4. Creates UserProfile instance directly (no separate profile creation needed)

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

### Admin Configuration
The UserProfile model is registered in Django admin with a custom admin class that extends `UserAdmin`:
- Adds custom fieldsets for age and phone fields
- Custom fieldsets labeled "Qo'shimcha Info" (Additional Info in Uzbek) and "Additional Info"
- Displays age and phone in list view

### Environment Configuration
- Uses python-decouple for environment variables (`.env` file exists)
- DEBUG setting loaded from environment with `config("DEBUG", default=True, cast=bool)`
- SECRET_KEY currently hardcoded in settings.py (should be moved to .env for production)
- Current .env only contains: `DEBUG = True`

## Important Notes

- **Custom User Model**: Uses `AUTH_USER_MODEL = "accounts.UserProfile"` - migrations must be run from start, cannot switch mid-project
- Database: SQLite (db.sqlite3)
- Python version: 3.13 (based on .venv)
- Django version: 6.0
- `ALLOWED_HOSTS = ["*"]` - should be restricted for production
- Static files configured but no static directory currently exists in project root
- Repository has two branches: `main` and `develop`
