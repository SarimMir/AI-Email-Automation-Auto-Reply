"""
StyleSync AI Mail — Flask Backend
====================================
REST API serving the frontend and powering the AI email pipeline.
"""

import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from sample_emails import SAMPLE_EMAILS, INTENT_COLORS, INTENT_ICONS
from email_pipeline import classify_email, draft_reply, DEMO_MODE
from rag_setup import initialize_rag, get_collection_stats
from prompt_templates import PROMPT_TEMPLATE_DOCS

# ── App setup ────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR)
CORS(app)

# ── In-memory state (email status & drafts) ──────────────────────────────────
email_store = {}   # id → {email, classification, draft, status, human_edit}

def _init_email_store():
    """Pre-populate with sample emails (unclassified)."""
    for em in SAMPLE_EMAILS:
        email_store[em["id"]] = {
            "email": em,
            "classification": None,
            "draft": None,
            "status": "pending",   # pending | reviewing | approved | rejected
            "human_edit": None,
            "approved_at": None,
        }

_init_email_store()

# Initialize RAG on startup
print("[Server] Initializing RAG knowledge base...")
try:
    initialize_rag()
except Exception as e:
    print(f"[Server] RAG init warning: {e}")

# ── Frontend serving ─────────────────────────────────────────────────────────
@app.route("/")
def serve_index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(FRONTEND_DIR, filename)

# ── API Routes ───────────────────────────────────────────────────────────────

@app.route("/api/status")
def api_status():
    """Health check + system info."""
    rag_stats = get_collection_stats()
    pending = sum(1 for v in email_store.values() if v["status"] == "pending")
    reviewing = sum(1 for v in email_store.values() if v["status"] == "reviewing")
    approved = sum(1 for v in email_store.values() if v["status"] == "approved")
    rejected = sum(1 for v in email_store.values() if v["status"] == "rejected")
    return jsonify({
        "status": "ok",
        "demo_mode": DEMO_MODE,
        "rag": rag_stats,
        "email_counts": {
            "total": len(email_store),
            "pending": pending,
            "reviewing": reviewing,
            "approved": approved,
            "rejected": rejected,
        },
        "timestamp": datetime.utcnow().isoformat() + "Z",
    })


@app.route("/api/emails")
def api_emails():
    """Return list of all emails with their current status and classification."""
    result = []
    for eid, data in email_store.items():
        em = data["email"]
        clf = data["classification"]
        result.append({
            "id": eid,
            "sender": em["sender"],
            "subject": em["subject"],
            "timestamp": em["timestamp"],
            "status": data["status"],
            "intent": clf["primary_intent"] if clf else None,
            "urgency": clf["urgency"] if clf else None,
            "sentiment": clf["sentiment"] if clf else None,
            "confidence": max(clf["confidence_scores"].values()) if clf else None,
            "color": INTENT_COLORS.get(clf["primary_intent"], "#6366f1") if clf else "#666",
            "icon":  INTENT_ICONS.get(clf["primary_intent"], "💬") if clf else "📧",
        })
    # Sort: pending first, then by timestamp descending
    result.sort(key=lambda x: (x["status"] != "pending", x["timestamp"]), reverse=False)
    return jsonify(result)


@app.route("/api/email/<email_id>")
def api_email_detail(email_id):
    """Return full detail for a single email."""
    data = email_store.get(email_id)
    if not data:
        return jsonify({"error": "Email not found"}), 404

    em = data["email"]
    clf = data["classification"]
    drft = data["draft"]

    return jsonify({
        "id": email_id,
        "email": em,
        "classification": clf,
        "draft": drft,
        "status": data["status"],
        "human_edit": data["human_edit"],
        "approved_at": data["approved_at"],
        "intent_color": INTENT_COLORS.get(clf["primary_intent"], "#6366f1") if clf else "#666",
        "intent_icon":  INTENT_ICONS.get(clf["primary_intent"], "💬") if clf else "📧",
    })


