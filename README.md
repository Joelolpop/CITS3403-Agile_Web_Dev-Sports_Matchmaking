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
