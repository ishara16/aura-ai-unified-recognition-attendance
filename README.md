<p align="center">
  <img src="assets/aura_logo.png" alt="AURA logo" width="120" />
</p>

<h1 align="center">AURA — AI Unified Recognition Attendance</h1>

<p align="center">
  Contactless classroom attendance using <b>face recognition</b> and <b>voice recognition</b>.<br/>
  Streamlit frontend · FastAPI backend · Supabase database
</p>

---

## Overview

Taking attendance by roll call wastes class time and is easy to fake. AURA lets a teacher mark a whole class present from **one group photo** or **one audio recording**. Students register once with their face (and optionally their voice), join subjects with a code or QR link, and can check their own attendance history.

## Features

**For teachers**
- Register and log in with username/password (bcrypt-hashed, JWT sessions)
- Create subjects (code, name, section) and share them through a **QR code / join link**
- **Face attendance**: upload or capture a class photo. Every face is detected, embedded and matched against enrolled students
- **Voice attendance**: record students speaking. The audio is split into utterances and each speaker is identified
- Review the recognized students before saving the attendance logs

**For students**
- Register with a face photo (and an optional voice sample)
- **Log in with your face**: no password needed
- Join subjects with a subject code or by scanning the teacher's QR code (auto-enroll through `?join-code=`)
- View your enrolled subjects and attendance records

## How recognition works

| Mode  | Pipeline |
|-------|----------|
| Face  | `dlib` frontal face detector → 68-point shape predictor → **128-d face embedding** → linear **SVM** (scikit-learn) trained on enrolled students' embeddings |
| Voice | `librosa` loads the audio at 16 kHz and splits it on silence → **Resemblyzer** speaker embedding for each segment → cosine similarity against stored voice embeddings (threshold 0.65) |

