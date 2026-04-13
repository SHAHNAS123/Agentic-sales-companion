"""
ABFRL SYNAPSE – agent.py
Recommendation, Payment, and Demo Flow agents.
Uses Ollama when available; falls back to smart rule-based responses.
"""

import os

# ---- Optional Ollama import ----------------------------------------
_OLLAMA_AVAILABLE = False
ollama_llm = None

try:
    from langchain_ollama import OllamaLLM
    _OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
    ollama_llm = OllamaLLM(model=_OLLAMA_MODEL)
    _OLLAMA_AVAILABLE = True
    print(f"[SYNAPSE] Ollama LLM loaded: {_OLLAMA_MODEL}")
except Exception as e:
    print(f"[SYNAPSE] Ollama not available ({e}). Using fallback responses.")


# ---- LLM helper ----------------------------------------------------
def _llm_generate(prompt: str) -> str:
    if _OLLAMA_AVAILABLE and ollama_llm:
        try:
            return str(ollama_llm.invoke(prompt))
        except Exception as e:
            print(f"[SYNAPSE] Ollama invoke error: {e}")
    return _rule_based_response(prompt)


def _rule_based_response(prompt: str) -> str:
    """Smart rule-based fallback when Ollama is not running."""
    p = prompt.lower()

    if any(w in p for w in ["recommend", "outfit", "suggest", "wear", "style", "fashion"]):
        return (
            "Based on your style profile, I recommend the "
            "<strong>Louis Philippe Premium Wool Suit – Navy (₹19,999)</strong>. "
            "Crafted from Super 120s wool with a full-canvas construction, it's perfect for "
            "formal occasions, business meetings, and weddings. "
            "Pair it with the <strong>Van Heusen Tech Smart Formal Shirt (₹2,299)</strong> "
            "for a complete power look.<br/>Would you like to proceed to checkout?"
        )

    if any(w in p for w in ["payment", "pay", "checkout", "purchase", "order", "buy"]):
        return (
            "<strong>Order Summary – Payment Agent</strong><br/>"
            "Item: Louis Philippe Premium Wool Suit – Navy<br/>"
            "Category: Suits / Occasion Wear<br/>"
            "Payable Amount: <strong>₹19,999</strong><br/>"
            "Estimated Delivery: 3–5 business days<br/>"
            "<span style='color:#36d399'>Secure payment via HDFC Visa ••••4242</span><br/>"
            "Ready to confirm? Click <strong>Pay Now</strong>."
        )

    if any(w in p for w in ["loyalty", "offer", "discount", "points", "tier", "reward"]):
        return (
            "Your <strong>Gold Tier</strong> loyalty profile has these active offers:<br/>"
            "• Flat <strong>10% off</strong> on premium occasion wear<br/>"
            "• Extra <strong>₹750 off</strong> on purchases above ₹7,500<br/>"
            "• Priority alteration service at select stores<br/>"
            "You have <strong>4,500 points</strong> — worth ₹450 in rewards.<br/>"
            "Would you like to apply these to a recommendation?"
        )

    if any(w in p for w in ["hello", "hi", "hey", "start", "help"]):
        return (
            "Hello! I'm your <strong>ABFRL AI Sales Agent</strong> — SYNAPSE.<br/>"
            "I can help you:<br/>"
            "• Discover and recommend premium outfits<br/>"
            "• Check your loyalty offers and rewards<br/>"
            "• Guide you through a seamless checkout<br/>"
            "What would you like to explore today?"
        )

    # Generic fallback
    return (
        "I'm here to help you discover the best of ABFRL's premium fashion portfolio — "
        "Louis Philippe, Van Heusen, Allen Solly, Peter England, and Pantaloons.<br/>"
        "Ask me to <strong>recommend an outfit</strong>, check <strong>loyalty offers</strong>, "
        "or <strong>proceed to purchase</strong>. How can I assist?"
    )


# ---- Public API ----------------------------------------------------
def get_recommendation(user_message: str = None, context: dict = None) -> str:
    """Recommendation Agent: returns a personalised outfit recommendation."""
    context = context or {}
    customer_id = context.get("customer_id", "ABFRL-C001")
    msg = user_message or "Recommend a premium outfit for me."

    prompt = f"""You are an expert ABFRL fashion recommendation agent serving customer {customer_id}.
Customer request: {msg}

Respond with a personalised outfit recommendation:
- Name a specific ABFRL product (brand: Louis Philippe, Van Heusen, Allen Solly, Peter England, or Pantaloons)
- Include the price in INR
- Briefly explain why it suits the occasion
- Keep it concise and use HTML tags like <strong> for emphasis
- End with a clear call-to-action (e.g., "Proceed to checkout?")"""

    return _llm_generate(prompt)


def get_payment_summary(product_name: str, price: str, category: str = "") -> str:
    """Payment Agent: returns a formatted order summary."""
    prompt = f"""You are the ABFRL Payment Agent. Generate a concise order summary for:
Product: {product_name}
Price: {price}
Category: {category or "Fashion"}

Include:
- Item name and price
- Estimated delivery (3-5 business days)
- Payment confirmation note
Use HTML <strong> tags for emphasis. Keep it brief."""

    return _llm_generate(prompt)


def run_demo_flow(context: dict = None) -> dict:
    """Full demo: Sales → Recommendation → Payment flow."""
    context = context or {}
    recommendation = get_recommendation(
        user_message="Show me a premium occasion wear outfit",
        context=context
    )
    payment_summary = get_payment_summary(
        product_name="Louis Philippe Premium Wool Suit – Navy",
        price="₹19,999",
        category="Suits / Occasion Wear"
    )
    return {
        "flow": "Sales Agent → Recommendation Agent → Payment Agent",
        "recommendation": recommendation,
        "payment_summary": payment_summary,
        "status": "demo_complete",
    }
