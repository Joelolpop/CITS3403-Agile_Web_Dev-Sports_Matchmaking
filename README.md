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
