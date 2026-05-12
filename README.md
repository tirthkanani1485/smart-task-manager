# Smart Task Management System

## Project Overview

This is a Flask-based Smart Task Management System developed using:

- Python
- Flask
- PostgreSQL
- REST APIs
- Pandas & NumPy
- WebSockets
- HTML/CSS

The application allows users to:
- Register/Login
- Add Tasks
- Delete Tasks
- View Analytics
- Get Real-time Updates

---

# Features

## Authentication
- User Registration
- User Login
- Logout

## Task Management
- Add Task
- Delete Task
- View Tasks

## Analytics
- Total Tasks
- Completed Tasks
- Pending Tasks
- Completion Percentage

## WebSocket
- Real-time task notifications

---

# Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-SocketIO
- PostgreSQL
- Pandas
- NumPy
- HTML
- CSS

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <repository-link>
```

## 2. Create Virtual Environment

```bash
python -m venv venv
```

## 3. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

## 4. Install Dependencies

```bash
pip install flask flask_sqlalchemy flask_login flask_socketio psycopg2-binary pandas numpy
```

## 5. Create PostgreSQL Database

Database Name:

```text
taskdb
```

## 6. Run Application

```bash
python app.py
```

---

# Project Structure

```text
smart-task-manager/
│
├── app.py
├── README.md
├── database_schema.sql
│
├── templates/
│   ├── login.html
│   ├── register.html
│   └── index.html
│
├── static/
│   └── style.css
```

---

# Author

Tirth Kanani
