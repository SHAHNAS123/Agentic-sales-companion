# ABfRL — Agentic AI Sales Companion

![ABFRL SYNAPSE](https://img.shields.io/badge/ABFRL-SYNAPSE-6d28d9?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat-square\&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square\&logo=python)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=flat-square\&logo=javascript)
![HTML5](https://img.shields.io/badge/HTML5-Frontend-E34F26?style=flat-square\&logo=html5)
![CSS3](https://img.shields.io/badge/CSS3-UI-1572B6?style=flat-square\&logo=css3)

---

## Overview

**ABFRL SYNAPSE** is an AI-powered retail intelligence platform designed to solve fragmented customer journeys across web, mobile, WhatsApp, and in-store channels. It uses a multi-agent AI architecture to deliver personalized recommendations, seamless checkout, loyalty integration, and premium omnichannel customer experiences.

The platform transforms traditional shopping flows into intelligent conversations where multiple AI agents collaborate like a smart digital sales team.

---

## Problem Statement

Modern retail customers expect:

* Personalized recommendations
* Connected journeys across channels
* Fast support and checkout
* Smart loyalty rewards
* Premium and consistent experiences

However, disconnected systems often lead to:

* Repeated customer interactions
* Missed cross-sell opportunities
* Lower conversions
* Poor engagement
* Reduced brand trust

---

## Solution Architecture

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
```

---

## Core Agents

| Agent                | Responsibility                                   |
| -------------------- | ------------------------------------------------ |
| Sales Agent          | Understands user intent and manages conversation |
| Recommendation Agent | Suggests personalized products and outfits       |
| Inventory Agent      | Checks real-time product availability            |
| Loyalty Agent        | Applies rewards, coupons, and offers             |
| Payment Agent        | Handles checkout and order summary               |
| Support Agent        | Manages post-purchase support and feedback       |

---

## Key Features

* Omnichannel retail experience
* AI-powered recommendations
* Real-time inventory awareness
* Loyalty and offers engine
* Smart checkout workflow
* WhatsApp commerce support
* In-store digital assistance
* Scalable modular system
* Premium customer engagement

---

## Tech Stack

| Layer      | Technology             |
| ---------- | ---------------------- |
| Frontend   | HTML, CSS, JavaScript  |
| Web App    | React.js               |
| Mobile App | React Native           |
| Backend    | Python, FastAPI        |
| Database   | PostgreSQL, ChromaDB   |
| AI / LLM   | LangChain, Grok API    |
| Messaging  | Twilio                 |
| Payments   | Razorpay               |
| Tools      | GitHub, VS Code, Figma |

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
User enters request
      ↓
Intent detected
      ↓
API request sent
      ↓
Agent processes request
      ↓
Response displayed
```

### Backend Flow

```text
FastAPI Server
      ↓
Agent Engine
      ↓
AI Logic / Rules
      ↓
Inventory / Data Layer
      ↓
Smart Response
```

---

## API Endpoints

| Method | Endpoint         | Description            |
| ------ | ---------------- | ---------------------- |
| GET    | /api/health      | Health check           |
| POST   | /api/chat        | Chat with Sales Agent  |
| POST   | /api/recommend   | Product recommendation |
| POST   | /api/payment     | Checkout summary       |
| POST   | /api/run_flow    | Full demo flow         |
| GET    | /api/llm_test    | AI connectivity test   |
| POST   | /admin/bootstrap | Product data bootstrap |

---

## Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/abfrl-synapse.git
cd abfrl-synapse
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Backend

```bash
python server_api.py
```

or

```bash
uvicorn server_api:app --reload --port 8000
```

### 4. Launch Application

Open:

```text
http://localhost:8000
```

or directly open `index.html`

---

## Business Impact

* Increased conversion rates
* Higher average order value
* Better upselling and cross-selling
* Reduced cart abandonment
* Faster support resolution
* Improved retention and loyalty
* Stronger premium brand experience

---

## Future Enhancements

* Voice AI assistant
* AR virtual try-on
* Predictive analytics dashboard
* Smart store kiosks
* Multilingual AI support
* Live order tracking
* Customer behavior forecasting

---

## Team SYNAPSE

Built for **EY Techathon 6.0**

* Shahnas M
* Mekha S R
* Bhargavi N
* Rinu Antony

---

## License

Developed for innovation, hackathon demonstration, and educational purposes.

---

## Contact

**Shahnas M**
BTech AI & ML Student
Developer • Innovator • Problem Solver
