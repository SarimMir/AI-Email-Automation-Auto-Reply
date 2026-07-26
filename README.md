# 🌟 StyleSync AI Mail
### AI-Powered Email Drafting & Auto-Reply System
**SafeX Internship — Week 3 | Group 53**

> **Target Company:** StyleSync — E-commerce Clothing Brand  
> **Difficulty:** Advanced | **Tools:** Python, Flask, ChromaDB, OpenAI/Gemini, RAG

---

## 📋 Project Overview

StyleSync AI Mail is a **full-stack AI email assistant** that automatically classifies incoming customer emails into 8 intent categories and drafts intelligent, context-aware replies — with a mandatory **human-review gate** before any email is sent.

Built as a premium web application (not just a script), it stands out with a **glassmorphism dark-mode UI**, real-time streaming AI responses, RAG-powered replies, confidence scoring, and an analytics dashboard.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🧠 **Intent Classification** | 8 categories with confidence scores per class |
| 📚 **RAG Knowledge Base** | ChromaDB with return policy, sizing & shipping docs |
| ✍️ **AI Draft Replies** | Contextual, on-brand replies using LLM + RAG |
| 👁️ **Human Review Gate** | Edit, Approve, or Reject before sending |
| 📊 **Analytics Dashboard** | Intent distribution, urgency & sentiment charts |
| 📋 **Prompt Template Docs** | All 4 prompts documented, interactive UI panel |
| 🎭 **Demo Mode** | Runs fully without any API key |
| ⚡ **Streaming UI** | Token-by-token typewriter animation |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│            FRONTEND (HTML / CSS / JS)               │
│   Glassmorphism UI — Inbox / Review / Analytics     │
└──────────────────────┬──────────────────────────────┘
                       │ REST API (fetch)
┌──────────────────────▼──────────────────────────────┐
│              BACKEND (Python / Flask)               │
│  /classify  /draft  /approve  /reject  /analytics   │
└──────────┬────────────────────────┬─────────────────┘
           │                        │
   ┌───────▼────────┐     ┌─────────▼──────────┐
   │  LLM API       │     │  ChromaDB (RAG)     │
   │  OpenAI GPT-4o │     │  Brand Knowledge    │
   │  or Gemini     │     │  Base (21 chunks)   │
   └────────────────┘     └────────────────────┘
```

---

## 📁 File Structure

```
safex-week3/
├── app.py                    ← Flask REST API (9 routes)
├── email_pipeline.py         ← AI classify + draft engine
├── rag_setup.py              ← ChromaDB RAG knowledge base
├── prompt_templates.py       ← 4 documented prompt templates
├── sample_emails.py          ← 20 real-world customer emails
├── requirements.txt          ← Python dependencies
├── .env.example              ← API key template
├── knowledge_base/
│   ├── return_policy.txt     ← 30-day return/exchange policy
│   ├── sizing_guide.txt      ← Men's & Women's size charts
│   └── shipping_info.txt     ← Domestic & international shipping
└── frontend/
    ├── index.html            ← Premium glassmorphism layout
    ├── style.css             ← Dark-mode + micro-animations
    └── app.js                ← Chart.js + streaming + review flow
