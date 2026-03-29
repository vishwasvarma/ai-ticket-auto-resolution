# AI Ticket Auto Resolution System

---

# Problem Statement

In large organizations, IT support teams receive hundreds of tickets daily. Most of these tickets are repetitive and require manual triaging, classification, and resolution.

This leads to several operational challenges:

- Slow response times  
- Increased operational cost  
- Human dependency for repetitive issues  
- Lack of automation in ticket handling  
- Delayed resolution for users  

The objective of this project is to build an **AI-powered Retrieval-Augmented Generation (RAG) based ticket resolution system** that can intelligently process incoming support tickets and automatically generate solutions.

The system is designed to:

- Automatically classify incoming tickets  
- Retrieve similar past solutions using embeddings  
- Generate structured responses using RAG pipeline  
- Allow admin intervention when needed  
- Store and manage tickets efficiently  

---

# Solution Overview

We developed an **AI-Driven RAG-Based Ticket Auto Resolution System** that automates the entire ticket lifecycle.

### Workflow

1. Users raise support tickets  
2. AI model analyzes ticket description  
3. Ticket is categorized automatically  
4. Similar tickets retrieved using embeddings  
5. Response generated using retrieved solutions  
6. Admin reviews when required  
7. All tickets stored in PostgreSQL  

This significantly reduces manual effort and improves response time.

---

# Contributors
```
- Manoj Royal - https://github.com/manojcodes93  
- Vishwas - https://github.com/vishwasvarma
```
---

# Project Highlights

- RAG-Based AI Architecture  
- 82%+ Classification Accuracy  
- Hybrid ML + Semantic Retrieval System  
- AI-Based Ticket Classification  
- Semantic Search Using Embeddings  
- Automatic Response Generation  
- Confidence-Based Manual Review  
- Spell Correction for Noisy Input  
- Admin Dashboard (Full UI Implemented)  
- User Dashboard (Full UI Implemented)  
- Ticket Status Management  
- Unique Ticket ID Generation  
- User Ticket History  
- Role-Based Access (Admin/User)  
- React Frontend Integration  
- JWT Authentication  
- Logout & Session Handling  
- Ticket Filtering (All / Closed / Unresolved)  
- AI Response Display  
- Professional Dashboard UI  

---

# Key Features

- AI-Based Ticket Classification  
- Semantic Search Using Embeddings  
- Retrieval-Augmented Generation (RAG)  
- Automatic Response Generation  
- Confidence-Based Manual Review  
- Spell Correction for Noisy Input  
- Admin Dashboard UI  
- User Dashboard UI  
- Ticket Status Management  
- Unique Ticket ID Generation  
- User Ticket History  
- Role-Based Access (Admin/User)  
- AI Confidence‑based Decision  
- Ticket Filtering  
- Ticket Response View  
- Logout Functionality  

---

# Tech Stack

## Frontend
- React.js 
- Modern Dashboard UI  

## Backend
- FastAPI  
- Python  

## Database
- PostgreSQL  
- SQLAlchemy ORM  

## AI / ML

- Scikit-Learn  
- Stochastic Gradient Descent (SGD) Classifier  
- TF-IDF Vectorizer  
- Sentence Transformers  
- MiniLM Embeddings  
- Cosine Similarity Retrieval  
- Retrieval Augmented Generation (RAG)

## NLP Utilities

- PySpellChecker  
- Numpy  
- Pandas  

## Deployment Tools

- Uvicorn  
- Python Virtual Environment  

---

# Models Used

## 1. Ticket Classification Model

### Algorithm Used

- TF-IDF Vectorizer  
- Stochastic Gradient Descent (SGD) Classifier  

### Model Details

- Training Dataset Size: ~4000+ tickets  
- Accuracy: ~82%+  
- Features: 20+ engineered features  

### Files

- model.pkl  
- vectorizer.pkl  

### Purpose

Classify tickets into categories:

- Software Error  
- Printer Malfunction  
- Account Access  
- Software Installation  
- Software Configuration  
- Other Issue  

---

## 2. Semantic Retrieval Model

### Embedding Model

sentence-transformers/all-MiniLM-L6-v2

### Used For

- Similar ticket retrieval  
- Context matching  
- Solution recommendation  

### Files

- embeddings.pkl  
- tickets.pkl  
- solutions.pkl  

---

# RAG-Based Architecture

This project follows a **Retrieval-Augmented Generation (RAG)** architecture.

## RAG Workflow

User Ticket  
↓  
Classification Model (SGD)  
↓  
Embedding Generation (MiniLM)  
↓  
Semantic Retrieval (Top Similar Tickets)  
↓  
Confidence Score Check  
↓  
Auto Resolution / Manual Review  

---

# RAG Components

## Retriever

- Sentence Transformers  
- MiniLM Embeddings  
- Cosine Similarity Search  

## Generator

- Retrieved historical solutions  
- Structured formatted responses  

---

# Why RAG Was Used

- Improves accuracy  
- Uses real historical solutions  
- Reduces hallucination  
- Improves enterprise reliability  

---

# Dataset Used

Dataset Source:  
https://huggingface.co/datasets/KameronB/synthetic-it-callcenter-tickets

Dataset includes:

- Ticket Description  
- Category  
- Resolution  

### Example Dataset

| Ticket | Category | Solution |
|--------|----------|----------|
| Printer not working | Printer Malfunction | Reset printer |
| Login issue | Account Access | Reset password |
| Application crash | Software Error | Restart service |

