# MindVault AI 

A note-taking REST API built with **FastAPI**, featuring secure authentication, CRUD operations for notes, and AI-powered summaries using **Google Gemini API**.  

---

## 🚀 Features
- **CRUD operations** for posts/notes (Create, Read, Update, Delete)
- **JWT authentication** with access & refresh tokens
- Tokens stored in **cookies** for secure session handling
- **AI-powered summaries** of notes via Gemini API
- **Email + password reset** (work in progress)
- Built with a clean, modular structure using FastAPI

---

## 🛠️ Tech Stack
- **Framework**: FastAPI
- **Auth**: JWT (access + refresh tokens), cookies
- **Database**: Neon (PostgreSQL)
- **AI Integration**: Google Gemini API
- **Other**: Pydantic, Python, Sqlalchemy, Bcrypt

---

## 📂 API Endpoints

### Authentication
- `POST /auth/register` → Register a new user  
- `POST /auth/login` → Login and receive tokens  
- `POST /refresh` → Refresh access token  
- `POST /reset-password` → (Work in progress) Reset user password via email  

### Notes
- `GET /notes/` → Get all notes for logged-in user  
- `GET /notes/{id}` → Get a single note  
- `POST /notes/` → Create a new note  
- `PUT /notes/{id}` → Update a note  
- `DELETE /notes/{id}` → Delete a note  

### AI
- `POST /notes/{id}/summarize` → Generate AI summary for a note using Gemini API  

---

## 🔑 Authentication Flow
- **JWT Access Token** (short-lived) stored in cookies  
- **JWT Refresh Token** (long-lived) used to renew access tokens  
- Middleware protects routes and verifies tokens  

---

## 🚀 How to Run
1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/mindvault-ai.git
   cd mindvault-ai
   ```
2. Create & activate a virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate   # Linux/Mac
  venv\Scripts\activate      # Windows
  ```
3. Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
4. Add environment variables (.env file):
  ```bash
  # Database (Postgres via Neon)
   DATABASE_URL=postgresql://neondb_owner:<password>@<host>/<dbname>?sslmode=require&channel_binding=require

   # JWT / Tokens
   ACCESS_TOKEN_SECRET_KEY=YOURKEY
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   REFRESH_TOKEN_SECRET_KEY=YOURKEY
   REFRESH_TOKEN_EXPIRE_DAYS=10
   RESET_TOKEN_SECRET_KEY=YOURKEY
   JWT_ALGORITHM=HS256
   # Gemini AI

   GEMINI_API_KEY=your_gemini_api_key
  ```
5. Run the server:
  ```bash
  uvicorn main:app --reload
  ```
