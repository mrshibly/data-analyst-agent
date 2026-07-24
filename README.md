---
title: Lumina Analyst
emoji: 💎
colorFrom: indigo
colorTo: purple
sdk: docker
pinned: false
app_port: 8000
base_path: /
---

# 💎 Lumina Analyst

**Lumina Analyst** is a high-performance, autonomous AI data analyst agent designed for deep analytical reasoning, predictive modeling, data cleaning, and executive reporting. Upload complex datasets (CSV/Excel), ask natural language questions, and receive real-time streaming insights with interactive visualizations.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.7-3178C6?logo=typescript)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.9-F7931E?logo=scikitlearn)
![Plotly](https://img.shields.io/badge/Plotly-6.0-3F4F75?logo=plotly)

---

## ✨ Features

- **💬 Chat-First Analytical UI** — Multi-turn conversation timeline with real-time reasoning steps & suggestion pills.
- **📊 Interactive Chart Studio** — Dynamic Plotly graphics with instant type switching (Bar, Line, Scatter, Pie, Box), high-res PNG export, and fullscreen mode.
- **📄 One-Click Executive PDF Exporter** — Instant executive report generation with KPI summary cards, structured insights, and browser print-to-PDF.
- **🤖 Predictive Machine Learning Engine** — Train Scikit-Learn linear regression models ($R^2$ fit scores, feature weights) and execute Isolation Forest anomaly/outlier detection.
- **🧹 AI Data Cleaning & Transformation** — Perform missing value imputation (mean, median, mode, forward-fill) and formula-calculated column engineering (`goals_per_match = goals / matches`).
- **🛡️ Multi-Model Rate Limit Resilience** — Multi-tiered automatic fallback system (`llama-3.1-8b-instant` ➔ `mixtral-8x7b-32768` ➔ `llama-3.3-70b-versatile`) to bypass strict free tier token quotas without downtime.
- **📂 Slide-Over Data Drawer** — Slide-over drawer for dataset preview, column schema inspection, and data type summaries.
- **🐍 Safe Python Code Sandbox** — AST-sandboxed code execution environment for custom pandas & numpy computations.

---

## 🏗️ Architecture

```
User (Browser Chat UI)
        ↓ HTTP / SSE
FastAPI Backend (Port 8000)
        ↓
Agent Orchestrator
        ↓
LLM Engine (Groq / OpenAI) ← Automatic Rate-Limit Failover
        ↓
Tool Router & Function Calling
   ┌────┼──────────────┬──────────────┬────────────────┐
  File  Python       Plotly       Data Cleaning     Predictive ML
Loader  Executor    Generator      & Imputation      (Regression &
                                                    Isolation Forest)
   └────┴──────────────┴──────────────┴────────────────┘
        ↓
Results & Interactive Payload Synthesis
        ↓
Frontend Render (Plotly + Markdown + KPI Cards + PDF Export)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | FastAPI, Python 3.12+, Pydantic v2, Uvicorn |
| **AI / LLM** | Groq API, OpenAI API, Multi-Model Failover Router |
| **Machine Learning** | Scikit-Learn (LinearRegression, IsolationForest), pandas, numpy |
| **Visualizations** | Plotly, Matplotlib, Seaborn |
| **Frontend** | React 19, TypeScript, TailwindCSS, Lucide Icons |
| **Testing** | Pytest, HTTPX |

---

## 📁 Project Structure

```
Lumina Analyst/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/    # REST & streaming route handlers
│   │   ├── core/                # Config, logging, SQLite database registry
│   │   ├── schemas/             # Pydantic data contracts
│   │   ├── services/            # Agent service, LLM service, chart service
│   │   ├── tools/               # File loader, executor, Plotly, cleaner, predictive ML
│   │   └── main.py              # FastAPI application server
│   ├── tests/                   # 17 Unit test suites (test_advanced_tools, test_analysis, etc.)
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/          # Interactive UI components (ChartViewer, DataDrawer, QueryInput)
│   │   ├── services/            # Axios API client
│   │   ├── types/               # TypeScript interfaces
│   │   ├── App.tsx              # Chat workspace & Executive Report exporter
│   │   └── index.css            # Dark mode styles & custom scrollbars
│   ├── dist/                    # Compiled production build
│   └── package.json
└── README.md
```

---

## 🚀 Quickstart

### Prerequisites

- Python 3.11+
- Node.js 18+
- A Groq API key (or OpenAI API key)

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment in .env
GROQ_API_KEY=gsk_...
GROQ_MODEL=llama-3.1-8b-instant

# Start FastAPI server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Build static bundle for FastAPI static mounting
npm run build
```

Open **http://127.0.0.1:8000** in your browser!

---

## 🔑 Environment Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | `groq` or `openai` | `groq` |
| `GROQ_API_KEY` | Groq API key | — |
| `GROQ_MODEL` | Primary Groq model | `llama-3.1-8b-instant` |
| `OPENAI_API_KEY` | OpenAI API key | — |
| `OPENAI_MODEL` | OpenAI model | `gpt-4o-mini` |
| `UPLOAD_DIR` | Upload dataset path | `./uploads` |
| `CHART_DIR` | Matplotlib chart path | `./charts` |

---

## 💬 Example Analytical Queries

- **Basic Analysis**: *"Who are the top 5 goalscorers across all leagues? Create a bar chart."*
- **Predictive ML**: *"Train a regression model predicting market value from rating and goals."*
- **Anomaly Detection**: *"Detect outliers in ratings and market value using Isolation Forest."*
- **Data Cleaning**: *"Fill missing values in the goals column with mean imputation."*
- **Feature Engineering**: *"Create a calculated column goals_per_match = goals / matches_played."*

---

## 🧪 Running Unit Tests

Run the backend test suite:

```bash
cd backend
.\venv\Scripts\python.exe -m pytest tests/ -v
```

All 17 pytest suites test upload handlers, sandbox security, data cleaning, regression modeling, and anomaly detection.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
