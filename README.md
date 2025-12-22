# To Do App

A modern, full-featured task management application built with Django 6.0. Features custom user authentication, real-time task status toggling, and a vibrant orange-themed UI.

## Features

- **User Authentication**: Custom user model with registration, login, and logout
- **Task Management**: Full CRUD operations (Create, Read, Update, Delete)
- **Quick Status Toggle**: Mark tasks complete/incomplete directly from homepage with one click
- **Visual Feedback**: Color-coded status badges, card borders, and strikethrough effects
- **Responsive Design**: Mobile-friendly interface that works on all devices
- **Secure**: CSRF protection, user-specific data isolation, login-required views

## Tech Stack

- **Backend**: Django 6.0, Python 3.13
- **Database**: PostgreSQL (with psycopg adapter)
- **Frontend**: HTML5, CSS3 (custom styling with CSS variables)
- **Authentication**: Django's built-in auth system with custom UserProfile model

## Prerequisites

- Python 3.10+
- PostgreSQL
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd auth-project
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**
   ```bash
   # Connect to PostgreSQL
   sudo -u postgres psql

   # Create database and user
   CREATE DATABASE todoapp_db;
   CREATE USER todoapp_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE todoapp_db TO todoapp_user;
   \c todoapp_db
   GRANT ALL ON SCHEMA public TO todoapp_user;
   \q
   ```

5. **Configure environment variables**

   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DB_NAME=todoapp_db
   DB_USER=todoapp_user
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ALLOWED_HOSTS=127.0.0.1,localhost
   ```

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start the development server**
   ```bash
   python manage.py runserver
   ```

9. **Visit the app**

   Open http://127.0.0.1:8000 in your browser

## Usage

### For New Users
1. Click "Get Started" or "Sign Up" to create an account
2. Fill in your details (username, email, password)
3. Log in with your credentials

### Managing Tasks
- **Create**: Click "Add New Task" button on the homepage
- **Toggle Status**: Click the checkbox next to any task to mark it complete/incomplete
- **Edit**: Click the "Edit" button on any task card
- **Delete**: Click the "Delete" button and confirm

### Task States
- **Pending**: Orange border, unchecked checkbox, "Pending" badge
- **Completed**: Green border, checked checkbox, "Done" badge, strikethrough title

## Project Structure

```
auth-project/
├── accounts/           # User authentication app
│   ├── models.py       # Custom UserProfile model
│   ├── forms.py        # Registration form
│   └── views.py        # Signup view
├── home/               # Task management app
│   ├── models.py       # Task model
│   ├── forms.py        # Task form
│   ├── views.py        # Home, CRUD, and toggle views
│   └── urls.py         # App URL patterns
├── django_project/     # Project configuration
│   ├── settings.py     # Django settings
│   └── urls.py         # Root URL configuration
├── templates/          # HTML templates
│   ├── base.html       # Base template with navigation
│   ├── home.html       # Homepage with task list
│   └── registration/   # Auth templates
├── static/css/         # Stylesheets
│   ├── base.css        # Global styles and CSS variables
│   ├── home.css        # Task list styles
│   └── reg.css         # Registration page styles
├── requirements.txt    # Python dependencies
└── manage.py           # Django management script
```

## Development Commands

```bash
# Run development server
python manage.py runserver

# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run tests
python manage.py test

# Access Django shell
python manage.py shell

# Create superuser for admin access
python manage.py createsuperuser
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Required |
| `DEBUG` | Debug mode | `True` |
| `DB_NAME` | PostgreSQL database name | Required |
| `DB_USER` | PostgreSQL username | Required |
| `DB_PASSWORD` | PostgreSQL password | Required |
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `5432` |
| `ALLOWED_HOSTS` | Comma-separated hosts | `127.0.0.1` |

## Documentation

- [CLAUDE.md](./CLAUDE.md) - Developer guide and codebase documentation
- [POSTGRES_GUIDE.md](./POSTGRES_GUIDE.md) - PostgreSQL migration and setup guide

## License

This project is for educational purposes.