Only embeddings are stored in the database. Raw photos and recordings are not.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | [Streamlit](https://streamlit.io/) |
| Backend API | [FastAPI](https://fastapi.tiangolo.com/), Uvicorn, Pydantic Settings |
| Database | [Supabase](https://supabase.com/) (PostgreSQL) |
| Auth | JWT (`python-jose`), `bcrypt` |
| Face recognition | `dlib`, `face_recognition_models`, scikit-learn (SVM), NumPy |
| Voice recognition | Resemblyzer, librosa |
| Utilities | Pandas, Pillow, Segno (QR codes) |

## Architecture

```
┌────────────────────┐      HTTP + JWT      ┌────────────────────┐      ┌────────────┐
│ Streamlit frontend │  ─────────────────▶  │   FastAPI backend  │ ───▶ │  Supabase  │
│  app.py, src/      │                      │   backend/         │      │ (Postgres) │
│  face/voice ML     │  ◀─────────────────  │   /api/*           │ ◀─── │            │
└────────────────────┘        JSON          └────────────────────┘      └────────────┘
```

The ML pipelines run in the Streamlit app. The backend handles auth, business rules and all database access.

```
AURA/
├── app.py                  # Streamlit entry point (routes to home/teacher/student screens)
├── backend/
│   ├── main.py             # FastAPI app
│   ├── config.py           # Settings loaded from .env
│   ├── api/                # Route handlers
│   ├── services/           # Business logic + Supabase queries
│   ├── schemas/            # Pydantic request/response models
│   ├── core/               # JWT security & auth dependencies
│   └── database/           # Supabase client
├── src/
│   ├── screens/            # Home, teacher and student screens
│   ├── components/         # Dialogs (enroll, attendance, share subject, ...)
│   ├── pipelines/          # face_pipeline.py, voice_pipeline.py
│   └── api/                # HTTP client for the backend
├── assets/
└── requirements.txt
```

## Getting Started

### Prerequisites
- Python **3.11+**
- A [Supabase](https://supabase.com/) project with the tables listed [below](#database-schema-supabase)
- On Windows, `dlib-bin` installs prebuilt wheels. On Linux/macOS you may need CMake and a C++ compiler.

### 1. Clone and install

```bash
git clone https://github.com/ishara16/aura-ai-unified-recognition-attendance.git
cd aura-ai-unified-recognition-attendance

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure environment

Create a **`.env`** file in the project root for the backend:

```env
SUPABASE_URL=https://<your-project>.supabase.co
SUPABASE_KEY=<your-supabase-key>
JWT_SECRET_KEY=<a-long-random-string>
# Optional
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Create **`.streamlit/secrets.toml`** for the frontend:

```toml
SUPABASE_URL = "https://<your-project>.supabase.co"
SUPABASE_KEY = "<your-supabase-key>"
API_BASE_URL = "http://127.0.0.1:8000"
```

Both files are git-ignored. Never commit them.

### 3. Run

Start the backend:

```bash
uvicorn backend.main:app --reload
```

Then, in a second terminal, start the frontend:

```bash
streamlit run app.py
```

- App: http://localhost:8501
- API docs (Swagger UI): http://127.0.0.1:8000/docs

## API Reference

All routes are prefixed with `/api`. Protected routes need an `Authorization: Bearer <token>` header.

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/` | — | API status message |
| GET | `/health` | — | Health check |
| **Teacher auth** | | | |
| POST | `/api/auth/teacher/register` | — | Register a teacher (`username`, `name`, `password`) |
| POST | `/api/auth/teacher/login` | — | Log in, returns a JWT access token |
| GET | `/api/auth/me` | Teacher | Current teacher's profile |
| **Student auth** | | | |
| POST | `/api/auth/student/login` | — | Log in with `student_id` |
| POST | `/api/auth/student/face-login` | — | Log in with a `face_embedding` |
| **Students** | | | |
| POST | `/api/students` | — | Register a student (`name`, `face_embedding`, optional `voice_embedding`) |
| GET | `/api/students` | Teacher | List all students |
| GET | `/api/students/{student_id}` | Teacher | Get one student |
| **Subjects** | | | |
| POST | `/api/subjects` | Teacher | Create a subject (`subject_code`, `name`, `section`) |
| GET | `/api/subjects` | Teacher | List the teacher's subjects |
| GET | `/api/subjects/{subject_id}/students` | Teacher | Students enrolled in a subject |
| GET | `/api/subjects/{subject_id}/voice-students` | Teacher | Enrolled students with voice embeddings |
| **Enrollments** | | | |
| POST | `/api/enrollments` | Student | Join a subject by `subject_code` |
| GET | `/api/enrollments/me` | Student | List my subjects |
| DELETE | `/api/enrollments/{subject_id}` | Student | Leave a subject |
| **Attendance** | | | |
| POST | `/api/attendance` | Teacher | Record attendance (`subject_id`, `student_id`, `is_present`, `timestamp`) |
| GET | `/api/attendance` | Teacher | Attendance logs for the teacher's subjects |
| GET | `/api/attendance/me` | Student | My attendance history |

## Database Schema (Supabase)

This schema was inferred from the application's queries. Adjust the column types to match your project.

```sql
create table teachers (
  teacher_id  bigint generated always as identity primary key,
  username    text unique not null,
  name        text not null,
  password    text not null          -- bcrypt hash
);

create table students (
  student_id      bigint generated always as identity primary key,
  name            text not null,
  face_embedding  jsonb,              -- 128 floats (dlib)
  voice_embedding jsonb               -- 256 floats (Resemblyzer)
);

create table subjects (
  subject_id    bigint generated always as identity primary key,
  subject_code  text unique not null,
  name          text not null,
  section       text,
  teacher_id    bigint references teachers(teacher_id) on delete cascade
);

create table subject_students (
  subject_id  bigint references subjects(subject_id) on delete cascade,
  student_id  bigint references students(student_id) on delete cascade,
  primary key (subject_id, student_id)
);

create table attendance_logs (
  id          bigint generated always as identity primary key,
  subject_id  bigint references subjects(subject_id) on delete cascade,
  student_id  bigint references students(student_id) on delete cascade,
  is_present  boolean default true,
  timestamp   timestamptz not null
);
```

## Author

**Isha Raut** · [GitHub @ishara16](https://github.com/ishara16)
