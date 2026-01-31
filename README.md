
 🔐 Advanced Authentication System (FastAPI)

A production-ready authentication system built with FastAPI featuring JWT authentication, Redis-backed token revocation, email verification, password reset, background task processing using Celery, and MySQL persistence.

This project is designed as a modular and scalable auth service that can be plugged into any backend application.

🚀 Features

✅ JWT-based Authentication (Access & Refresh Tokens)

🔁 Refresh Token Rotation

🔒 Redis Token Blocklist (Logout Token Revocation)

📧 Email Verification System

🔑 Password Reset via Email

🧵 Background Tasks with Celery + Redis

🗄️ MySQL Database (Async SQLAlchemy / SQLModel)

🔐 Secure Password Hashing

🧩 Modular Architecture

📜 Centralized Logging

🛡️ Dependency-Based Route Protection

🏗️ Tech Stack

FastAPI

Python 3.11

MySQL

Redis

Celery

SQLModel / SQLAlchemy

JWT (JSON Web Tokens)

FastAPI-Mail

📁 Project Structure
📦src
 ┣ 📂Auth
 ┃ ┣ 📜Dependancy.py
 ┃ ┣ 📜routes.py
 ┃ ┣ 📜Schema.py
 ┃ ┣ 📜Services.py
 ┃ ┗ 📜utils.py
 ┣ 📂DB
 ┃ ┣ 📜Models.py
 ┃ ┣ 📜Redis.py
 ┃ ┗ 📜__init__.py
 ┣ 📜celery_task.py
 ┣ 📜config.py
 ┣ 📜logger.py
 ┣ 📜Mail.py
 ┣ 📜middleware.py
 ┣ 📜README.md
 ┗ 📜__init__.py



🔐 Authentication Flow
Login

User submits credentials

Password verified

Access Token + Refresh Token generated

Tokens returned to client

Protected Routes

JWT extracted from header

Signature validated

Token checked against Redis blocklist

Logout

Token JTI stored in Redis blocklist

Token becomes invalid instantly

🔁 Token Revocation Using Redis

When a user logs out:

Token JTI → Redis Set → Checked on every request


If present → request denied.

📧 Email Verification

User registers

Verification token generated

Email sent via Celery

User clicks verification link

Account marked as verified

🔑 Password Reset Flow

User requests password reset

Reset token emailed

User submits new password with token

Password updated securely

⚙️ Environment Variables

Create a .env file:

DATABASE_URL=mysql+aiomysql://root:root@localhost/DB_name
JWT_key=
Alogrithm=HS256
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_SERVER=
MAIL_PORT=
MAIL_FROM=
MAIL_FROM_NAME=
Domain=localhost:
URL_REDIS=
REDIS_PORT=
CELERY_BROKER_URL=
CELERY_RESULT_BACKEND=
BetterStack=(Optional)

🐳 Redis Using Docker
docker run -d -p 6379:6379 redis

🔄 Start Celery Worker
celery -A src.celery_task worker --loglevel=info

▶️ Run FastAPI Server
uvicorn src.main:app --reload

📌 API Endpoints (Example)
POST   /auth/sign_up
POST   /auth/login
POST   /auth/logout
GET    /auth/verify-email
POST   /auth/refresh
POST   /auth/request-password-reset
POST   /auth/reset-password

🔒 Security Practices Implemented

Password hashing (bcrypt)

Short-lived access tokens

Refresh token rotation

Redis-based token invalidation

Email verification before activation

Background tasks isolation

🧪 Development Notes

Async database sessions

Dependency injection used everywhere

Separation of concerns (Routes → Services → DB)

📈 Future Improvements

Device-based sessions

Admin Dashboard

Audit Logs

2FA / OTP
