# Expense Tracker Backend

A production-grade backend API for a personal expense tracking application, built with **FastAPI**, **raw SQL**, and **JWT-based authentication with refresh tokens**.

This project is designed with **clean architecture**, **security**, and **real-world backend practices** in mind.

---

## 🧩 Features

- User authentication (register, login)
- JWT Access Tokens
- Refresh Tokens with database-backed sessions
- Token rotation & logout
- Category management
- Expense tracking
- Monthly & category-wise reports
- Pagination
- Raw SQL (no ORM)
- Clean architecture (API → Service → Storage)

---

## 🛠️ Tech Stack

- **Python**
- **FastAPI**
- **SQLite** (v1)
- **PostgreSQL** (planned for v2)
- **Raw SQL**
- **Pydantic v2**
- **JWT (JSON Web Tokens)**

---

## 🔐 Authentication System

This backend uses **Access Tokens + Refresh Tokens** for real-world authentication.

| Token              | Purpose                       | Lifetime    |
| ------------------ | ----------------------------- | ----------- |
| Access Token (JWT) | Used to access protected APIs | Short-lived |
| Refresh Token      | Used to get new access tokens | Long-lived  |

Refresh tokens are stored in the database, allowing:

- logout
- session revocation
- multi-device login
- stolen token protection

---

## 🔄 Authentication Flow

<h2 style="color:#1f6feb;">1️⃣ Login</h2> 
`POST /auth/login`

Returns:

```json
{
  "access_token": "...",
  "refresh_token": "..."
}

<h2 style="color:#1f6feb;">2️⃣ Access Protected APIs</h2>

Use the access token:
Authorization: Bearer <access_token>

<h2 style="color:#1f6feb;">3️⃣ Access Token Expires</h2>

Protected APIs return:
401 Unauthorized

<h2 style="color:#1f6feb;">4️⃣ Refresh Tokenes</h2>
POST /auth/refresh
Client sends the refresh token and receives:

->a new access token
->(and a new refresh token if rotation is enabled)

<h2 style="color:#1f6feb;">5️⃣ Logout</h2>
POST /auth/logout

The refresh token is revoked in the database, ending the session.

🗄️ Database

The system uses the following core tables:
🔹users
🔹categories
🔹expenses
🔹refresh_tokens

The refresh_tokens table allows the backend to manage user sessions securely.

🚀 How to Run

git clone https://github.com/yourusername/expense-tracker-backend
cd expense-tracker-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

Open Swagger UI:
http://127.0.0.1:8000/docs

📈 Project Roadmap

 ☑️JWT Authentication
 ☑️Refresh Tokens & Sessions
 ☑️Logout & Token Revocation
 ⬜PostgreSQL migration
 ⬜Indexes & constraints
 ⬜Logging & observability
 ⬜Dockerization

👨‍💻 Author
Built as a portfolio-grade backend project focused on real-world authentication, clean architecture, and SQL-first design.
```
