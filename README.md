---
title: Lumina Analyst
emoji: 💎
colorFrom: indigo
colorTo: purple
sdk: docker
pinned: false
app_port: 7860
base_path: /
---

# 💎 Lumina Analyst

**Lumina Analyst** is a high-performance, autonomous AI data agent designed for deep analytical reasoning. Upload complex datasets, ask high-level questions, and receive real-time streaming insights with advanced visualizations — powered by LLMs and a high-resiliency analytical core.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6?logo=typescript)

---

## ✨ Features

- **⚡ Real-Time Streaming Analysis** — Watch the agent's reasoning-step-by-step
- **🛡️ High-Resiliency Context** — Smart schema compression for strict LLM rate limits
- **🔍 Natural Language Intelligence** — Ask complex questions in plain English
- **📊 Interactive Visualizations** — Dynamic Plotly charts (Histogram, Box, Pie, etc.)
- **📈 Intelligence Synthesis** — Automated executive summaries and numeric insights
- **🐍 Safe Code Execution** — Secure environment for advanced pandas operations
- **🎨 Obsidian Design System** — A stunning, modern dark UI for premium analytical experiences

---

## 🏗️ Architecture

```
Frontend (React + Vite)
        ↓ HTTP
FastAPI Backend
        ↓
Agent Orchestrator
        ↓
LLM (Groq / OpenAI) ← Function Calling
        ↓
Tool Router
     ↙    ↓    ↘
 File   Python   Chart
Loader  Executor Generator
     ↘    ↓    ↙
Results Collected
        ↓
LLM Explanation
        ↓
Structured JSON Response
        ↓
Frontend Display
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | FastAPI, Python 3.11+, Pydantic v2, Uvicorn |
| **AI/LLM** | Groq API, OpenAI API (function calling) |
| **Analysis** | pandas, numpy, matplotlib, seaborn |
| **Frontend** | React 19, Vite, TypeScript |
| **Testing** | pytest, httpx |

---

## 📁 Project Structure

```
data-analyst-agent/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/    # Route handlers
│   │   ├── core/                # Config, logging, exceptions
│   │   ├── schemas/             # Pydantic models
│   │   ├── services/            # Business logic & agent
│   │   ├── tools/               # File loader, Python executor, chart gen
│   │   ├── utils/               # Helpers
│   │   └── main.py              # FastAPI app entry point
│   ├── tests/                   # pytest test suite
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/          # React UI components
│   │   ├── services/            # API client
│   │   ├── types/               # TypeScript interfaces
│   │   ├── App.tsx              # Main app
│   │   └── index.css            # Design system
│   └── package.json
└── README.md
```

---

## 🚀 Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- A Groq or OpenAI API key

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env and add your GROQ_API_KEY or OPENAI_API_KEY

# Start the server
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## 🔑 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | `groq` or `openai` | `groq` |
| `GROQ_API_KEY` | Groq API key | — |
| `OPENAI_API_KEY` | OpenAI API key | — |
| `GROQ_MODEL` | Groq model name | `llama-3.3-70b-versatile` |
| `OPENAI_MODEL` | OpenAI model name | `gpt-4o-mini` |
| `UPLOAD_DIR` | Upload storage path | `./uploads` |
| `CHART_DIR` | Chart storage path | `./charts` |
| `FRONTEND_URL` | CORS origin | `http://localhost:5173` |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/upload` | Upload dataset (CSV/Excel) |
| `GET` | `/api/v1/files/{id}/preview` | Preview dataset rows & schema |
| `POST` | `/api/v1/analyze` | Run AI analysis on dataset |
| `GET` | `/api/v1/files/{id}/charts/{name}` | Serve chart image |

### Example API Flow

```bash
# 1. Upload a CSV
curl -X POST http://localhost:8000/api/v1/upload \
  -F "file=@sales_data.csv"

# Response: { "file_id": "a1b2c3d4e5f6g7h8", ... }

# 2. Ask a question
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"file_id": "a1b2c3d4e5f6g7h8", "query": "Show revenue trends by month"}'
```

### Example Response

```json
{
  "summary": "Revenue shows a consistent upward trend over the past 6 months...",
  "insights": [
    "Revenue grew by 18% month-over-month on average",
    "June had the highest total revenue at $142,000",
    "The Electronics category was the top performer"
  ],
  "statistics": {
    "row_count": 1200,
    "column_count": 8,
    "numeric_columns": ["revenue", "profit", "units_sold"]
  },
  "charts": [
    {
      "title": "Monthly Revenue Trend",
      "url": "/api/v1/files/a1b2c3d4/charts/monthly_revenue_trend",
      "chart_type": "line"
    }
  ],
  "tool_calls": ["group_and_aggregate", "create_chart", "compute_statistics"]
}
```

---

## 💬 Example Queries

- *"Analyze this CSV and summarize the key trends"*
- *"Show revenue by month"*
- *"Find correlations between profit and marketing spend"*
- *"Create a histogram for customer age"*
- *"Which product category performs best?"*
- *"Show summary statistics"*
- *"Analyze null values in the dataset"*
- *"Create a scatter plot of price vs quantity"*

---

## 🧪 Running Tests

```bash
cd backend
python -m pytest tests/ -v
```

---

## 🔮 Future Improvements

- [ ] Session history & conversation memory
- [ ] Multiple file support (joins, comparisons)
- [ ] Downloadable reports (PDF export)
- [ ] WebSocket streaming for real-time analysis progress
- [ ] Docker containerization
- [ ] Database-backed file registry (PostgreSQL)
- [ ] Authentication & user management
- [ ] More chart types (pie, treemap, box plot)
- [ ] Natural language data filtering
- [ ] Automated data cleaning suggestions

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
