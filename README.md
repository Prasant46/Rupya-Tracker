# 💰 RupyaTrack - Expense Tracker

A modern full-stack expense tracking application built with Flask and React.

[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=flat&logo=react&logoColor=white)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.3.3-38B2AC?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

---

## ✨ Features

- 🔐 **Authentication** - Email/password & OAuth (Google, GitHub) with JWT
- 💸 **CRUD Operations** - Create, read, update, delete expenses
- 📊 **Smart Filtering** - Search, date ranges, today's summary
- 🗑️ **Trash System** - Soft delete with restore capability
- 📥 **PDF Export** - Download expenses as PDF with date filtering
- 🌑 **Dark Mode** - Toggle between light and dark themes
- 📱 **Responsive** - Mobile-first design, works on all devices

---

## 🛠 Tech Stack

**Frontend:** React 18.2 • Vite • Tailwind CSS • React Query • Zustand • Axios • React Hook Form

**Backend:** Flask 2.3 • PostgreSQL • SQLAlchemy • JWT • Marshmallow • Bcrypt • Alembic

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 15+

### 1. Clone & Setup Backend

```bash
# Clone repository
git clone https://github.com/Prasant46/Rupya-Tracker.git
cd Rupya-Tracker/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Setup database
createdb expense_tracker
flask db upgrade

# Start backend
python run.py
```

Backend runs on **http://localhost:5000**

### 2. Setup Frontend

```bash
# Navigate to frontend
cd ../frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Set VITE_API_URL=http://localhost:5000

# Start development server
npm run dev
```

Frontend runs on **http://localhost:3000**

### 3. Access Application

Open **http://localhost:3000** in your browser

---

## 🔑 Environment Variables

### Backend `.env`
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=postgresql://user:pass@localhost:5432/expense_tracker
FRONTEND_URL=http://localhost:3000

# Optional OAuth
GITHUB_CLIENT_ID=your-github-id
GITHUB_CLIENT_SECRET=your-github-secret
GOOGLE_CLIENT_ID=your-google-id
GOOGLE_CLIENT_SECRET=your-google-secret
```

### Frontend `.env`
```env
VITE_API_URL=http://localhost:5000
```

---


## 👨‍💻 Author

**Prasant46** - [@Prasant46](https://github.com/Prasant46)

⭐ Star this repo if you found it helpful!