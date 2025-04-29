# UNSW Seams (Backend Server)

> 🧵 A Microsoft Teams-inspired full-stack communication and collaboration tool, developed for UNSW's COMP1531 course.

This repository contains the **backend server** for UNSW Seams, providing a comprehensive API to support team messaging, collaboration, user management, analytics, and more.  
The backend is implemented using **Python (Flask)**, and interacts with a frontend React application ([Teams-Frontend](https://github.com/Manjot44/Teams-Frontend)).

---

## 🔗 Related Repositories
Please refer to the following repo if you wish to run this backend with the appropriate frontend. 
- [Teams-Frontend](https://github.com/Manjot44/Teams-Frontend) — Frontend React application for UNSW Seams

---

## 📚 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Backend Architecture](#backend-architecture)
- [API Overview](#api-overview)
- [Tech Stack](#tech-stack)
- [Installation & Setup](#installation--setup)
- [Running the Server](#running-the-server)
- [Testing](#testing)
- [Deployment](#deployment)
- [Team](#team)
- [License](#license)

---

## 🛠️ Features
- **User Authentication**: Register, login, logout, password reset
- **Channels**: Create channels, join, leave, invite members
- **Direct Messaging (DMs)**: Private one-on-one or group chats
- **Messaging**: Send, edit, delete, react to, and pin messages
- **Notifications**: Mention alerts, channel invites, and DM activities
- **Profile Management**: Update name, email, handle, profile picture
- **Standups**: Short-term, batch messaging sessions for teams
- **Scheduled Messages**: Send messages at a future scheduled time
- **Administrative Features**: Promote/demote owners, remove users, global user permissions
- **Analytics and Usage Stats**: User and workspace activity data

---

## ⚙️ Backend Architecture

```plaintext
/Teams-Project
│
├── src/                # Backend source code
│   ├── auth/           # User authentication and management
│   ├── channel/        # Channel functionalities
│   ├── dm/             # Direct messaging
│   ├── message/        # Messaging (send, edit, delete, react, schedule)
│   ├── notifications/  # Notifications system
│   ├── user/           # User profile management
│   ├── admin/          # Admin and workspace owner functions
│   ├── standup/        # Standup sessions
│   ├── other/          # Workspace statistics, search, user stats
│   ├── config.py       # Configuration (port settings etc.)
│   └── server.py       # Flask server and route definitions
│
├── tests/              # Pytest-based test suite
│
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

- Stateless design using tokens for authentication.
- Data is temporarily stored in-memory using Python data structures (dictionaries, lists).
- RESTful API endpoints using Flask routes.
- JSON used for request and response payloads.

---

## 🔌 API Overview

Sample of core API endpoints:

| Method | Endpoint | Description |
|:------|:---------|:------------|
| `POST` | `/auth/register/v2` | Register a new user |
| `POST` | `/auth/login/v2` | Login user |
| `POST` | `/channels/create/v2` | Create a new channel |
| `POST` | `/message/send/v1` | Send a message in a channel or DM |
| `GET` | `/notifications/get/v1` | Fetch user's notifications |
| `POST` | `/standup/start/v1` | Start a standup session |
| `POST` | `/message/sendlater/v1` | Schedule a message for future sending |
| `GET` | `/users/stats/v1` | User engagement statistics |

  For full API details and parameter lists, refer to the `src/README.md` file for the official project documentation.

---

## ⚙️ Tech Stack
- **Backend**: Python 3, Flask, Flask-CORS
- **Testing**: Pytest, Coverage.py
- **Version Control**: Git, GitHub

---

## 🚀 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/Manjot44/Teams-Project.git
cd Teams-Project
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 Running the Server
Run the Flask server locally:

```bash
python3 -m src.server
```

By default, the server runs on **http://localhost:5000**.  
If the port is busy, change the port number in `src/config.py`.

---

## 🧪 Testing

A full suite of unit and integration tests has been written using **pytest**.

### Run all tests:
```bash
pytest
```

### Run tests with coverage report:
```bash
coverage run -m pytest
coverage report
```

### Generate a coverage HTML report:
```bash
coverage html
```
Then open `htmlcov/index.html` in your browser to view detailed coverage.

Tests cover:
- User registration and login
- Channel operations
- Messaging functionalities
- Direct messages (DMs)
- Profile updates
- Admin controls
- Notifications and standup sessions
- Scheduled messaging

---

## 👨‍💻 Team
Contributors:
- Manjot Bhathal
- Jerry Lin
- Sanjam Singh
- Iqtidar Rahman
- Ashwin Sureshkumar 

---

## 📄 License
This project was developed as part of UNSW coursework and is for educational purposes only.

---