Dataset Size:

~4000+ tickets

---

# Project Architecture

User  
↓  
React Frontend  
↓  
FastAPI Backend  
↓  
AI Engine  
↓  
Classification Model  
↓  
RAG Retrieval System  
↓  
PostgreSQL Database  

---

# Folder Structure

```
ai-ticket-auto-resolution/
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── UserDashboard.jsx
│   │   │   └── AdminDashboard.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   └── main.jsx
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   │
│   └── routes/
│       ├── auth_routes.py
│       └── ticket_routes.py
│
├── model/
│   ├── ai_engine.py
│   ├── retrieval.py
│   ├── build_embeddings.py
│   ├── model.pkl
│   ├── vectorizer.pkl
│   ├── embeddings.pkl
│   ├── train_model.py
│   ├── test_model.py
│   ├── tuning.py
│   └── test_ai_engine.py
│
├── test_cases.pdf
│
├── requirements.txt
└── README.md
```

---

# Database Schema

## Users Table

| Column | Type |
|--------|------|
| id | Integer |
| username | String |
| password | String |
| role | String |
| created_at | Timestamp |

---

## Tickets Table

| Column | Type |
|--------|------|
| id | Integer |
| ticket_number | String |
| title | String |
| description | Text |
| category | String |
| response | Text |
| status | String |
| user_id | Integer |
| created_at | Timestamp |

---

# Ticket Status Flow

Open  
↓  
AI Response Generated  
↓  
Resolved / Needs Attention  
↓  
Admin Review (Optional)  
↓  
Closed  

---

# Requirements

```
fastapi
uvicorn
sqlalchemy
psycopg2-binary
pydantic
sentence-transformers
scikit-learn
numpy
pandas
pyspellchecker
requests
openai
```

---

# How to Run the Project

## Step 1 — Clone Repository

```
git clone https://github.com/manojcodes93/ai-ticket-auto-resolution
cd ai-ticket-auto-resolution
```

---

## Step 2 — Create Virtual Environment

```
python -m venv myvenv
```

Activate

```
myvenv\Scripts\activate
```

---

## Step 3 — Install Dependencies

```
pip install -r requirements.txt
```

---

## Step 4 — Create PostgreSQL Database

Create Database

```
ai_ticket_handling
```

---

## Step 5 — Generate Embeddings

```
python model/build_embeddings.py
```

---

## Step 6 — Run Backend

```
uvicorn backend.main:app --reload
```

---

## Step 7 — Run Frontend

```
cd frontend
npm install
npm run dev
```

---

# API Endpoints

## Authentication

POST  
/login  

## Create Ticket

POST  
/tickets/create  

## Get User Tickets

GET  
/tickets/my  

## Admin Get Tickets

GET  
/tickets  

## Update Ticket

PATCH  
/tickets/{ticket_number}

---

# Unique Ticket Number

Example

```
TCKA83F29X
```

Generated using:

- Random Alphabets  
- Random Numbers  
- PostgreSQL Unique Constraint  

---

# AI Decision Flow

User Ticket  
↓  
Spell Correction  
↓  
Classification Model  
↓  
Embedding Similarity  
↓  
Confidence Check  
↓  
Auto Response / Manual Review  

---

# Confidence Threshold

| Score | Action |
|-------|--------|
| ≥ 55% | Resolved |
| 40–55% | Open |
| < 40% | Needs Attention |

---

# Performance

Average Response Time

- Classification: < 100ms  
- Retrieval: < 200ms  
- Total Response: < 500ms  

---

# Test Cases

Test cases included for:

- API Testing  
- AI Model Testing  
- Ticket Creation  
- Authentication Testing  
- Retrieval Testing  

Test cases located in:

```
https://github.com/manojcodes93/ai-ticket-auto-resolution/blob/main/test_cases.pdf
```

---

# Why This Project Stands Out

- RAG-Based AI Architecture  
- Real-world enterprise use case  
- AI + Full Stack Integration  
- Hybrid ML + Semantic Retrieval  
- Production-ready architecture  
- Scalable design  
- Admin + User UI  
- JWT Authentication  

---


# Final Outcome

This system reduces:

- Manual ticket triage  
- Resolution time  
- Support workload  

This system improves:

- Automation  
- Efficiency  
- Scalability  

---

# Future Improvements

## Admin Enhancements

- Admin manual response override  
- Admin editing AI responses  
- Ticket reassignment  
- Priority‑based handling  

---

## User Management

- Multiple user accounts  
- Role-based access  
- Account creation  
- Account deletion  

---

## UI Improvements

- Professional UI  
- Sidebar navigation  
- Analytics dashboard  
- Responsive layout  

---

## AI Improvements

- Model fine‑tuning  
- Feedback learning  
- Multi‑language support  

---

## Enterprise Features

- Multi‑tenant support  
- SLA tracking  
- Audit logs  

---

# Roadmap

## Phase 1

- Admin response system  
- Multiple users  
- Account management  

## Phase 2

- Advanced UI  
- Analytics  
- Notifications  

## Phase 3

- AI improvements  
- Enterprise features  
- Cloud deployment  

---

# GitHub

Project Repository  
https://github.com/manojcodes93/ai-ticket-auto-resolution

Dataset  
https://huggingface.co/datasets/KameronB/synthetic-it-callcenter-tickets

Contributors  
https://github.com/manojcodes93  
https://github.com/vishwasvarma

---
