"""
ABFRL SYNAPSE – server_api.py
FastAPI backend. Run with:  python server_api.py
or:  uvicorn server_api:app --reload --port 8000
"""

import asyncio
import os
import time
import traceback

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agent import get_recommendation, get_payment_summary, run_demo_flow

app = FastAPI(title="ABFRL SYNAPSE API", version="1.0.0")

# ---- CORS: allow every origin so the HTML frontend on any port works ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,   # must be False when allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---- Pydantic models -----------------------------------------------
class ChatRequest(BaseModel):
    message: str
    context: dict | None = None


class PaymentRequest(BaseModel):
    product_name: str
    price: str
    category: str | None = None


class AdminBootstrapRequest(BaseModel):
    seeds: list[str]
    limit: int = 100
    delay: float = 1.0
    out: str | None = None


# ---- Health --------------------------------------------------------
@app.get("/api/health")
async def api_health():
    return JSONResponse(status_code=200, content={"status": "ok"})


# ---- Chat ----------------------------------------------------------
@app.post("/api/chat")
async def api_chat(req: ChatRequest):
    try:
        reply = await asyncio.to_thread(
            lambda: get_recommendation(user_message=req.message, context=req.context)
        )
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---- Recommend -----------------------------------------------------
@app.post("/api/recommend")
async def api_recommend(context: dict | None = None):
    try:
        result = await asyncio.to_thread(lambda: get_recommendation(context=context or {}))
        return {"recommendation": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---- Payment -------------------------------------------------------
@app.post("/api/payment")
async def api_payment(req: PaymentRequest):
    try:
        result = await asyncio.to_thread(
            lambda: get_payment_summary(req.product_name, req.price, req.category or "")
        )
        return {"payment_summary": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---- Full demo flow ------------------------------------------------
@app.post("/api/run_flow")
async def api_run_flow(context: dict | None = None):
    try:
        result = await asyncio.to_thread(lambda: run_demo_flow(context or {}))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---- Debug ---------------------------------------------------------
@app.post("/api/debug")
async def api_debug_run(payload: dict | None = None):
    start = time.time()
    try:
        message = payload.get("message") if payload else None
        context = payload.get("context") if payload else None
        result = await asyncio.to_thread(
            lambda: get_recommendation(user_message=message, context=context)
        )
        return JSONResponse(
            status_code=200,
            content={"ok": True, "elapsed": round(time.time() - start, 3), "result": str(result)},
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"ok": False, "error": str(e), "traceback": traceback.format_exc()},
        )


# ---- LLM test ------------------------------------------------------
@app.get("/api/llm_test")
async def api_llm_test():
    try:
        from agent import ollama_llm, _OLLAMA_AVAILABLE

        if not _OLLAMA_AVAILABLE or ollama_llm is None:
            return JSONResponse(
                status_code=200,
                content={"ok": True, "mode": "fallback", "sample": "Ollama not configured — using built-in responses."},
            )

        result = await asyncio.to_thread(
            lambda: ollama_llm.generate(["Say hello in one short sentence."])
        )
        sample = (
            result.generations[0][0].text
            if hasattr(result, "generations") and result.generations
            else str(result)
        )
        return JSONResponse(status_code=200, content={"ok": True, "mode": "ollama", "sample": sample})
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"ok": False, "error": str(e), "traceback": traceback.format_exc()},
        )


# ---- Admin bootstrap -----------------------------------------------
@app.post("/admin/bootstrap")
async def admin_bootstrap(
    req: AdminBootstrapRequest,
    x_admin_token: str | None = Header(None),
    token: str | None = None,
):
    ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "dev-token")
    if (x_admin_token or token) != ADMIN_TOKEN:
        return JSONResponse(status_code=403, content={"ok": False, "error": "Invalid admin token"})

    try:
        from data import refresh_products_from_site
    except Exception as e:
        return JSONResponse(status_code=500, content={"ok": False, "error": f"Scraper unavailable: {e}"})

    try:
        count, saved = await asyncio.to_thread(
            lambda: refresh_products_from_site(req.seeds, out_path=req.out, limit=req.limit, delay=req.delay)
        )
        return JSONResponse(status_code=200, content={"ok": True, "count": count, "saved": saved})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"ok": False, "error": str(e), "traceback": traceback.format_exc()},
        )


# ---- Serve frontend static files if in same directory --------------
_here = os.path.dirname(os.path.abspath(__file__))
if os.path.exists(os.path.join(_here, "index.html")):
    app.mount("/", StaticFiles(directory=_here, html=True), name="static")


# ---- Entry point ---------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    print("\n" + "=" * 55)
    print("  ABFRL SYNAPSE Backend")
    print(f"  API:      http://localhost:{port}/api/health")
    print(f"  Frontend: http://localhost:{port}  (or open index.html directly)")
    print("=" * 55 + "\n")
    uvicorn.run("server_api:app", host="0.0.0.0", port=port, reload=True)
