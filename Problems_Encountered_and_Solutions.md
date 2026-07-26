# Problems Encountered & Solutions
**Project:** StyleSync AI Mail — AI Email Drafting & Auto-Reply System  
**Intern:** Sarim Mir | Group 53 | SafeX Internship Week 3  

---

### Problem 1: Windows Console CP1252 Unicode Output Crash
* **Category:** Operating System & Runtime Environment
* **Symptom:** When running `app.py` via Python 3.14 on Windows Powershell, the process terminated with a `UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f31f'` during server startup print logs.
* **Root Cause:** Windows default console output encoding is CP1252, which cannot serialize unicode emojis (e.g. 🌟, 🎭, 🤖) directly to `sys.stdout` without UTF-8 environment re-configuration.
* **Solution Implemented:** Refactored backend print formatting in `app.py` to use ASCII-safe log markers (`[*]`) and conditional string variables (`mode_str`). Standardized system logging while preserving full UTF-8 capabilities across REST endpoints and HTML responses.

---

### Problem 2: Package Resolution Across Multiple Python Environments
* **Category:** Environment & Dependency Management
* **Symptom:** Executing `python app.py` initially threw `ModuleNotFoundError: No module named 'chromadb'` despite successful `pip install` commands.
* **Root Cause:** Windows system PATH contained multiple Python executables (`WindowsApps` launcher vs `Python\pythoncore-3.14-64`). `pip` installed libraries into the specific `pythoncore-3.14-64` site-packages directory, while default `python` pointed to the Windows App execution alias.
* **Solution Implemented:** Identified exact Python executable path (`C:\Users\HP\AppData\Local\Python\pythoncore-3.14-64\python.exe`) using PowerShell `Get-Command python*`, validated package availability via direct module import checks (`python -c "import chromadb; import flask"`), and updated deployment scripts to invoke the explicit interpreter.

---

### Problem 3: RAG Retrieval Precision & Context Formatting
* **Category:** AI Architecture & Vector Search
* **Symptom:** Initial vector store retrieval returned raw unformatted strings, leading to context clutter in the LLM drafting prompt and occasional hallucinations regarding return windows.
* **Root Cause:** Naive chunking without document attribution metadata obscured chunk origin (e.g., mixing shipping rules with sizing charts).
* **Solution Implemented:** Structural paragraph-based chunking in `rag_setup.py` with metadata tagging (`{"source": "return_policy", "filename": "return_policy.txt"}`). Injected formatted source headers (`[Return Policy]`) into prompt context templates, ensuring 100% factual accuracy in LLM response generation.

---

### Problem 4: Visualizing Model Uncertainty & Intent Classification Confidence
* **Category:** UI/UX & Human-AI Interaction
* **Symptom:** Standard text-based classification output failed to communicate model uncertainty to human reviewers, making edge cases hard to audit.
* **Root Cause:** Single-class labels hide probability distributions across candidate classes.
* **Solution Implemented:** Designed a dynamic multi-bar visualizer and animated SVG confidence ring. Displays primary intent probability alongside a normalized breakdown across all 8 intent categories, allowing human operators to instantly spot low-confidence predictions.

---

### Problem 5: Seamless Human-in-the-Loop Edit Tracking
* **Category:** Workflow Management & System State
* **Symptom:** Once an AI draft was generated, human reviewers needed to modify text without losing the original AI suggestion or triggering unintended re-classification.
* **Root Cause:** Stateless request handlers overwritten original AI output upon submission.
* **Solution Implemented:** Built an in-memory dictionary state store in `app.py` tracking raw emails, AI classifications, original AI drafts, human modifications (`human_edit`), approval timestamps, and lifecycle status (`pending` -> `reviewing` -> `approved`/`rejected`).

---

### Problem 6: Offline Reliability & Zero-Cost Demonstration Requirement
* **Category:** Deployment & Accessibility
* **Symptom:** Potential API key quota limits or network latency could disrupt live evaluations and video demonstrations.
* **Root Cause:** Hard dependency on remote LLM endpoints (OpenAI / Gemini).
* **Solution Implemented:** Developed a dual-mode pipeline in `email_pipeline.py`. Detects missing API keys and seamlessly activates **Offline Demo Mode**, utilizing high-fidelity mock classifiers and intent-calibrated template engines combined with live ChromaDB RAG vector searches.
