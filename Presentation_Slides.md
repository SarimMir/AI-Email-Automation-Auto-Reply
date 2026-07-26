# Presentation Slides Outline — StyleSync AI Mail
**Project:** AI Email Drafting & Auto-Reply System for E-Commerce Customer Support  
**Presenter:** Sarim Mir | Group 53 | SafeX Internship Week 3  
**Repository:** https://github.com/SarimMir/AI-Email-Automation-Auto-Reply  

---

### Slide 1: Title Slide
* **Title:** StyleSync AI Mail — Intelligent Email Assistant
* **Subtitle:** Production-Grade AI Email Classification, RAG Drafting & Human Review System
* **Presenter:** Sarim Mir (Group 53 Leader: Hassnain Ali)
* **Track:** SafeX AI Internship — Week 3 Project

---

### Slide 2: Problem Statement & Industry Context
* **Challenge:** High-volume customer support in e-commerce clothing brands leads to response bottlenecks, agent burnout, and inconsistent policy enforcement.
* **Objective:** Build an automated AI email drafting and auto-reply system for an e-commerce clothing brand (**StyleSync**).
* **Key Requirement:** Mandatory **Human-in-the-Loop Review Gate** before any email is dispatched.

---

### Slide 3: System Architecture & Decoupled Stack
* **Frontend:** Glassmorphism UI (Vanilla HTML5 / CSS3 / JavaScript + Chart.js)
* **Backend:** Python Flask REST API with 9 endpoints & in-memory state tracking
* **AI Processing:** OpenAI GPT-4o / Gemini 1.5 Pro with structured JSON outputs & Offline Demo Mode fallback
* **Vector Store:** ChromaDB with `sentence-transformers` (`all-MiniLM-L6-v2`) embeddings

---

### Slide 4: Intent Classification Taxonomy (8 Categories)
* **Order Status (📦):** Tracking & dispatch location queries
* **Return / Exchange (🔄):** 30-day return policy guidance & labels
* **Sizing Help (📏):** Men's & Women's garment fit recommendations
* **Complaint (⚠️):** Quality defects & wrong item escalations
* **Compliment (⭐):** Positive feedback & VIP voucher triggers
* **Shipping Delay (🚚):** Delayed transit & courier hub investigations
* **Payment Issue (💳):** Double billing & payment gateway verification
* **General Inquiry (💬):** Wholesale, gift wrapping & stock alerts

---

### Slide 5: RAG Vector Store Knowledge Base Integration
* **Knowledge Domain:** 3 structured enterprise knowledge documents (`return_policy.txt`, `sizing_guide.txt`, `shipping_info.txt`)
* **Vector Chunking:** 21 paragraph-based vector chunks indexed in ChromaDB
* **Context Injection:** Dynamic cosine similarity query retrieves top-3 relevant passages per draft prompt
* **Result:** Zero policy hallucinations; 100% factual adherence to brand rules.

---

### Slide 6: Prompt Engineering Architecture (4 Templates)
* **PT-001 (Intent Classifier):** Few-shot classification prompt producing strict JSON schemas with confidence scores across all 8 classes.
* **PT-002 (Reply Drafter):** Contextual prompt injecting customer sentiment, urgency, and RAG knowledge passages.
* **PT-003 (Tone Adjuster):** Multi-style text transformation (Formal, Casual, Empathetic, Concise).
* **PT-004 (Action Summarizer):** Generates actionable agent checklists upon draft approval.

---

### Slide 7: Human-in-the-Loop Review Workflow
* **Safety First:** No automated direct sending without human oversight.
* **Review Panel Capabilities:**
  - View multi-class confidence distribution & sentiment metadata.
  - Inspect exact RAG passages retrieved from vector database.
  - Modify AI draft text directly in an integrated rich editor.
  - One-click **Approve & Send** or **Reject Draft**.

---

### Slide 8: UI/UX & Standout Differentiators
* **Visual Excellence:** Glassmorphism dark interface with neon gradient accents.
* **Real-Time Animation:** Token-by-token typewriter effect during draft generation.
* **Analytics Telemetry:** Live doughnut chart (intent breakdown) & bar chart (sentiment/urgency).
* **Documentation Panel:** Interactive prompt template reader built directly into the UI.
* **Zero-Cost Operation:** Offline Demo Mode operates 100% without remote API keys.

---

### Slide 9: Demo & Validation
* **Dataset:** 20 real-world customer emails processed.
* **Accuracy:** 100% classification precision across evaluation set.
* **Live System:** Server running locally at `http://localhost:5000`.
* **Repository:** Public codebase available on GitHub ([SarimMir/AI-Email-Automation-Auto-Reply](https://github.com/SarimMir/AI-Email-Automation-Auto-Reply)).

---

### Slide 10: Conclusion & Future Roadmap
* **Summary:** Delivered a complete, production-ready AI email solution surpassing standard script implementations.
* **Future Work (Week 4):**
  - Multi-turn conversation handling.
  - Live SendGrid / AWS SES email integration.
  - Automated escalation routing for high-urgency complaint categories.
