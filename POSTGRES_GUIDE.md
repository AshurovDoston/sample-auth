# Django PostgreSQL Migration Guide
## From SQLite to PostgreSQL: A Beginner's Learning Journey

> **Note**: This is a detailed learning-focused guide. For quick reference, see [CLAUDE.md](./CLAUDE.md) for project-specific configuration and commands.

---

## 📚 Table of Contents

1. [Why Switch to PostgreSQL?](#1-why-switch-to-postgresql)
2. [Understanding the Architecture](#2-understanding-the-architecture)
3. [Prerequisites Checklist](#3-prerequisites-checklist)
4. [Step 1: Install PostgreSQL](#step-1-install-postgresql)
5. [Step 2: Create Database and User](#step-2-create-database-and-user)
6. [Step 3: Install Python PostgreSQL Adapter](#step-3-install-python-postgresql-adapter)
7. [Step 4: Configure Django Settings](#step-4-configure-django-settings)
8. [Step 5: Migrate Your Data](#step-5-migrate-your-data)
9. [Step 6: Verify Everything Works](#step-6-verify-everything-works)
10. [Troubleshooting Common Errors](#troubleshooting-common-errors)
11. [Learning Checkpoints](#learning-checkpoints)

---

## 1. Why Switch to PostgreSQL?

### Learning Moment 💡
Before changing anything, understand **why** you're doing it:

| SQLite | PostgreSQL |
|--------|------------|
| File-based (db.sqlite3) | Server-based (runs as a service) |
| Great for development | Great for development AND production |
| Single user at a time | Multiple concurrent users |
| Limited data types | Rich data types (JSON, Arrays, etc.) |
| No user/permission system | Full user authentication & permissions |

### Real-World Use Case
Your to-do app with `age` and `phone` fields is perfect for PostgreSQL because:
- Phone numbers might need special validation
- You might want to add search functionality later
- Multiple users can access simultaneously
- Production servers expect PostgreSQL

---

## 2. Understanding the Architecture

### Learning Moment 💡
Here's what changes when you switch databases:

```
BEFORE (SQLite):
┌─────────────────┐
│  Django App     │
│  ↓              │
│  settings.py    │ ──→ db.sqlite3 (file in your project)
│  (SQLite)       │
└─────────────────┘

AFTER (PostgreSQL):
┌─────────────────┐     ┌──────────────────────┐
│  Django App     │     │  PostgreSQL Server   │
│  ↓              │     │  (separate service)  │
│  settings.py    │ ──→ │  ├── todoapp_db      │
│  (PostgreSQL)   │     │  └── other databases │
└─────────────────┘     └──────────────────────┘
```

**Key Insight**: PostgreSQL runs as a separate service on your computer. Django connects to it over a network port (default: 5432).

---

## 3. Prerequisites Checklist

Before starting, confirm you have:

- [ ] Python 3.x installed
- [ ] Django project working with SQLite
- [ ] Admin/sudo access on your computer
- [ ] Your existing migrations files (in `your_app/migrations/`)

### Check Your Current Setup
```bash
# Check Python version
python --version

# Check Django version
python -c "import django; print(django.VERSION)"

# Check if you have existing data
python manage.py shell
>>> from your_app.models import Task  # replace with your model
>>> Task.objects.count()
```

---

## Step 1: Install PostgreSQL

### On Windows:
1. Download from https://www.postgresql.org/download/windows/
2. Run the installer
3. Remember the password you set for the `postgres` user!
4. Keep default port: `5432`

### On macOS:
```bash
# Using Homebrew (recommended)
brew install postgresql@15
brew services start postgresql@15
```

### On Ubuntu/Linux:
```bash
# Update package list
sudo apt update

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Start the service
sudo systemctl start postgresql
sudo systemctl enable postgresql  # auto-start on boot
```

### Learning Moment 💡
**What just happened?**
- PostgreSQL is now installed as a **system service**
- It created a default user called `postgres` (superuser)
- It's listening on port `5432`
- Unlike SQLite, it runs continuously in the background

### Verify Installation:
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Or on macOS:
brew services list
```

---

## Step 2: Create Database and User

### Learning Moment 💡
**Why create a separate user?**
- Security: Don't use the superuser (`postgres`) for your app
- Isolation: Each project gets its own database and user
- Best Practice: Principle of least privilege

### Connect to PostgreSQL:
```bash
# Linux/macOS
sudo -u postgres psql

# Windows (open SQL Shell from Start Menu)
# or
psql -U postgres
```

You'll see a prompt like: `postgres=#`

### Create Database and User:
```sql
-- Step 2a: Create the database
CREATE DATABASE todoapp_db;

-- Step 2b: Create a user with password
CREATE USER todoapp_user WITH PASSWORD 'your_secure_password_here';

-- Step 2c: Configure the user (Django recommended settings)
ALTER ROLE todoapp_user SET client_encoding TO 'utf8';
ALTER ROLE todoapp_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE todoapp_user SET timezone TO 'UTC';

-- Step 2d: Grant permissions
GRANT ALL PRIVILEGES ON DATABASE todoapp_db TO todoapp_user;

-- Step 2e: For PostgreSQL 15+, grant schema permissions
\c todoapp_db
GRANT ALL ON SCHEMA public TO todoapp_user;

-- Exit psql
\q
```

### Understanding Each Command:

| Command | What It Does | Why It Matters |
|---------|--------------|----------------|
| `CREATE DATABASE` | Creates empty database | Your app's data container |
| `CREATE USER` | Creates login credentials | Separate from system users |
| `ALTER ROLE ... SET` | Sets defaults | Ensures Django compatibility |
| `GRANT ALL PRIVILEGES` | Gives full access | User can create/modify tables |
| `GRANT ALL ON SCHEMA` | Schema-level access | Required for PostgreSQL 15+ |

### Verify Your Database:
```bash
# Connect as your new user
psql -U todoapp_user -d todoapp_db -h localhost

# List databases (should see todoapp_db)
\l

# Exit
\q
```

---

## Step 3: Install Python PostgreSQL Adapter

### Learning Moment 💡
Django can't talk to PostgreSQL directly. It needs a "translator" called a PostgreSQL adapter.

```
Django ORM ←→ psycopg/psycopg2 ←→ PostgreSQL
             (adapter)
```

### Install the Adapter:
```bash
# Activate your virtual environment first!
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Option 1: psycopg (psycopg3) - Modern, recommended
pip install psycopg[binary]

# Option 2: psycopg2-binary (legacy, easier)
pip install psycopg2-binary

# Option 3: psycopg2 (legacy, production)
pip install psycopg2
```

### Which Package to Use?

| Package | Version | Use Case | Notes |
|---------|---------|----------|-------|
| `psycopg[binary]` | 3.x | **Recommended** - Modern Django projects | Latest version, better performance |
| `psycopg2-binary` | 2.x | Development, learning | Pre-compiled, easy install |
| `psycopg2` | 2.x | Production (legacy) | Compiled from source |

**Note**: This project uses `psycopg` (version 3.x) as seen in `requirements.txt`.

### Verify Installation:
```python
# For psycopg3:
python -c "import psycopg; print(psycopg.__version__)"

# For psycopg2:
python -c "import psycopg2; print(psycopg2.__version__)"
```

---

## Step 4: Configure Django Settings

### Learning Moment 💡
This is where you tell Django: "Stop using SQLite, start using PostgreSQL"

### Locate Your settings.py:
```
your_project/
├── manage.py
└── your_project/
    └── settings.py  ← Edit this file
```

### Find the DATABASES Section:

**BEFORE (SQLite - default):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**AFTER (PostgreSQL):**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'todoapp_db',
        'USER': 'todoapp_user',
        'PASSWORD': 'your_secure_password_here',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Understanding Each Setting:

| Setting | Value | Explanation |
|---------|-------|-------------|
| `ENGINE` | `django.db.backends.postgresql` | Which database driver to use |
| `NAME` | `todoapp_db` | Database name you created in Step 2 |
| `USER` | `todoapp_user` | Username you created |
| `PASSWORD` | Your password | The password from Step 2 |
| `HOST` | `localhost` | Where PostgreSQL runs (your machine) |
| `PORT` | `5432` | PostgreSQL's default port |

### 🔐 Security Best Practice: Use Environment Variables

**Don't hardcode passwords!** This project uses `python-decouple` for environment management.

**Step 1: Install python-decouple**
```bash
pip install python-decouple
```

**Step 2: Create a `.env` file** in your project root (same level as `manage.py`):
```env
# .env file
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=todoapp_db
DB_USER=todoapp_user
DB_PASSWORD=your_secure_password_here
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=127.0.0.1,localhost
```

**Step 3: Update settings.py** (this project already has this configured):
```python
from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

**Step 4: Add `.env` to `.gitignore`** to prevent committing secrets:
```bash
echo ".env" >> .gitignore
```

---

## Step 5: Migrate Your Data

### Learning Moment 💡
Your PostgreSQL database is empty. You need to:
1. Create all the tables (from your models)
2. Optionally transfer existing data from SQLite

### Option A: Fresh Start (No Existing Data)

```bash
# Create all tables in PostgreSQL
python manage.py migrate

# Create a superuser for admin access
python manage.py createsuperuser
```

### Option B: Transfer Existing Data from SQLite

If you have data you want to keep:

```bash
# Step 1: Export data from SQLite (while still using SQLite config)
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > data_backup.json

# Step 2: Now change settings.py to PostgreSQL (as shown in Step 4)

# Step 3: Run migrations on PostgreSQL
python manage.py migrate

# Step 4: Load data into PostgreSQL
python manage.py loaddata data_backup.json
```

### Understanding What Happens:

```
dumpdata:    Your Models → JSON file
             (exports all data)

migrate:     Your Models → PostgreSQL Tables
             (creates table structure)

loaddata:    JSON file → PostgreSQL Tables
             (imports all data)
```

---

## Step 6: Verify Everything Works

### Test 1: Check Database Connection
```bash
python manage.py check --database default
```

Expected output: `System check identified no issues`

### Test 2: Open Django Shell
```python
python manage.py shell

>>> from django.db import connection
>>> connection.vendor
'postgresql'  # Should say 'postgresql', not 'sqlite'
```

### Test 3: Run Your Server
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/admin/ and log in.

### Test 4: Check Your Models
```python
python manage.py shell

>>> from your_app.models import YourModel  # Replace with actual model
>>> YourModel.objects.all()
# Should show your data (or empty queryset if fresh start)
```

### Test 5: Verify in PostgreSQL Directly
```bash
psql -U todoapp_user -d todoapp_db -h localhost

# List all tables
\dt

# You should see tables like:
# - auth_user
# - django_migrations
# - your_app_yourmodel
# etc.

# Check your model's table
SELECT * FROM your_app_task;  # Replace with your table name

\q
```

---

## Troubleshooting Common Errors

### Error 1: "FATAL: password authentication failed"
```
django.db.utils.OperationalError: FATAL: password authentication failed for user "todoapp_user"
```

**Solutions:**
- Double-check password in settings.py
- Recreate user: `DROP USER todoapp_user;` then create again
- Check `pg_hba.conf` allows password authentication

### Error 2: "could not connect to server"
```
django.db.utils.OperationalError: could not connect to server: Connection refused
```

**Solutions:**
- Is PostgreSQL running? `sudo systemctl status postgresql`
- Check HOST is `localhost` or `127.0.0.1`
- Check PORT is `5432`

### Error 3: "relation does not exist"
```
django.db.utils.ProgrammingError: relation "your_app_task" does not exist
```

**Solutions:**
- Run migrations: `python manage.py migrate`
- Check you're connected to the right database

### Error 4: "permission denied for schema public"
```
django.db.utils.ProgrammingError: permission denied for schema public
```

**Solution (PostgreSQL 15+):**
```sql
sudo -u postgres psql
\c todoapp_db
GRANT ALL ON SCHEMA public TO todoapp_user;
\q
```

### Error 5: "psycopg2 not found"
```
ModuleNotFoundError: No module named 'psycopg2'
```

**Solutions:**
- Activate virtual environment first
- Install: `pip install psycopg2-binary`

---

## Learning Checkpoints

After completing this guide, you should be able to answer:

### Checkpoint 1: Basics
- [ ] What's the difference between SQLite and PostgreSQL?
- [ ] Why does Django need psycopg2?
- [ ] What port does PostgreSQL use by default?

### Checkpoint 2: Configuration
- [ ] What do each of the DATABASES settings mean?
- [ ] Why shouldn't you hardcode passwords?
- [ ] How do you set environment variables?

### Checkpoint 3: PostgreSQL Commands
- [ ] How do you connect to PostgreSQL? (`psql`)
- [ ] How do you list databases? (`\l`)
- [ ] How do you list tables? (`\dt`)
- [ ] How do you exit? (`\q`)

### Checkpoint 4: Django Commands
- [ ] What does `migrate` do?
- [ ] What does `dumpdata` do?
- [ ] What does `loaddata` do?

---

## Next Steps for Learning

Now that PostgreSQL is working, here are prompts to continue learning:

### 1. Explore PostgreSQL-Specific Features:
> "Show me how to use PostgreSQL's ArrayField in my Django model. I want to store multiple phone numbers for a user. Explain what ArrayField is and why SQLite doesn't support it."

### 2. Understand Database Indexes:
> "My to-do app is slow with many tasks. Explain what database indexes are and show me how to add one to my Task model's 'due_date' field in PostgreSQL."

### 3. Learn About Database Backups:
> "How do I backup my PostgreSQL database? Explain pg_dump and pg_restore with examples for my todoapp_db."

### 4. Explore Full-Text Search:
> "I want users to search their tasks. Show me how to implement full-text search using PostgreSQL's built-in features with Django's SearchVector."

---

## Quick Reference Card

```bash
# PostgreSQL Service
sudo systemctl start postgresql     # Start
sudo systemctl stop postgresql      # Stop
sudo systemctl status postgresql    # Check status

# Connect to PostgreSQL
sudo -u postgres psql               # As superuser
psql -U todoapp_user -d todoapp_db  # As your user

# Inside psql
\l                    # List databases
\c database_name      # Connect to database
\dt                   # List tables
\d table_name         # Describe table
\du                   # List users
\q                    # Quit

# Django Commands
python manage.py migrate            # Create tables
python manage.py dumpdata > data.json   # Export data
python manage.py loaddata data.json     # Import data
python manage.py dbshell            # Open database shell
```

---

**Congratulations!** 🎉 You've successfully migrated from SQLite to PostgreSQL while learning the fundamentals. This is a crucial skill for deploying Django applications to production.