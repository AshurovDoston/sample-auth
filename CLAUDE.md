# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django 6.0 To Do App with custom user authentication and task management. Features a custom user model extending AbstractUser, modern purple gradient UI, and organized static file structure. Uses SQLite database with two main apps: `accounts` (authentication) and `home` (task management and landing page).

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
- **home**: Task management (CRUD operations) and landing page views
- **django_project**: Project-level configuration (settings, URLs, WSGI/ASGI)
- **templates**: Shared HTML templates at project root level
- **static**: CSS files organized by purpose (base, reg, home)

### URL Routing Pattern
The project uses a hierarchical URL structure defined in `django_project/urls.py`:
- `/admin/` → Django admin interface
- `/accounts/` → Custom signup view (accounts.urls) + built-in auth views (login, logout, password management)
- `/` → Home page (home.urls)
- `/tasks/create/` → Task creation form (home.urls)

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

### Task Management System

**Task Model** (`home/models.py`):
- Links to UserProfile via ForeignKey with `related_name='tasks'`
- Fields: title (CharField), description (TextField, optional), completed (BooleanField)
- Auto-timestamps: created_at, updated_at
- Ordered by creation date (newest first)

**Task Form** (`home/forms.py`):
- Uses ModelForm pattern for automatic form generation from Task model
- Excludes user field (set automatically in view)
- Custom widgets for better UX (placeholders, CSS classes)
- Help text for user guidance

**Task Views** (`home/views.py`):
- `home_view`: Shows task list for authenticated users, landing page for guests
- `task_create_view`: Handles task creation with `@login_required` decorator
- Uses `request.user.tasks.all()` to get user-specific tasks (via related_name)

**Key Pattern**:
```python
# In view:
task = form.save(commit=False)  # Create object without saving
task.user = request.user        # Set user field
task.save()                     # Save to database
```

### Authentication Configuration
- `LOGIN_REDIRECT_URL = "/"` - redirects to home after login
- `LOGOUT_REDIRECT_URL = "/accounts/logout/"` - redirects to logout confirmation
- `LOGIN_URL = "/accounts/login/"` - where @login_required redirects
- Uses Django's built-in authentication views for login/logout/password management
- Custom signup view in accounts app
- **Logout requires POST**: Django 6.0 security - logout button uses form with CSRF token, not a link
- Navigation bar shows user status: authenticated users see username + logout button, guests see login/signup links

### Template & Static File Organization

**Templates** stored at project root in `templates/` directory:
- `base.html` - Base template with navigation, loads base.css
- `home.html` - Home page (authenticated: task list, guest: landing page)
- `task_create.html` - Task creation form
- `registration/login.html` - Login form
- `registration/signup.html` - User registration form
- `registration/logged_out.html` - Logout confirmation page

**Static Files** organized in `static/css/`:
- `base.css` - Global styles (navigation, forms, buttons, cards, utility classes)
- `reg.css` - Registration pages (login, signup, logged_out) and task_create form
- `home.css` - Home page and task list styles

**CSS Architecture:**
- Each template loads base.css automatically via base.html
- Page-specific CSS loaded via `{% load static %}` and `<link>` tag in content block
- Uses CSS variables (`:root`) for theming: --primary-color, --secondary-color, etc.
- Purple gradient color scheme with modern card-based layouts
- **NO inline styles** - all styling in separate CSS files
- Task list uses semantic CSS classes: `.task-item`, `.task-status-badge`, etc.

Settings: `STATICFILES_DIRS = [BASE_DIR / "static"]` and `DIRS: [BASE_DIR / "templates"]`

### Admin Configuration

**UserProfile** in `accounts/admin.py`:
- Extends UserAdmin
- Adds custom fieldsets for age and phone fields
- Custom fieldsets labeled "Qo'shimcha Info" (Additional Info in Uzbek) and "Additional Info"
- Displays age and phone in list view

**Task** in `home/admin.py`:
- Custom list_display: title, user, completed, created_at
- Filters: completed, created_at
- Search: title, description
- Read-only: created_at, updated_at

### Environment Configuration
- Uses python-decouple for environment variables (`.env` file exists)
- DEBUG setting loaded from environment with `config("DEBUG", default=True, cast=bool)`
- SECRET_KEY currently hardcoded in settings.py (should be moved to .env for production)
- Current .env only contains: `DEBUG = True`

### UI/UX Design Pattern
The app uses different views for authenticated vs. guest users on the home page:

**Authenticated Users:**
- Personalized welcome message with username
- Task list displaying all user's tasks
- Each task shows: title, description (if present), creation date, completion status
- Visual distinction: completed tasks have green border, pending have purple
- "Add New Task" button links to `/tasks/create/`

**Guest Users:**
- Landing page with app description
- Call-to-action buttons ("Get Started", "Login")
- Feature list highlighting app benefits

**Form Pattern:**
- All forms use Django ModelForm pattern
- CSRF protection required on all POST forms
- Forms use `form.save(commit=False)` when additional data needs to be set before saving
- Validation errors displayed automatically by Django

### Django Patterns Used

**Models:**
- ForeignKey relationships with `related_name` for reverse lookups
- `settings.AUTH_USER_MODEL` reference instead of hardcoded User model
- Auto-timestamps with `auto_now_add` and `auto_now`
- Model `Meta` class for ordering and display names

**Views:**
- Function-based views (FBV) pattern
- `@login_required` decorator for protected views
- GET vs POST request handling
- `redirect()` after successful form submission (PRG pattern)
- Context dictionary for passing data to templates

**Forms:**
- ModelForm for automatic form generation from models
- Custom widgets for HTML attributes
- Form validation with `is_valid()`
- `commit=False` pattern for setting additional fields

**Templates:**
- Template inheritance with `{% extends %}`
- Template tags: `{% load static %}`, `{% url %}`
- Template filters: `{{ task.created_at|date:"M d, Y" }}`
- Conditional rendering: `{% if %}`, `{% for %}`

## Important Notes

- **Custom User Model**: Uses `AUTH_USER_MODEL = "accounts.UserProfile"` - migrations must be run from start, cannot switch mid-project
- **ForeignKey Reference**: Always use `settings.AUTH_USER_MODEL` when creating ForeignKey to user, not direct User import
- **Logout POST Requirement**: In Django 6.0+, logout must use POST method for security (implemented with form + CSRF token)
- **CSS Organization**: NO inline styles in templates - all styling in separate CSS files
- **Related Name Pattern**: Access user's tasks via `user.tasks.all()` (uses `related_name='tasks'` in Task model)
- Database: SQLite (db.sqlite3)
- Python version: 3.13 (based on .venv)
- Django version: 6.0
- `ALLOWED_HOSTS = ["*"]` - should be restricted for production
- Repository has two branches: `main` and `develop`
