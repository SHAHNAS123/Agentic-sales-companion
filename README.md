````md
# ABFRL SYNAPSE — Agentic AI Sales Companion

![ABFRL SYNAPSE](https://img.shields.io/badge/ABFRL-SYNAPSE-6d28d9?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat-square&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=flat-square&logo=javascript)
![HTML5](https://img.shields.io/badge/HTML5-Frontend-E34F26?style=flat-square&logo=html5)
![CSS3](https://img.shields.io/badge/CSS3-UI-1572B6?style=flat-square&logo=css3)

---

## Overview

**ABFRL SYNAPSE** is an AI-powered retail intelligence platform built to solve the fragmented customer journey problem across web, mobile, WhatsApp, and in-store channels. It introduces a multi-agent AI system that delivers personalized recommendations, intelligent support, seamless checkout, and premium omnichannel experiences. :contentReference[oaicite:0]{index=0}

Traditional retail systems often separate customer touchpoints, causing inconsistent experiences, repeated interactions, and lost sales opportunities. SYNAPSE unifies these channels through collaborative AI agents that act like a smart digital sales team. :contentReference[oaicite:1]{index=1}

---

## Problem Statement

Modern premium retail customers expect:

- Personalized recommendations  
- Seamless journeys across channels  
- Fast support and checkout  
- Smart offers and loyalty rewards  
- Consistent premium brand experience  

However, disconnected systems create:

- Poor customer engagement  
- Lost cross-sell / upsell opportunities  
- Reduced loyalty  
- Lower conversion rates  
- Broken customer trust  



---

## Our Solution — Multi-Agent AI Architecture

```text
Customer Request
      ↓
Sales Agent
      ↓
Recommendation Agent
      ↓
Inventory Agent
      ↓
Loyalty Agent
      ↓
Payment Agent
      ↓
Support Agent
      ↓
Premium Customer Experience
````

Each AI agent has a specialized role and works together to guide users from product discovery to successful purchase completion.

---

## Core Agents

| Agent                | Responsibility                              |
| -------------------- | ------------------------------------------- |
| Sales Agent          | Understands intent and manages conversation |
| Recommendation Agent | Suggests personalized outfits/products      |
| Inventory Agent      | Checks product availability                 |
| Loyalty Agent        | Applies offers, coupons, rewards            |
| Payment Agent        | Handles checkout flow                       |
| Support Agent        | Post-purchase support & feedback            |



---

## Key Features

* Omnichannel retail experience
* AI-powered product recommendations
* Real-time inventory awareness
* Smart loyalty & offers engine
* Integrated payment workflow
* WhatsApp commerce support
* In-store digital assistance
* Scalable modular architecture
* Premium customer engagement system

---

## Tech Stack

| Layer     | Technology                      |
| --------- | ------------------------------- |
| Frontend  | HTML, CSS, JavaScript, React.js |
| Mobile    | React Native                    |
| Backend   | Python, FastAPI                 |
| Database  | PostgreSQL, ChromaDB            |
| AI Engine | LangChain, Grok API             |
| Messaging | Twilio                          |
| Payments  | Razorpay                        |
| Tools     | GitHub, VS Code, Figma          |

---

## Project Structure

```bash
abfrl/
├── index.html
├── style.css
├── script.js
├── server_api.py
├── agent.py
├── data.py
├── fetch_abfrl.py
├── requirements.txt
├── .env
└── data/
    └── products.json
```



---

## How It Works

### Frontend Flow

```text
User enters query
      ↓
UI captures request
      ↓
Detects intent
(recommendation / loyalty / payment / support)
      ↓
Calls Backend API
      ↓
Agent generates response
      ↓
Response shown to customer
```

### Backend Flow

```text
FastAPI Backend
      ↓
Agent Engine
      ↓
AI / Rule Logic
      ↓
Database / Inventory
      ↓
Return Smart Response
```

---

## API Endpoints

| Method | Endpoint         | Description            |
| ------ | ---------------- | ---------------------- |
| GET    | /api/health      | Health check           |
| POST   | /api/chat        | Chat with Sales Agent  |
| POST   | /api/recommend   | Product recommendation |
| POST   | /api/payment     | Payment summary        |
| POST   | /api/run_flow    | Full demo flow         |
| GET    | /api/llm_test    | AI connectivity test   |
| POST   | /admin/bootstrap | Product bootstrap      |



---

## Installation

## 1. Clone Repository

```bash
git clone https://github.com/your-username/abfrl-synapse.git
cd abfrl-synapse
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Run Backend

```bash
python server_api.py
```

or

```bash
uvicorn server_api:app --reload --port 8000
```

## 4. Launch App

Open:

```text
http://localhost:8000
```

or directly open `index.html`

---

## Business Impact

* Higher conversion rates
* Increased Average Order Value (AOV)
* Better upselling and cross-selling
* Reduced cart abandonment
* Faster support resolution
* Improved customer retention
* Stronger brand loyalty



---

## Why This Project Matters

SYNAPSE transforms retail from a transactional process into an intelligent customer experience. Instead of static shopping flows, users interact with smart AI agents that understand intent, personalize journeys, and reduce friction across every touchpoint.

---

## Future Enhancements

* Voice AI shopping assistant
* AR virtual try-on
* Predictive analytics dashboard
* Smart store kiosks
* Multilingual AI support
* Customer behavior forecasting
* Live order tracking assistant

---

## Team SYNAPSE

Built for **EY Techathon 6.0**

* Shahnas M
* Mekha S R
* Bhargavi N
* Rinu Antony



---

## License

This project was created for innovation, hackathon demonstration, and educational purposes.

---

## Contact

**Shahnas M**
BTech AI & ML Student
Developer • Innovator • Problem Solver

---

```
```
