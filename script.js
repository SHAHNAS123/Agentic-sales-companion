// ============================================================
// ABFRL SYNAPSE – script.js
// Works standalone via Anthropic API (Claude-in-Claude).
// Also connects to Python backend at localhost:8000 if running.
// ============================================================

const ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages";
const BACKEND_URL = "http://localhost:8000";

const appState = {
  selectedProduct: null,
  paymentStatus: "idle",       // idle | pending | success
  backendAvailable: false,
  conversationHistory: [],
};

// ---- DOM refs -------------------------------------------------------
const chatElements = {
  chatbot:      document.getElementById("chatbot"),
  toggleButton: document.getElementById("chat-toggle"),
  closeButton:  document.getElementById("chat-close"),
  chatBody:     document.getElementById("chat-body"),
  btnRecommend: document.getElementById("btn-recommend"),
  btnLoyalty:   document.getElementById("btn-loyalty"),
  btnPurchase:  document.getElementById("btn-purchase"),
  chatInput:    document.getElementById("chat-input"),
  chatSend:     document.getElementById("chat-send"),
};

// ---- Utility: scroll -----------------------------------------------
function scrollChatToBottom() {
  chatElements.chatBody.scrollTop = chatElements.chatBody.scrollHeight;
}

// ---- Utility: typing indicator -------------------------------------
function showTypingIndicator() {
  const wrapper = document.createElement("div");
  wrapper.className = "message agent";
  wrapper.dataset.typing = "true";
  const inner = document.createElement("div");
  inner.className = "message-inner";
  const meta = document.createElement("div");
  meta.className = "message-meta";
  meta.textContent = "ABFRL AI Sales Agent is thinking…";
  const typing = document.createElement("div");
  typing.className = "typing";
  for (let i = 0; i < 3; i++) {
    const dot = document.createElement("span");
    dot.className = "typing-dot";
    typing.appendChild(dot);
  }
  inner.appendChild(meta);
  inner.appendChild(typing);
  wrapper.appendChild(inner);
  chatElements.chatBody.appendChild(wrapper);
  scrollChatToBottom();
  return wrapper;
}

function removeTypingIndicator(el) {
  if (el && el.parentNode) el.parentNode.removeChild(el);
}

// ---- Utility: append message ---------------------------------------
function appendMessage(sender, text, options = {}) {
  const { isHTML = false, metaLabel = "", afterRender } = options;
  const message = document.createElement("div");
  message.className = `message ${sender}`;
  const inner = document.createElement("div");
  inner.className = "message-inner";
  if (metaLabel) {
    const meta = document.createElement("div");
    meta.className = "message-meta";
    meta.textContent = metaLabel;
    inner.appendChild(meta);
  }
  const content = document.createElement("div");
  if (isHTML) { content.innerHTML = text; } else { content.textContent = text; }
  inner.appendChild(content);
  message.appendChild(inner);
  chatElements.chatBody.appendChild(message);
  if (typeof afterRender === "function") afterRender(inner);
  scrollChatToBottom();
}

function appendSystemMessage(text) {
  const div = document.createElement("div");
  div.className = "message-system";
  div.textContent = text;
  chatElements.chatBody.appendChild(div);
  scrollChatToBottom();
}

function showImage(url, caption = "", metaLabel = "Sales Agent") {
  appendMessage("agent",
    `<img src="${url}" alt="${caption || "image"}" class="product-img"/>` +
    (caption ? `<div style="color:#b2b3c0;font-size:11px;margin-top:6px">${caption}</div>` : ""),
    {
      isHTML: true, metaLabel,
      afterRender: (inner) => {
        const img = inner.querySelector(".product-img");
        if (img) { img.style.cursor = "pointer"; img.addEventListener("click", () => window.open(url, "_blank")); }
      },
    }
  );
}

// ---- Backend health ------------------------------------------------
const backendStatusEl = document.getElementById("backend-status");

function updateBackendStatus(isUp) {
  appState.backendAvailable = !!isUp;
  if (!backendStatusEl) return;
  if (isUp) {
    backendStatusEl.textContent = "Backend: online";
    backendStatusEl.className = "backend-status online";
  } else {
    backendStatusEl.textContent = "AI: ready";
    backendStatusEl.className = "backend-status offline";
  }
}