@app.route("/api/classify/<email_id>", methods=["POST"])
def api_classify(email_id):
    """Run intent classification on an email."""
    data = email_store.get(email_id)
    if not data:
        return jsonify({"error": "Email not found"}), 404

    try:
        clf = classify_email(data["email"])
        email_store[email_id]["classification"] = clf
        email_store[email_id]["status"] = "reviewing"
        return jsonify({
            "success": True,
            "classification": clf,
            "intent_color": INTENT_COLORS.get(clf["primary_intent"], "#6366f1"),
            "intent_icon":  INTENT_ICONS.get(clf["primary_intent"], "💬"),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/draft/<email_id>", methods=["POST"])
def api_draft(email_id):
    """Generate a draft reply for a classified email."""
    data = email_store.get(email_id)
    if not data:
        return jsonify({"error": "Email not found"}), 404
    if not data["classification"]:
        return jsonify({"error": "Email not classified yet"}), 400

    try:
        drft = draft_reply(data["email"], data["classification"])
        email_store[email_id]["draft"] = drft
        return jsonify({"success": True, "draft": drft})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/process/<email_id>", methods=["POST"])
def api_process(email_id):
    """Classify + Draft in one call (convenience endpoint)."""
    data = email_store.get(email_id)
    if not data:
        return jsonify({"error": "Email not found"}), 404

    try:
        clf = classify_email(data["email"])
        email_store[email_id]["classification"] = clf

        drft = draft_reply(data["email"], clf)
        email_store[email_id]["draft"] = drft
        email_store[email_id]["status"] = "reviewing"

        return jsonify({
            "success": True,
            "classification": clf,
            "draft": drft,
            "intent_color": INTENT_COLORS.get(clf["primary_intent"], "#6366f1"),
            "intent_icon":  INTENT_ICONS.get(clf["primary_intent"], "💬"),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/approve/<email_id>", methods=["POST"])
def api_approve(email_id):
    """
    Human-review step: Approve a draft (optionally with edits).
    Body (JSON, optional): { "edited_text": "..." }
    """
    data = email_store.get(email_id)
    if not data:
        return jsonify({"error": "Email not found"}), 404
    if not data["draft"]:
        return jsonify({"error": "No draft to approve"}), 400

    body = request.get_json(silent=True) or {}
    edited_text = body.get("edited_text", None)

    email_store[email_id]["human_edit"] = edited_text
    email_store[email_id]["status"] = "approved"
    email_store[email_id]["approved_at"] = datetime.utcnow().isoformat() + "Z"

    final_text = edited_text if edited_text else data["draft"]["draft_text"]
    return jsonify({
        "success": True,
        "message": "Email approved and marked as sent ✓",
        "final_reply": final_text,
        "approved_at": email_store[email_id]["approved_at"],
    })


@app.route("/api/reject/<email_id>", methods=["POST"])
def api_reject(email_id):
    """Human-review step: Reject a draft and reset to pending."""
    data = email_store.get(email_id)
    if not data:
        return jsonify({"error": "Email not found"}), 404

    body = request.get_json(silent=True) or {}
    reason = body.get("reason", "No reason provided")

    email_store[email_id]["status"] = "rejected"
    email_store[email_id]["draft"] = None
    email_store[email_id]["classification"] = None

    return jsonify({
        "success": True,
        "message": f"Draft rejected. Reason: {reason}",
    })


@app.route("/api/analytics")
def api_analytics():
    """Return aggregated analytics data."""
    intent_counts = {}
    urgency_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
    sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0, "very_negative": 0}
    processed = 0
    approved = 0
    rejected = 0

    for data in email_store.values():
        clf = data["classification"]
        if clf:
            processed += 1
            intent = clf.get("primary_intent", "General Inquiry")
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
            urgency_counts[clf.get("urgency", "medium")] = urgency_counts.get(clf.get("urgency", "medium"), 0) + 1
            sent_key = clf.get("sentiment", "neutral")
            sentiment_counts[sent_key] = sentiment_counts.get(sent_key, 0) + 1

        if data["status"] == "approved":
            approved += 1
        elif data["status"] == "rejected":
            rejected += 1

    return jsonify({
        "total_emails": len(email_store),
        "processed": processed,
        "approved": approved,
        "rejected": rejected,
        "pending": len(email_store) - processed,
        "intent_distribution": [
            {
                "intent": k,
                "count": v,
                "color": INTENT_COLORS.get(k, "#6366f1"),
                "icon": INTENT_ICONS.get(k, "💬"),
            }
            for k, v in sorted(intent_counts.items(), key=lambda x: -x[1])
        ],
        "urgency_distribution": urgency_counts,
        "sentiment_distribution": sentiment_counts,
    })


@app.route("/api/prompt-templates")
def api_prompt_templates():
    """Return all prompt template documentation."""
    return jsonify(PROMPT_TEMPLATE_DOCS)


@app.route("/api/reset", methods=["POST"])
def api_reset():
    """Reset all email statuses to pending (for demo restarts)."""
    global email_store
    _init_email_store()
    return jsonify({"success": True, "message": "All emails reset to pending."})


if __name__ == "__main__":
    print("\n" + "="*55)
    print("  [*] StyleSync AI Mail -- Starting Server")
    print("="*55)
    mode_str = "DEMO (no API key needed)" if DEMO_MODE else "LIVE (LLM connected)"
    print(f"  Mode: {mode_str}")
    print(f"  URL:  http://localhost:5000")
    print("="*55 + "\n")
    app.run(debug=True, port=5000, use_reloader=False)