```

---

## 🎯 Intent Classification Taxonomy (8 Categories)

| Intent | Example Trigger | Tone |
|---|---|---|
| 📦 Order Status | "where is my order", "tracking" | Informative |
| 🔄 Return/Exchange | "return", "refund", "exchange" | Empathetic |
| 📏 Sizing Help | "size", "measurements", "fit" | Helpful |
| ⚠️ Complaint | "disappointed", "wrong item", "damaged" | Apologetic |
| ⭐ Compliment | "love", "amazing", "great quality" | Warm |
| 🚚 Shipping Delay | "late", "delayed", "hasn't arrived" | Reassuring |
| 💳 Payment Issue | "double billed", "charge", "not processed" | Urgent |
| 💬 General Inquiry | everything else | Neutral |

---

## 🧠 Prompt Templates (4 Templates)

### PT-001 — Intent Classifier
Classifies email into one of 8 intents with confidence scores, urgency level, sentiment, and key entities.  
**Output:** JSON with `primary_intent`, `confidence_scores`, `urgency`, `sentiment`

### PT-002 — Reply Drafter
Generates a contextual, on-brand reply using classified intent + RAG context from the knowledge base.  
**Output:** Plain-text customer service email

### PT-003 — Tone Adjuster
Rewrites a draft in a different tone (formal/casual/empathetic/concise) without changing facts.

### PT-004 — Action Summarizer
Generates a concise action checklist for the human reviewer about what to do after approving.

---

## 📧 Sample Emails (20 Total)

| Category | Count |
|---|---|
| Order Status | 3 |
| Return/Exchange | 3 |
| Sizing Help | 2 |
| Complaint | 3 |
| Compliment | 2 |
| Shipping Delay | 2 |
| Payment Issue | 2 |
| General Inquiry | 3 |

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.9+
- Git

### Install Dependencies
```bash
python -m pip install flask flask-cors openai chromadb python-dotenv sentence-transformers
```

### Configure API Key (Optional)
Copy `.env.example` to `.env` and add your key:
```env
# Option 1: OpenAI
OPENAI_API_KEY=sk-...

# Option 2: Google Gemini
GEMINI_API_KEY=AIza...
```
> **Note:** If no key is provided, the app runs in **Demo Mode** automatically.

### Run the Server
```bash
python app.py
```
Then open: **http://localhost:5000**

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/status` | Health check + system info |
| GET | `/api/emails` | List all emails with status |
| GET | `/api/email/<id>` | Full email detail |
| POST | `/api/process/<id>` | Classify + Draft in one call |
| POST | `/api/approve/<id>` | Human approve (with optional edit) |
| POST | `/api/reject/<id>` | Human reject draft |
| GET | `/api/analytics` | Aggregated analytics data |
| GET | `/api/prompt-templates` | All prompt template docs |
| POST | `/api/reset` | Reset demo to initial state |

---

## 📊 Demo Mode vs Live Mode

| Feature | Demo Mode | Live Mode |
|---|---|---|
| API Key Required | ❌ No | ✅ Yes |
| Intent Classification | Mock (uses known labels) | Real LLM call |
| Draft Generation | Pre-written templates | Real LLM + RAG |
| RAG Context Retrieval | ✅ Real ChromaDB | ✅ Real ChromaDB |
| Confidence Scores | Randomized realistic | Real scores |

---

## 📚 Skills Demonstrated

- **Prompt Engineering** — Multi-stage pipeline with few-shot examples
- **RAG (Retrieval-Augmented Generation)** — ChromaDB vector store
- **Applied AI/ML** — LLM API integration (OpenAI / Gemini)
- **Business Process Analysis** — E-commerce customer support workflow
- **Full-Stack Development** — Flask REST API + Premium web UI
- **AI Solution Design** — Human-in-the-loop review architecture

---

## 🗂️ Submission Requirements (Week 3)

- [x] Working prototype with sample input/output
- [x] Prompt template documentation (4 templates, in-app panel)
- [x] Before/after example emails (20 sample emails)
- [x] GitHub Repository ← **this repo**
- [ ] Weekly Progress Report (PDF)
- [ ] Daily Work Log
- [ ] Demo Video (5-10 min, HD, face visible)
- [ ] Presentation Slides
- [ ] Problems Encountered & Solutions
- [ ] Next Week's Plan

---

## 👤 Author

**Sarim Mir** — Group 53 | SafeX AI Internship Week 3  
GitHub: [@SarimMir](https://github.com/SarimMir)

---

## 📝 Notes

- **Company substitution:** Used *StyleSync* as the target e-commerce clothing brand (fictional brand representing a Pakistani fashion e-commerce company in the same space as Khaadi, Generation, etc.)
- **No emails are actually sent** — the "Approve" action marks an email as sent in the demo but does not use SMTP. This is intentional per the human-review requirement.
- **Demo mode** was built to allow full functionality without API costs during demonstration.