async function checkBackendHealth(timeoutMs = 2500) {
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(`${BACKEND_URL}/api/health`, { signal: controller.signal });
    clearTimeout(id);
    const data = await res.json();
    updateBackendStatus(data && data.status === "ok");
  } catch {
    clearTimeout(id);
    updateBackendStatus(false);
  }
}

// ---- Anthropic API (Claude-in-Claude) ------------------------------
const SALES_SYSTEM_PROMPT = `You are SYNAPSE, the ABFRL (Aditya Birla Fashion and Retail Limited) AI Sales Agent.
You orchestrate three specialised agents:
  • Sales Agent – handles conversation flow
  • Recommendation Agent – curates outfits from ABFRL brands
  • Payment Agent – manages checkout and order summaries

ABFRL Brands: Louis Philippe (Premium), Van Heusen (Premium), Allen Solly (Mid-Premium), Peter England (Value), Pantaloons (Value Fashion).

Sample products:
  - Louis Philippe Premium Wool Suit – Navy        ₹19,999  formal/wedding
  - Van Heusen Power Suit Blazer – Grey            ₹8,999   business
  - LP Classic Blazer – Black (on sale)            ₹8,499   versatile formal
  - LP Premium Cotton Formal Shirt – White         ₹2,999   office
  - Allen Solly Fit & Flare Work Dress – Navy      ₹2,999   women's workwear
  - LP Classic Polo T-Shirt – Navy                 ₹1,999   smart casual
  - LP Stretch Cotton Chinos – Khaki               ₹2,499   casual

Rules:
  - Be warm, knowledgeable, fashion-forward
  - Mention which agent is responding when relevant
  - Use <strong> for emphasis, <br/> for line breaks — HTML-safe output
  - Keep replies concise (3–6 lines) and end with a clear next action
  - For recommendations: include product name, price, occasion fit
  - For payments: show a clean order summary with amount and next steps`;

async function callAnthropicAPI(userPrompt) {
  const messages = [
    ...appState.conversationHistory,
    { role: "user", content: userPrompt },
  ];

  const response = await fetch(ANTHROPIC_API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "claude-sonnet-4-20250514",
      max_tokens: 1000,
      system: SALES_SYSTEM_PROMPT,
      messages,
    }),
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.error?.message || `API error ${response.status}`);
  }

  const data = await response.json();
  const replyText = data.content
    .map((b) => (b.type === "text" ? b.text : ""))
    .join("\n")
    .trim();

  // Keep last 20 turns in history
  appState.conversationHistory.push(
    { role: "user", content: userPrompt },
    { role: "assistant", content: replyText }
  );
  if (appState.conversationHistory.length > 20) {
    appState.conversationHistory = appState.conversationHistory.slice(-20);
  }
  return replyText;
}

