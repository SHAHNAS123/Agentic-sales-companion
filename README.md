# ABFRL SYNAPSE – Smart Retail Experience

AI-powered multi-agent retail demo for Aditya Birla Fashion and Retail Limited.
Three agents work together: **Sales Agent → Recommendation Agent → Payment Agent**.

---

## Project Structure

```
abfrl/
├── index.html        ← Frontend (open directly OR serve via backend)
├── style.css         ← Stylesheet
├── script.js         ← Frontend logic (Claude-in-Claude + backend fallback)
├── server_api.py     ← FastAPI backend  ← START HERE
├── agent.py          ← LLM agent logic (Ollama or rule-based fallback)
├── data.py           ← Customer profiles + product catalog
├── fetch_abfrl.py    ← Optional product scraper
├── requirements.txt  ← Python dependencies
├── .env              ← (optional) environment variables
└── data/
    └── products.json ← (auto-created by /admin/bootstrap)
```

---

## Quick Start (2 options)

### Option A — Frontend Only (No Python needed)
Just open `index.html` in your browser. The chat uses the **Anthropic API directly**
(Claude-in-Claude), so everything works without any backend.

> The status badge will show **"AI: ready"** — this is correct and expected.

---

### Option B — Full Stack (Frontend + Python backend)

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. (Optional) Configure Ollama**
```bash
# Install Ollama from https://ollama.ai, then:
ollama pull llama3
```
If Ollama is not running, the backend uses smart built-in responses automatically.

**3. Start the backend**
```bash
python server_api.py
# OR
uvicorn server_api:app --reload --port 8000
```

**4. Open the frontend**
- Visit `http://localhost:8000` (backend serves static files too), OR
- Open `index.html` directly in your browser (also works)

The status badge will show **"Backend: online"** when the Python server is reachable.

---

## Environment Variables (optional)

Create a `.env` file:
```
PORT=8000
OLLAMA_MODEL=llama3
ADMIN_TOKEN=your-secret-token
```

---

## How It Works

```
User types a message
       │
       ▼
script.js detects intent (recommend / loyalty / payment / chat)
       │
       ├─► If Python backend online → POST /api/chat → agent.py → Ollama or fallback
       │
       └─► If backend offline → Anthropic API directly (Claude Sonnet)
                                  (works without any backend)
```

### Agent Flow
1. **Sales Agent** — orchestrates the conversation, captures intent
2. **Recommendation Agent** — suggests outfit + product with price
3. **Payment Agent** — generates order summary, handles confirmation

---

## API Endpoints (when backend is running)

| Method | Path              | Description                        |
|--------|-------------------|------------------------------------|
| GET    | /api/health       | Health check (returns `{"status":"ok"}`) |
| POST   | /api/chat         | Free-text chat → Sales Agent       |
| POST   | /api/recommend    | Get outfit recommendation          |
| POST   | /api/payment      | Get order/payment summary          |
| POST   | /api/run_flow     | Run full Sales→Rec→Payment demo    |
| GET    | /api/llm_test     | Test Ollama connectivity           |
| POST   | /api/debug        | Debug endpoint with traceback      |
| POST   | /admin/bootstrap  | Scrape products (requires token)   |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Chat shows "Backend: offline" | Normal if Python server isn't running — AI still works via Anthropic API |
| `ModuleNotFoundError: agent` | Make sure you're running `python server_api.py` from the `abfrl/` folder |
| Ollama errors | Ollama is optional — the system falls back automatically |
| CORS errors | The backend allows all origins (`*`). If you still see CORS errors, open `index.html` from `http://localhost:8000` instead of the filesystem |
| Port 8000 already in use | `PORT=8001 python server_api.py` |
