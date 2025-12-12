# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django 6.0 To Do App with custom user authentication system. Features a custom user model extending AbstractUser, modern purple gradient UI, and organized static file structure. Uses SQLite database with two main apps: `accounts` (authentication) and `home` (landing page).

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
- Uses Django's built-in authentication views for login/logout/password management
- Custom signup view in accounts app
- **Logout requires POST**: Django 6.0 security - logout button uses form with CSRF token, not a link
- Navigation bar shows user status: authenticated users see username + logout button, guests see login/signup links

### Template & Static File Organization

**Templates** stored at project root in `templates/` directory:
- `base.html` - Base template with navigation, loads base.css
- `home.html` - Home page (authenticated: task section, guest: landing page)
- `registration/login.html` - Login form
- `registration/signup.html` - User registration form
- `registration/logged_out.html` - Logout confirmation page

**Static Files** organized in `static/css/`:
- `base.css` - Global styles (navigation, forms, buttons, cards, utility classes)
- `reg.css` - Registration pages only (login, signup, logged_out)
- `home.css` - Home page specific styles

**CSS Architecture:**
- Each template loads base.css automatically via base.html
- Page-specific CSS loaded via `{% load static %}` and `<link>` tag in content block
- Uses CSS variables (`:root`) for theming: --primary-color, --secondary-color, etc.
- Purple gradient color scheme with modern card-based layouts

Settings: `STATICFILES_DIRS = [BASE_DIR / "static"]` and `DIRS: [BASE_DIR / "templates"]`

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

### UI/UX Design Pattern
The app uses different views for authenticated vs. guest users on the home page:

**Authenticated Users:**
- Personalized welcome message with username
- Task management section (placeholder for future functionality)
- "Add New Task" button

**Guest Users:**
- Landing page with app description
- Call-to-action buttons ("Get Started", "Login")
- Feature list highlighting app benefits

## Important Notes

- **Custom User Model**: Uses `AUTH_USER_MODEL = "accounts.UserProfile"` - migrations must be run from start, cannot switch mid-project
- **Logout POST Requirement**: In Django 6.0+, logout must use POST method for security (implemented with form + CSRF token)
- **CSS Organization**: NO inline styles in templates - all styling in separate CSS files
- Database: SQLite (db.sqlite3)
- Python version: 3.13 (based on .venv)
- Django version: 6.0
- `ALLOWED_HOSTS = ["*"]` - should be restricted for production
- Repository has two branches: `main` and `develop`