// ---- Smart reply: tries backend first, then Anthropic API ----------
async function getAIReply(userMessage, systemHint = "") {
  const fullMessage = systemHint ? `${systemHint}\n\nCustomer says: ${userMessage}` : userMessage;

  // 1. Try Python backend
  if (appState.backendAvailable) {
    try {
      const res = await fetch(`${BACKEND_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
      });
      if (res.ok) {
        const data = await res.json();
        const reply = data.reply || data.recommendation || data.payment_summary;
        if (reply) return reply;
      }
    } catch { /* fall through */ }
  }

  // 2. Anthropic API
  return await callAnthropicAPI(fullMessage);
}

// ---- Agent label constants -----------------------------------------
const Agents = {
  SALES:          "Sales Agent",
  RECOMMENDATION: "Recommendation Agent",
  PAYMENT:        "Payment Agent",
};

// ---- Product images (varied picks) ---------------------------------
const PRODUCT_IMAGES = [
  "https://picsum.photos/id/1011/640/420",
  "https://picsum.photos/id/1005/640/420",
  "https://picsum.photos/id/1025/640/420",
  "https://picsum.photos/id/1062/640/420",
  "https://picsum.photos/id/1074/640/420",
];
function pickImage() {
  return PRODUCT_IMAGES[Math.floor(Math.random() * PRODUCT_IMAGES.length)];
}

// ---- Recommend flow ------------------------------------------------
async function recommendProduct() {
  appendMessage("user", "Recommend an outfit for me", { metaLabel: "You" });
  appendSystemMessage("Recommendation Agent activated — analysing your style profile…");
  const typing = showTypingIndicator();

  try {
    const reply = await getAIReply(
      "Recommend a premium ABFRL outfit for me. Include specific product name, price in INR, and why it suits the occasion.",
      "You are acting as the Recommendation Agent."
    );
    removeTypingIndicator(typing);

    const img = pickImage();
    appState.selectedProduct = { name: "ABFRL Premium Selection", category: "Premium Occasion Wear", price: "₹8,999", image: img };
    appState.paymentStatus = "idle";

    const html = `${reply}<br/>
      <img src="${img}" alt="Recommended product" class="product-img"/>
      <div class="inline-actions">
        <button class="btn tiny primary" id="inline-proceed-payment">Proceed to Payment</button>
      </div>`;

    appendMessage("agent", html, {
      isHTML: true, metaLabel: Agents.RECOMMENDATION,
      afterRender: (inner) => {
        const btn = inner.querySelector("#inline-proceed-payment");
        if (btn) btn.addEventListener("click", proceedToPayment);
        const imgEl = inner.querySelector(".product-img");
        if (imgEl) { imgEl.style.cursor = "pointer"; imgEl.addEventListener("click", () => window.open(img, "_blank")); }
      },
    });
    appendSystemMessage("Recommendation Agent handed control back to Sales Agent for payment orchestration.");
  } catch (err) {
    removeTypingIndicator(typing);
    appendMessage("agent",
      `I'd recommend our <strong>Louis Philippe Premium Wool Suit – Navy (₹19,999)</strong> — impeccably tailored for formal occasions and weddings.<br/>
       <div class="inline-actions"><button class="btn tiny primary" id="inline-fallback-pay">Proceed to Payment</button></div>`,
      { isHTML: true, metaLabel: Agents.RECOMMENDATION,
        afterRender: (inner) => {
          const btn = inner.querySelector("#inline-fallback-pay");
          if (btn) btn.addEventListener("click", proceedToPayment);
          appState.selectedProduct = { name: "LP Premium Wool Suit – Navy", category: "Suits", price: "₹19,999", image: pickImage() };
        }
      }
    );
  }
}

// ---- Loyalty flow --------------------------------------------------
async function checkLoyaltyOffers() {
  appendMessage("user", "Check loyalty offers", { metaLabel: "You" });
  const typing = showTypingIndicator();

  try {
    const reply = await getAIReply(
      "Show me my loyalty tier and current personalised offers.",
      "You are the Sales Agent. Describe Gold/Platinum loyalty tier benefits and active offers."
    );
    removeTypingIndicator(typing);

    const html = `${reply}
      <div class="inline-actions">
        <span class="badge">Personalised Loyalty Stack</span>
        <button class="btn tiny ghost" id="inline-use-offers">Use offers on an outfit</button>
      </div>`;
    appendMessage("agent", html, {
      isHTML: true, metaLabel: Agents.SALES,
      afterRender: (inner) => {
        const btn = inner.querySelector("#inline-use-offers");
        if (btn) btn.addEventListener("click", recommendProduct);
      },
    });
  } catch {
    removeTypingIndicator(typing);
    const html = `Your <strong>Gold tier</strong> loyalty benefits today:<br/>
      • Flat <strong>10% off</strong> on premium occasion wear<br/>
      • Extra <strong>₹750 off</strong> on purchases above ₹7,500<br/>
      • Priority alteration at select stores
      <div class="inline-actions">
        <button class="btn tiny ghost" id="inline-use-offers-fb">Use offers on an outfit</button>
      </div>`;
    appendMessage("agent", html, {
      isHTML: true, metaLabel: Agents.SALES,
      afterRender: (inner) => {
        const btn = inner.querySelector("#inline-use-offers-fb");
        if (btn) btn.addEventListener("click", recommendProduct);
      },
    });
  }
}

// ---- Payment flow --------------------------------------------------
async function proceedToPayment() {
  if (!appState.selectedProduct) {
    appendMessage("user", "Proceed to purchase", { metaLabel: "You" });
    const typing = showTypingIndicator();
    setTimeout(() => {
      removeTypingIndicator(typing);
      appendMessage("agent", "Let me fetch a recommendation first before we check out.", { metaLabel: Agents.SALES });
      recommendProduct();
    }, 500);
    return;
  }

  appendMessage("user", "Proceed to payment for this outfit", { metaLabel: "You" });
  const typing = showTypingIndicator();

  try {
    const p = appState.selectedProduct;
    const reply = await getAIReply(
      `Generate a clean order summary for: ${p.name}, price ${p.price}, category ${p.category}.`,
      "You are the Payment Agent. Present a concise order summary with delivery estimate."
    );
    removeTypingIndicator(typing);
    appState.paymentStatus = "pending";

    const html = `${reply}<br/>
      <img src="${p.image}" alt="${p.name}" class="product-img"/>
      <span class="badge">Payment Agent: Order Summary Ready</span>
      <div class="inline-actions">
        <button class="btn tiny primary" id="inline-pay-now">Pay Now</button>
        <button class="btn tiny ghost" id="inline-change-outfit">Change outfit</button>
      </div>`;

    appendMessage("agent", html, {
      isHTML: true, metaLabel: Agents.PAYMENT,
      afterRender: (inner) => {
        const payBtn = inner.querySelector("#inline-pay-now");
        const changeBtn = inner.querySelector("#inline-change-outfit");
        if (payBtn) payBtn.addEventListener("click", completePayment);
        if (changeBtn) changeBtn.addEventListener("click", () => {
          appState.selectedProduct = null;
          appState.paymentStatus = "idle";
          appendMessage("agent", "No problem — I'll loop the Recommendation Agent back in.", { metaLabel: Agents.SALES });
          recommendProduct();
        });
        const imgEl = inner.querySelector(".product-img");
        if (imgEl) { imgEl.style.cursor = "pointer"; imgEl.addEventListener("click", () => window.open(p.image, "_blank")); }
      },
    });
    appendSystemMessage("Payment Agent leading the flow — order summary and next action ready.");
  } catch {
    removeTypingIndicator(typing);
    const p = appState.selectedProduct;
    const html = `<strong>Order Summary</strong><br/>
      Item: <strong>${p.name}</strong><br/>
      Category: ${p.category}<br/>
      Payable: <strong>${p.price}</strong><br/>
      <span class="badge">Estimated delivery: 3–5 business days</span>
      <div class="inline-actions">
        <button class="btn tiny primary" id="inline-pay-now-fb">Pay Now</button>
      </div>`;
    appState.paymentStatus = "pending";
    appendMessage("agent", html, {
      isHTML: true, metaLabel: Agents.PAYMENT,
      afterRender: (inner) => {
        const btn = inner.querySelector("#inline-pay-now-fb");
        if (btn) btn.addEventListener("click", completePayment);
      },
    });
  }
}

// ---- Complete payment ----------------------------------------------
function completePayment() {
  if (appState.paymentStatus === "success") return;
  appendMessage("user", "Pay Now", { metaLabel: "You" });
  const typing = showTypingIndicator();
  setTimeout(() => {
    removeTypingIndicator(typing);
    appState.paymentStatus = "success";
    appState.selectedProduct = null;
    appendMessage("agent",
      `<strong>✓ Payment Successful!</strong> Your order has been confirmed.<br/>
       You'll receive an email confirmation shortly. Thank you for shopping with ABFRL!<br/>
       <span class="badge">Order confirmed</span> <span class="badge">Delivery: 3–5 business days</span>`,
      { isHTML: true, metaLabel: Agents.PAYMENT }
    );
    appendSystemMessage("End-to-end flow complete: Sales Agent → Recommendation Agent → Payment Agent → Confirmation.");
  }, 900);
}

// ---- Free-text chat ------------------------------------------------
async function sendChatMessage() {
  const input = chatElements.chatInput;
  if (!input) return;
  const text = input.value.trim();
  if (!text) return;
  input.value = "";

  appendMessage("user", text, { metaLabel: "You" });

  // Detect intent
  const lower = text.toLowerCase();
  let hint = "";
  if (/recommend|outfit|wear|suggest|style|fashion|dress|shirt|suit|kurti|saree|blazer/.test(lower))
    hint = "You are acting as the Recommendation Agent. Suggest a specific product with price.";
  else if (/loyalty|offer|discount|points|tier|reward|cashback/.test(lower))
    hint = "You are the Sales Agent. Describe loyalty tier benefits and current offers.";
  else if (/pay|checkout|purchase|buy|order|cart|payment/.test(lower))
    hint = "You are the Payment Agent. Generate a concise order summary.";

  const typing = showTypingIndicator();
  try {
    const reply = await getAIReply(text, hint);
    removeTypingIndicator(typing);
    appendMessage("agent", reply, { isHTML: true, metaLabel: Agents.SALES });
  } catch {
    removeTypingIndicator(typing);
    appendMessage("agent",
      "I'm here to help! Try asking me to <strong>recommend an outfit</strong>, check <strong>loyalty offers</strong>, or <strong>proceed to purchase</strong>.",
      { isHTML: true, metaLabel: Agents.SALES }
    );
  }
}

// ---- Chat open/close -----------------------------------------------
function openChatAsMain(open = true) {
  const backdrop = document.getElementById("chat-backdrop");
  if (open) {
    chatElements.chatbot.classList.add("open", "main");
    if (backdrop) { backdrop.classList.add("visible"); backdrop.hidden = false; }
    ensureInitialGreeting();
  } else {
    chatElements.chatbot.classList.remove("open", "main");
    if (backdrop) { backdrop.classList.remove("visible"); backdrop.hidden = true; }
  }
}

function toggleChat() {
  openChatAsMain(!chatElements.chatbot.classList.contains("open"));
}

let hasGreeted = false;
function ensureInitialGreeting() {
  if (hasGreeted) return;
  hasGreeted = true;
  appendMessage("agent",
    "Hi, I'm your <strong>ABFRL AI Sales Agent</strong>. I orchestrate our Recommendation and Payment agents to guide you from discovery to purchase. How can I assist you today?",
    { isHTML: true, metaLabel: Agents.SALES }
  );
  appendSystemMessage("Tap a quick action below to see the end-to-end multi-agent flow.");
}

// ---- Dev bootstrap panel -------------------------------------------
const devToggle    = document.getElementById("dev-toggle");
const devPanel     = document.getElementById("dev-panel");
const devBootstrap = document.getElementById("dev-bootstrap");
const devSeeds     = document.getElementById("dev-seeds");
const devLimit     = document.getElementById("dev-limit");
const devDelay     = document.getElementById("dev-delay");
const devToken     = document.getElementById("dev-token");
const devStatus    = document.getElementById("dev-status");

if (devToggle && devPanel) devToggle.addEventListener("click", () => { devPanel.hidden = !devPanel.hidden; });

async function runAdminBootstrap() {
  if (!devSeeds) return;
  const seeds = devSeeds.value.split(",").map((s) => s.trim()).filter(Boolean);
  if (!seeds.length) { devStatus.textContent = "Enter at least one seed URL"; return; }
  devStatus.textContent = "Starting…";
  try {
    const res = await fetch(`${BACKEND_URL}/admin/bootstrap`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "x-admin-token": devToken?.value || "" },
      body: JSON.stringify({ seeds, limit: parseInt(devLimit?.value || "30", 10), delay: parseFloat(devDelay?.value || "1.5"), out: null }),
    });
    const data = await res.json();
    devStatus.textContent = res.ok && data.ok ? `Saved ${data.count} products to ${data.saved}` : `Error: ${data.error}`;
  } catch (err) {
    devStatus.textContent = `Request failed: ${err.message}`;
  }
}
if (devBootstrap) devBootstrap.addEventListener("click", runAdminBootstrap);

// ---- Hero CTA buttons ----------------------------------------------
document.querySelectorAll("button[data-show-image]").forEach((btn) => {
  btn.addEventListener("click", () => {
    openChatAsMain(true);
    showImage(btn.dataset.image, btn.textContent.trim(), Agents.SALES);
  });
});

// ---- Wire all events -----------------------------------------------
chatElements.toggleButton.addEventListener("click", toggleChat);
chatElements.closeButton.addEventListener("click", toggleChat);
chatElements.btnRecommend.addEventListener("click", recommendProduct);
chatElements.btnLoyalty.addEventListener("click", checkLoyaltyOffers);
chatElements.btnPurchase.addEventListener("click", proceedToPayment);

const chatBackdrop = document.getElementById("chat-backdrop");
if (chatBackdrop) chatBackdrop.addEventListener("click", () => openChatAsMain(false));

if (chatElements.chatSend && chatElements.chatInput) {
  chatElements.chatSend.addEventListener("click", sendChatMessage);
  chatElements.chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendChatMessage(); }
  });
}

// ---- Init ----------------------------------------------------------
checkBackendHealth();
setInterval(checkBackendHealth, 8000);
openChatAsMain(true);
