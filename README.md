# CITS3403-Agile_Web_Dev-Sports_Matchmaking

A sports matchmaking web application that connects athletes based on shared interests and skill levels. Built with Flask, featuring user authentication, event management, friend connections, and intelligent matching algorithms.

## Project Overview

This project consists of:

- **Backend**: Flask Python web application with user authentication and database management
- **Frontend**: HTML/CSS/JavaScript templates with dynamic functionality
- **Database**: SQLite (local development)
- **Testing**: Selenium integration tests for end-to-end workflows

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [macOS Setup](#macos-setup)
  - [Windows Setup](#windows-setup)
- [Python Dependencies](#python-dependencies)
- [Running the Application](#running-the-application)
- [Database Migrations](#database-migrations)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)


## Quick Start

**Choose your platform below:**

### macOS

```bash
brew install python && brew install --cask google-chrome
/opt/homebrew/bin/python3 -m pip install --break-system-packages flask flask-login flask-migrate flask-sqlalchemy flask-wtf werkzeug sqlalchemy alembic email-validator selenium webdriver-manager
flask run
```

Open http://127.0.0.1:5000

### Windows

```cmd
python -m venv venv
venv\Scripts\activate
pip install flask flask-login flask-migrate flask-sqlalchemy flask-wtf werkzeug sqlalchemy alembic email-validator selenium webdriver-manager
flask run
```

Open http://127.0.0.1:5000

## Prerequisites

### macOS

- macOS 10.14 or later
- Homebrew ([install here](https://brew.sh/))
- Python 3.8+ (via Homebrew)
- Google Chrome (for Selenium tests)

### Windows

- Windows 10 or later
- Python 3.8+ ([download here](https://www.python.org/downloads/))
- Google Chrome ([download here](https://www.google.com/chrome/))

Verify installation:

```bash
# macOS
/opt/homebrew/bin/python3 --version

# Windows
python --version
```

## Setup Instructions

### macOS Setup

**Step 1: Install Prerequisites**

```bash
brew install python
brew install --cask google-chrome
```

**Step 2: Navigate to Project Directory**

```bash
cd /Users/nmd/AGILE\ WEB\ DEV\ /Project1_ver1/My\ branch/ver_test_1
```

**Step 3: Install Python Dependencies**

```bash
/opt/homebrew/bin/python3 -m pip install --break-system-packages \
	flask flask-login flask-migrate flask-sqlalchemy flask-wtf \
	werkzeug sqlalchemy alembic email-validator \
	selenium webdriver-manager
```

**Step 4: Verify Installation**

```bash
/opt/homebrew/bin/python3 -c "import flask; print('Flask version:', flask.__version__)"
```

### Windows Setup

**Step 1: Install Prerequisites**

1. Download and install Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. Download and install Google Chrome from [google.com/chrome](https://www.google.com/chrome/)
3. Ensure Python is added to PATH during installation

**Step 2: Create Python Virtual Environment**

```cmd
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` appear in your command prompt when activated.

**Step 3: Install Python Dependencies**

```cmd
pip install flask flask-login flask-migrate flask-sqlalchemy flask-wtf werkzeug sqlalchemy alembic email-validator selenium webdriver-manager
```

**Step 4: Verify Installation**

```cmd
python -c "import flask; print('Flask version:', flask.__version__)"
```


## Python Dependencies

The project requires the following packages:

**Runtime Dependencies:**
- `flask`: Web framework
- `flask-login`: User session management
- `flask-migrate`: Database migrations with Alembic
- `flask-sqlalchemy`: SQL toolkit and ORM
- `flask-wtf`: CSRF protection and form handling
- `werkzeug`: WSGI utilities and security
- `sqlalchemy`: SQL toolkit and object-relational mapping
- `alembic`: Database schema migration tool
- `email-validator`: Email validation library

**Testing Dependencies:**
- `selenium`: Web automation for integration testing
- `webdriver-manager`: Automatic WebDriver management

### Installing Dependencies

**macOS:**

```bash
/opt/homebrew/bin/python3 -m pip install --break-system-packages \
	flask flask-login flask-migrate flask-sqlalchemy flask-wtf \
	werkzeug sqlalchemy alembic email-validator \
	selenium webdriver-manager
```

**Windows (with virtual environment activated):**

```cmd
pip install flask flask-login flask-migrate flask-sqlalchemy flask-wtf werkzeug sqlalchemy alembic email-validator selenium webdriver-manager
```


## Running the Application

Before running the application, ensure all dependencies are installed and you're in the project root directory.

### macOS

```bash
flask run
```

### Windows

With virtual environment activated:

```cmd
flask run
```

Or alternatively:

```cmd
python -m flask run
```

### Access the Application

Once the server is running, open your browser and navigate to:

- **Application URL**: http://127.0.0.1:5000
- **Default Port**: 5000

The application will reload automatically when you make code changes (development mode).


## Database Migrations

The project uses Alembic for managing database schema migrations alongside SQLAlchemy.

### Running Migrations

**macOS:**

```bash
/opt/homebrew/bin/python3 db_upgrade.sh
```

**Windows:**

```cmd
python db_upgrade.sh
```

### Downgrading Database

If needed, downgrade the database schema:

**macOS:**

```bash
/opt/homebrew/bin/python3 db_downgrade.sh
```

**Windows:**

```cmd
python db_downgrade.sh
```

## Running Tests

The project includes comprehensive Selenium integration tests for end-to-end testing of key workflows: user signup, profile management, event creation, and friend connections.

### Run Selenium Integration Tests (v2 - Recommended)

**macOS:**

```bash
/opt/homebrew/bin/python3 testing/integration_test.py -v
```

**Windows (with virtual environment activated):**

```cmd
python testing/integration_test.py -v
```

### Test Coverage

- **Signup & Profile Update**: User registration and profile completion
- **Login & Event Creation**: User authentication and event management
- **Friend Workflow**: Sending friend requests, accepting, and removing connections
- **Smoke Tests**: Homepage accessibility and basic functionality

### Run Unit Tests

**macOS:**
```bash
python3 -m unittest tests/test_models.py
```

**Windows:**
```bash
python -m unittest tests/test_models.py
```

### Test Coverage

#### UserModelTestCase

Tests the `Users` model:
- **test_password_hashing** — verifies correct password is accepted and wrong password is rejected
- **test_sports_property** — verifies the sports property returns the correct list of sports
- **test_get_id** — verifies `get_id()` returns a string as required by Flask-Login

#### MatchingScoreTestCase

Tests the `calculate_match_score` function:
- **test_match_score_one_common_sport** — users with 1 common sport and 1 postcode apart score 3
- **test_match_score_no_common_sport** — users with no common sports and 10 postcodes apart score 13
- **test_match_score_no_postcode** — verifies missing postcode is handled without crashing

#### MatchingModelTestCase

Tests the `Matching` model's `result` property — covers all Accept/Reject combinations:
- **test_matching_both_accept** — both accept returns `'Friends'`
- **test_matching_one_reject** — one rejects returns `'Skip'`
- **test_matching_both_reject** — both reject returns `'Skip'`
- **test_matching_first_rejects** — first user rejects returns `'Skip'`

#### RoutesTestCase

Tests Flask routes using the test client:
- **test_home_page** — homepage returns 200 OK
- **test_signup_page** — signing up creates a new user in the database
- **test_login_page** — correct credentials return 200 OK
- **test_friends_search_json** — friends search returns valid JSON with a `friends` key

## Project Structure

```
.
├── app/                          # Main Flask application
│   ├── __init__.py              # App initialization
│   ├── config.py                # Configuration settings
│   ├── forms.py                 # WTForms definitions
│   ├── models.py                # SQLAlchemy models (Users, Events, Friends, etc.)
│   ├── routes.py                # Flask route handlers
│   ├── static/                  # Static files
│   │   ├── css/                 # Stylesheets
│   │   └── js/                  # JavaScript files
│   └── templates/               # HTML templates
│       ├── base.html            # Base template
│       ├── homepage.html        # Home page
│       ├── user_profile_edit.html # Profile editor
│       ├── event_*.html         # Event-related templates
│       ├── friends_*.html       # Friend-related templates
│       └── matching.html        # Matching interface
├── migrations/                  # Alembic database migrations
│   └── versions/                # Migration scripts
├── testing/                     # Test suites
│   ├── __init__.py              # Package Folder
│   ├── integration_test.py      # Integration tests      
│   └── test_models.py           # Unit Tests
├── db_upgrade.sh                # Database upgrade script
├── db_downgrade.sh              # Database downgrade script
├── run.py                       # Application entry point
└── README.md                    # This file
```
