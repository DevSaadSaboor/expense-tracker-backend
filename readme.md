<div align="center">
# 💰 Expense Tracker API
</div>
### A production-grade backend API for a personal expense tracking application, built with FastAPI, raw SQL, and JWT-based authentication with refresh tokens.
This project is designed with clean architecture, security, and real-world backend practices in mind.
---

## 🌟 Features

<table>
<tr>
<td width="50%">

### 🔐 Authentication

- ✅ User registration & login
- ✅ JWT access tokens (short-lived)
- ✅ Refresh tokens with rotation
- ✅ Session revocation (logout)
- ✅ Secure password hashing (bcrypt)

</td>
<td width="50%">

### 📊 Data Management

- ✅ Expense & category management
- ✅ Monthly & category-wise reports
- ✅ Pagination support
- ✅ Raw SQL queries (no ORM)
- ✅ PostgreSQL database

</td>
</tr>
<tr>
<td width="50%">

### 🏗️ Infrastructure

- ✅ Dockerized setup
- ✅ Alembic migrations
- ✅ Clean architecture
- ✅ Environment configuration
- ✅ API documentation (Swagger)

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.9+ (for local development)

### 🐳 Run with Docker (Recommended)

```bash

# Start the application
docker compose up --build
```

**🎉 That's it!** The API is now running at:

- 📖 **Swagger UI:** http://localhost:8000/docs

## 💻 Local Development

### Without Docker

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

---

## 🛠 Tech Stack

<div align="center">

FastAPI – Web framework
PostgreSQL – Database
psycopg2 – Raw SQL driver
Alembic – Schema migrations
Docker & Docker Compose – Containerization
python-jose – JWT handling
bcrypt – Password hashing

</div>

---

## 🏗️ Architecture

```
expense-tracker-api/
│
├── 📁 api/                    # FastAPI routes & request/response models
│   ├── auth.py               # Authentication endpoints
│   ├── expenses.py           # Expense endpoints
│   └── categories.py         # Category endpoints
│
├── 📁 service/                # Business logic & validation
│   ├── auth_service.py
│   ├── expense_service.py
│   └── category_service.py
│
├── 📁 storage/                # Raw SQL repositories
│   ├── user_repository.py
│   ├── expense_repository.py
│   └── category_repository.py
│
├── 📁 core/                   # Security, auth, shared utilities
│   ├── security.py
│   ├── config.py
│   └── dependencies.py
│
├── 📁 migrations/             # Alembic database migrations
│   └── versions/
│
├── 🐳 Dockerfile
├── 🐳 docker-compose.yml
├── 📄 requirements.txt
└── 📄 .env.example
```

### Layered Designs

- **API Layer:** Handles HTTP requests/responses, validation
- **Service Layer:** Business rules, authentication, authorization
- **Storage Layer:** Database operations, raw SQL queries

---

## 🔐 Authentication System

### Token Architecture

<div align="center">

| Token Type           | Purpose                 | Lifetime    |
| -------------------- | ----------------------- | ----------- |
| 🎫 **Access Token**  | Authorize API requests  | Short Lived |
| 🔄 **Refresh Token** | Issue new access tokens | Long Lived  |

</div>
Refresh tokens:
Are stored in the database
Are rotated on every refresh
Are revoked on logout
Are checked for expiration and revocation

### 🔄 Authentication Flow

User logs in → receives access token + refresh token
Access token is used for API requests
When access token expires → client sends refresh token
Backend validates and rotates the refresh token
New access + refresh tokens are issued
Logout revokes the refresh token in the database

````

---

## 📚 API Endpoints

### 🔐 Authentication

```http
POST   /auth/register          Create new user account
POST   /auth/login             Login and receive tokens
POST   /auth/refresh           Rotate refresh token
POST   /auth/logout            Revoke refresh token and logout
````

### 💰 Expenses

```http
GET    /expenses               List expenses (paginated)
POST   /expenses               Create new expense
GET    /expenses/{id}          Get expense by ID
PUT    /expenses/{id}          Update expense
DELETE /expenses/{id}          Delete expense
```

### 🏷️ Categories

```http
GET    /categories             List all categories
POST   /categories             Create new category
```

### 🔒 Protected Endpoints

All endpoints except `/auth/register` and `/auth/login` require authentication:

```http
Authorization: Bearer <access_token>
```

---

## 🗄️ Database Schema

```sql
┌─────────────────────┐
│       users         │
├─────────────────────┤
│ id (PK)             │
│ name                │
│ email (UNIQUE)      │
│ password_hash       │
│ created_at          │
└─────────────────────┘
          │
          │
          ▼
┌─────────────────────┐       ┌─────────────────────┐
│    categories       │       │   refresh_tokens    │
├─────────────────────┤       ├─────────────────────┤
│ id (PK)             │       │ id (PK)             │
│ user_id (FK)        │       │ user_id (FK)        │
│ name                │       │ token               │
│ created_at          │       │ expires_at          │
└─────────────────────┘       │ revoked             │
          │                   │ created_at          │
          │                   └─────────────────────┘
          ▼
┌─────────────────────┐
│      expenses       │
├─────────────────────┤
│ id (PK)             │
│ user_id (FK)        │
│ category_id (FK)    │
│ amount              │
│ note                │
│ spend_at            │
│ created_at          │
└─────────────────────┘
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

> ⚠️ **Security Warning:** Always use strong, unique values for `JWT_SECRET` in production!

---

## 📈 Future Improvements

- [ ] 📝 Structured logging & Request Tracing
- [ ] 🚀 Cloud deployment
- [ ] 📈 Monitoring & metrics
- [ ] 🔒 Rate limiting
- [ ] 🏊 Connection pooling

---

## 👨‍💻 Author

## ** Saad Saboor **

Built as a portfolio-grade backend project focused on:

- 🔐 Real-world authentication patterns
- 🗄️ PostgreSQL and raw SQL
- 🏗️ Clean architecture principles
- 🚀 Production-ready best practices

---

<div align="center">

### ⭐ Star this repo if you find it helpful!

Made with ❤️ and FastAPI

</div>
