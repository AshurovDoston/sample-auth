# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django 6.0 To Do App with custom user authentication and task management. Features a custom user model extending AbstractUser, modern purple gradient UI, and organized static file structure. Uses PostgreSQL database with two main apps: `accounts` (authentication) and `home` (task management and landing page).

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

# Install dependencies
pip install -r requirements.txt
```

### PostgreSQL Database Setup
```bash
# Make sure PostgreSQL is installed and running
# The project uses PostgreSQL instead of SQLite

# Create the database (if not exists)
# psql -U postgres
# CREATE DATABASE your_db_name;

# After configuring .env with database credentials, run migrations
python manage.py migrate
```

**For detailed PostgreSQL migration guide**: See [POSTGRES_GUIDE.md](./POSTGRES_GUIDE.md) for comprehensive step-by-step instructions on:
- Installing and configuring PostgreSQL
- Creating database users with proper permissions
- Migrating from SQLite to PostgreSQL
- Data transfer and troubleshooting
- PostgreSQL-specific features and best practices

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
- `/tasks/<int:pk>/edit/` → Task edit form (home.urls)
- `/tasks/<int:pk>/delete/` → Task delete confirmation (home.urls)

**URL Parameters**: `<int:pk>` captures task ID from URL and passes to view as `pk` argument.

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
- `task_update_view`: Handles task editing with pre-populated form
- `task_delete_view`: Shows confirmation page before deleting task
- All views use `get_object_or_404(Task, pk=pk, user=request.user)` for security
- Uses `request.user.tasks.all()` to get user-specific tasks (via related_name)

**CRUD Patterns**:
```python
# CREATE: Set user before saving
task = form.save(commit=False)
task.user = request.user
task.save()

# UPDATE: Use instance parameter
form = TaskForm(request.POST, instance=task)
form.save()  # Updates existing task

# DELETE: Simple delete call
task.delete()
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
- `home.html` - Home page (authenticated: task list with edit/delete buttons, guest: landing page)
- `task_create.html` - Task creation form
- `task_update.html` - Task edit form (pre-populated with task data)
- `task_delete.html` - Task delete confirmation page
- `registration/login.html` - Login form
- `registration/signup.html` - User registration form
- `registration/logged_out.html` - Logout confirmation page

**Static Files** organized in `static/css/`:
- `base.css` - Global styles (navigation, forms, buttons, cards, utility classes)
- `reg.css` - Registration pages (login, signup, logged_out), task forms (create, update, delete)
- `home.css` - Home page, task list, edit/delete button styles

**CSS Architecture:**
- Each template loads base.css automatically via base.html
- Page-specific CSS loaded via `{% load static %}` and `<link>` tag in content block
- Uses CSS variables (`:root`) for theming: --primary-color, --secondary-color, --danger, etc.
- Purple gradient color scheme with modern card-based layouts
- **NO inline styles** - all styling in separate CSS files
- Task list uses semantic CSS classes: `.task-item`, `.task-status-badge`, `.task-edit-btn`, `.task-delete-btn`
- Delete confirmation uses: `.delete-warning`, `.delete-actions`, `.btn-danger`

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

### Database Architecture

The project uses **PostgreSQL** as the production database system (migrated from SQLite).

**Database Configuration** (`django_project/settings.py`):
- Engine: `django.db.backends.postgresql`
- Adapter: `psycopg` (psycopg3) - PostgreSQL database adapter for Python
- Configuration loaded from environment variables for security

**Key Benefits**:
- Multi-user concurrent access
- Advanced data types and indexing
- Full-text search capabilities
- Production-ready scalability
- User authentication and permissions at database level

**Common PostgreSQL Commands**:
```bash
# Connect to database
psql -U your_user -d your_db_name -h localhost

# Inside psql:
\l                    # List all databases
\dt                   # List tables
\d table_name         # Describe table structure
\q                    # Exit
```

### Environment Configuration
- Uses python-decouple for environment variables (`.env` file required)
- Required environment variables in `.env`:
  - `SECRET_KEY` - Django secret key for cryptographic signing
  - `DEBUG` - Boolean flag (True/False)
  - `DB_NAME` - PostgreSQL database name
  - `DB_USER` - PostgreSQL username
  - `DB_PASSWORD` - PostgreSQL password
  - `DB_HOST` - Database host (default: localhost)
  - `DB_PORT` - Database port (default: 5432)
  - `ALLOWED_HOSTS` - Comma-separated list of allowed hosts (default: 127.0.0.1)

### UI/UX Design Pattern
The app uses different views for authenticated vs. guest users on the home page:

**Authenticated Users:**
- Personalized welcome message with username
- Task list displaying all user's tasks
- Each task shows: title, description (if present), creation date, completion status
- Visual distinction: completed tasks have green border, pending have purple
- Action buttons on each task: Edit (purple), Delete (red)
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
- `redirect()` after successful form submission (PRG pattern - Post/Redirect/Get)
- `get_object_or_404()` for safe object retrieval with 404 on failure
- Context dictionary for passing data to templates
- URL parameters captured with `<int:pk>` and passed as view arguments

**Forms:**
- ModelForm for automatic form generation from models
- Custom widgets for HTML attributes
- Form validation with `is_valid()`
- `commit=False` pattern for CREATE (setting user field)
- `instance=` parameter for UPDATE (pre-populate and update existing object)
- Same form (TaskForm) used for both create and update views

**Templates:**
- Template inheritance with `{% extends %}`
- Template tags: `{% load static %}`, `{% url %}`
- Template filters: `{{ task.created_at|date:"M d, Y" }}`
- Conditional rendering: `{% if %}`, `{% for %}`

## Important Notes

- **Database Migration**: Project has migrated from SQLite to PostgreSQL. See [POSTGRES_GUIDE.md](./POSTGRES_GUIDE.md) for detailed migration instructions. PostgreSQL must be installed and running, and `.env` file must contain valid database credentials.
- **Custom User Model**: Uses `AUTH_USER_MODEL = "accounts.UserProfile"` - migrations must be run from start, cannot switch mid-project
- **ForeignKey Reference**: Always use `settings.AUTH_USER_MODEL` when creating ForeignKey to user, not direct User import
- **Security Pattern**: All task views filter by `user=request.user` to prevent users from accessing others' tasks
- **Environment Variables**: Never commit `.env` file or hardcode sensitive data (database passwords, SECRET_KEY). All configuration uses python-decouple.
- **Logout POST Requirement**: In Django 6.0+, logout must use POST method for security (implemented with form + CSRF token)
- **Delete Confirmation**: Delete operations use GET for confirmation page, POST for actual deletion
- **CSS Organization**: NO inline styles in templates - all styling in separate CSS files
- **Related Name Pattern**: Access user's tasks via `user.tasks.all()` (uses `related_name='tasks'` in Task model)
- **URL Naming**: Use `{% url 'name' %}` in templates, never hardcode URLs
- **Form Reusability**: Same ModelForm (TaskForm) used for both create and update operations
- **Database**: PostgreSQL (configured via environment variables)
- **Python version**: 3.13 (based on .venv)
- **Django version**: 6.0
- **Key Dependencies**: psycopg (PostgreSQL adapter), python-decouple (environment config), black (code formatter)
- Repository has two branches: `main` and `develop`
