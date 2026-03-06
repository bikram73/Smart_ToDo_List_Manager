# 📝 Smart To-Do List Manager (Advanced Dashboard)

A full-stack web application built with **FastAPI** and **Python**, featuring an advanced dashboard with a calendar view, email reminders, and user profile management. Designed for serverless deployment on **Vercel**.


---

## 🚀 Features
### Core Features
*   **🔐 User Authentication**: Secure Signup & Login using JWT (JSON Web Tokens) and Bcrypt password hashing.
*   **✅ Full CRUD for Tasks**: Create, Read, Update, and Delete tasks.
*   **📊 Dashboard**: Real-time statistics showing total, completed, and pending tasks.

### Advanced Dashboard Features
*   **📅 Calendar Task View**: A monthly calendar that visualizes tasks.
    *   🟢 Green dot for days with tasks.
    *   🔵 Blue highlight for the current day.
    *   🔴 Red dot for past days with incomplete tasks.
*   **⏰ Optional Time Scheduling**: Assign specific start and end times to tasks.
*   **📧 Automatic Email Reminders**: If a scheduled task is not completed by its end time, the system automatically sends a reminder email (requires a Cron Job).
*   **🗓️ Reschedule Past Tasks**: Easily move incomplete tasks from past days to today with a single click.
*   **👤 User Profile Management**: Users can view and update their username, email, and password.


---

## 🛠️ Tech Stack

*   **Backend**: Python 3.9+, FastAPI, SQLAlchemy, Pydantic
*   **Frontend**: HTML5, JavaScript (Fetch API), Bootstrap 5
*   **Database**: SQLite (Local), PostgreSQL (Production/Vercel)
*   **Emailing**: `smtplib` for sending email notifications via Gmail/SMTP.
*   **Security**: OAuth2, JWT, Passlib (Bcrypt)

---

## 📂 Project Structure

```text
todo-python-vercel/
│
├── api/                 # Backend entry point
│   └── index.py
│
├── database/            # Database connections
│   ├── auth_db.py
│   └── todo_db.py
│
├── models/              # SQLAlchemy & Pydantic models
│   ├── user_model.py
│   └── todo_model.py
│
├── services/
│   └── email_service.py     # Logic for sending emails
│
├── routes/              # API Endpoints
│   ├── auth_routes.py
│   └── todo_routes.py
│   └── user_routes.py       # /user/profile
│
├── utils/               # Helper functions
│   └── security.py      # Hashing & JWT logic
│
├── frontend/            # Static UI files
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   └── dashboard.html
│   ├── profile.html
│   └── calendar.js
│
├── fix_db.py
├── requirements.txt     # Python dependencies
└── vercel.json          # Vercel configuration
```

---

## ⚡ Installation & Local Setup

Follow these steps to run the project locally.

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/smart-todo-list.git
cd smart-todo-list
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python -m uvicorn api.index:app --reload
```

### 5. Access the App
Open your browser and go to:
👉 **http://127.0.0.1:8000**

---

## 🔑 Environment Variables

By default, the app uses **SQLite** for local development. To use **PostgreSQL**, set the following environment variables:

| Variable | Description |
| :--- | :--- |
| `AUTH_DATABASE_URL` | Connection string for User DB (e.g., `postgresql://user:pass@host/auth_db`) |
| `TODO_DATABASE_URL` | Connection string for Todo DB (e.g., `postgresql://user:pass@host/todo_db`) |
| `JWT_SECRET` | Secret key for signing tokens (default: `supersecretkey`) |

---

## 📡 API Endpoints

### Authentication
*   `POST /api/signup` - Register a new user
*   `POST /api/login` - Login and receive JWT token

### Todos
*   `GET /api/todos` - Get all tasks for logged-in user
*   `POST /api/todos` - Create a new task
*   `PUT /api/todos/{id}` - Update task details
*   `PATCH /api/todos/{id}/complete` - Mark task as completed
*   `DELETE /api/todos/{id}` - Delete a task

---

## ☁️ Deployment (Vercel)

1.  **Push to GitHub**: Upload your code to a GitHub repository.
2.  **Import to Vercel**: Go to Vercel and import the repo.
3.  **Configure Environment**:
    *   Add `AUTH_DATABASE_URL` and `TODO_DATABASE_URL` (use Neon or Supabase for free PostgreSQL).
    *   Add `JWT_SECRET`.
4.  **Deploy**: Click deploy! Vercel will handle the serverless backend.

---

Made with ❤️ by Bikram