"""
StyleSync AI Mail — Core Email Pipeline
=========================================
Handles intent classification and reply drafting using LLM + RAG.
Supports: OpenAI GPT-4o, Google Gemini, and a Demo/Mock mode (no API key needed).
"""

import os
import json
import random
import re
from datetime import datetime
from dotenv import load_dotenv

from prompt_templates import (
    CLASSIFICATION_SYSTEM_PROMPT,
    CLASSIFICATION_USER_PROMPT,
    DRAFTING_SYSTEM_PROMPT,
    DRAFTING_USER_PROMPT,
    REVIEW_SUMMARY_PROMPT,
)
from rag_setup import retrieve_context

load_dotenv()

# ── LLM Provider Detection ──────────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"

if not OPENAI_API_KEY and not GEMINI_API_KEY:
    DEMO_MODE = True
    print("[Pipeline] No API key found — running in DEMO mode.")

# ── Mock responses for Demo mode ───────────────────────────────────────────
MOCK_CLASSIFICATIONS = {
    "Order Status":    {"urgency": "medium", "sentiment": "neutral"},
    "Return/Exchange": {"urgency": "medium", "sentiment": "negative"},
    "Sizing Help":     {"urgency": "low",    "sentiment": "neutral"},
    "Complaint":       {"urgency": "high",   "sentiment": "very_negative"},
    "Compliment":      {"urgency": "low",    "sentiment": "positive"},
    "Shipping Delay":  {"urgency": "high",   "sentiment": "negative"},
    "Payment Issue":   {"urgency": "critical","sentiment": "very_negative"},
    "General Inquiry": {"urgency": "low",    "sentiment": "neutral"},
}

MOCK_REPLIES = {
    "Order Status": (
        "Dear {name},\n\n"
        "Thank you for reaching out about your order #{order_id}! 📦\n\n"
        "We completely understand your concern. Our records show your order is currently "
        "being processed and will be dispatched within the next 24 hours. You'll receive "
        "a tracking link via email as soon as it's on its way.\n\n"
        "If you haven't received shipping confirmation within 24 hours, please don't "
        "hesitate to reply to this email and we'll investigate immediately.\n\n"
        "Warm regards,\nStyleSync Support Team"
    ),
    "Return/Exchange": (
        "Dear {name},\n\n"
        "We're sorry to hear that your recent purchase didn't meet your expectations. "
        "Your satisfaction is our top priority!\n\n"
        "Great news — you're within our 30-day return window and fully eligible for a "
        "return or exchange. Here's how to proceed:\n\n"
        "1. Reply to this email with your order number\n"
        "2. We'll send you a prepaid return label within 24 hours\n"
        "3. Drop the package at any courier drop-off point\n"
        "4. Your refund will be processed within 5-7 business days upon receipt\n\n"
        "We hope to make this right for you! 🤝\n\n"
        "Warm regards,\nStyleSync Support Team"
    ),
    "Sizing Help": (
        "Dear {name},\n\n"
        "Happy to help you find the perfect fit! 📏\n\n"
        "Based on your measurements, we'd recommend going with a **Large** for a "
        "comfortable, true-to-fit feel. Our items generally run true to size, but for "
        "our denim collection, we suggest sizing up if you prefer a relaxed fit.\n\n"
        "You can also check the specific size guide on the product page by clicking "
        "the 'Size Guide' button — it has exact garment measurements for that item.\n\n"
        "If you're still unsure, feel free to share your exact measurements and we'll "
        "give you a personalized recommendation!\n\n"
        "Warm regards,\nStyleSync Support Team"
    ),
    "Complaint": (
        "Dear {name},\n\n"
        "We sincerely apologize for this experience — this is absolutely not the "
        "standard we hold ourselves to, and we completely understand your frustration.\n\n"
        "Please know that your concern is being treated as our highest priority. Here's "
        "what we'll do immediately:\n\n"
        "• We'll arrange a full replacement or refund — your choice\n"
        "• A prepaid return label will be sent to you within 24 hours\n"
        "• A quality report will be filed to prevent this from happening again\n\n"
        "We truly value your trust and want to make this right. Could you please reply "
        "with your order number and a photo of the issue? This will help us process "
        "your request immediately.\n\n"
        "Sincerely,\nStyleSync Support Team"
    ),
    "Compliment": (
        "Dear {name},\n\n"
        "Your message absolutely made our day! ⭐\n\n"
        "We work incredibly hard to ensure every piece that leaves our warehouse is "
        "crafted with care, and hearing that you love it means the world to our entire "
        "team. Thank you for taking the time to share this with us.\n\n"
        "As a thank you, use code STYLELOVE10 for 10% off your next order — our little "
        "way of saying we appreciate you!\n\n"
        "We can't wait to style you again soon. ✨\n\n"
        "With gratitude,\nStyleSync Support Team"
    ),
    "Shipping Delay": (
        "Dear {name},\n\n"
        "We sincerely apologize for the delay with your order — we understand how "
        "frustrating this must be, especially when you were counting on it arriving "
        "on time. 🚚\n\n"
        "We've escalated this to our courier partner for an immediate investigation. "
        "You should receive a status update within 24 hours. In most cases, delays "
        "like this are resolved within 1-2 additional business days.\n\n"
        "If your order doesn't arrive within 48 hours from now, we will either "
        "reship your order or issue a full refund — whichever you prefer.\n\n"
        "We're truly sorry for the inconvenience and appreciate your patience.\n\n"
        "Warm regards,\nStyleSync Support Team"
    ),
    "Payment Issue": (
        "Dear {name},\n\n"
        "We take billing concerns very seriously and want to resolve this for you "
        "as quickly as possible.\n\n"
        "We've flagged your account for an urgent review. Here's what happens next:\n\n"
        "• Our billing team will verify the transaction within 2-4 hours\n"
        "• If a duplicate charge is confirmed, the extra amount will be refunded "
        "within 3-5 business days\n"
        "• You'll receive an email confirmation once the refund is processed\n\n"
        "Please reply with your order number and the last 4 digits of the card used, "
        "so we can match your transaction records immediately.\n\n"
        "Warm regards,\nStyleSync Support Team"
    ),
    "General Inquiry": (
        "Dear {name},\n\n"
        "Thank you for reaching out to StyleSync! 💬\n\n"
        "We'd be happy to help with your query. To give you the most accurate answer, "
        "could you please provide a few more details about what you're looking for?\n\n"
        "In the meantime, you may find answers to common questions in our FAQ section "
        "at stylesync.com/faq, or feel free to chat with us directly.\n\n"
        "We'll get back to you with a full response within 24 hours.\n\n"
        "Warm regards,\nStyleSync Support Team"
    ),
}


# ── Helper functions ────────────────────────────────────────────────────────

def _extract_first_name(sender: str) -> str:
    """Try to extract first name from email address."""
    local = sender.split("@")[0]
    # Remove numbers and special chars, get first word
    name = re.sub(r'[^a-zA-Z.]', ' ', local).split()[0].capitalize()
    return name if name else "Valued Customer"


def _extract_order_id(text: str) -> str:
    """Extract first order ID pattern from text."""
    match = re.search(r'#?(SS-\d+)', text, re.IGNORECASE)
    return match.group(1) if match else "your order"


# ── Mock pipeline (Demo mode) ───────────────────────────────────────────────

def _mock_classify(email: dict) -> dict:
    """Simulate classification based on known intent field (demo mode)."""
    intent = email.get("intent", "General Inquiry")
    meta = MOCK_CLASSIFICATIONS.get(intent, MOCK_CLASSIFICATIONS["General Inquiry"])

    # Build confidence scores (high for primary, noise for others)
    scores = {}
    all_intents = list(MOCK_CLASSIFICATIONS.keys())
    remaining = 1.0
    primary_conf = round(random.uniform(0.68, 0.92), 2)
    scores[intent] = primary_conf
    remaining -= primary_conf

    others = [i for i in all_intents if i != intent]
    random.shuffle(others)
    for i, other in enumerate(others):
        if i == len(others) - 1:
            scores[other] = round(max(remaining, 0.0), 2)
        else:
            val = round(random.uniform(0.0, remaining / max(len(others) - i, 1)), 2)
            scores[other] = val
            remaining -= val

    body = email.get("body", "")
    return {
        "primary_intent": intent,
        "confidence_scores": scores,
        "urgency": meta["urgency"],
        "sentiment": meta["sentiment"],
        "key_entities": [_extract_order_id(body)] if "SS-" in body else [],
        "mode": "demo"
    }


def _mock_draft(email: dict, classification: dict) -> str:
    """Return a mock draft reply based on intent."""
    intent = classification.get("primary_intent", "General Inquiry")
    template = MOCK_REPLIES.get(intent, MOCK_REPLIES["General Inquiry"])
    name = _extract_first_name(email.get("sender", "customer@email.com"))
    order_id = _extract_order_id(email.get("body", ""))
    return template.format(name=name, order_id=order_id)


def _mock_action_summary(email: dict, classification: dict, draft: str) -> str:
    """Return a canned action summary for demo mode."""
    intent = classification.get("primary_intent", "General Inquiry")
    summaries = {
        "Order Status":    "• Check order dispatch status in fulfillment system\n• Update tracking if available\n• Escalate to warehouse if not yet dispatched",
        "Return/Exchange": "• Send prepaid return label to customer email\n• Reserve replacement item in inventory\n• Create return ticket in CRM",
        "Sizing Help":     "• No immediate action required\n• Flag if customer doesn't respond within 48 hours\n• Offer discount code if they place an order",
        "Complaint":       "• Escalate to QA team immediately\n• Initiate replacement or refund in payment system\n• File quality complaint report in CRM",
        "Compliment":      "• Log positive feedback in CRM\n• Add customer to VIP segment\n• Ensure discount code STYLELOVE10 is active",
        "Shipping Delay":  "• Contact courier partner with tracking ID\n• Get ETA update within 24 hours\n• Prepare refund/reship option if still delayed",
        "Payment Issue":   "• Verify transaction in payment gateway dashboard\n• Initiate refund if duplicate charge confirmed\n• Contact payment processor if pending",
        "General Inquiry": "• Review query for any actionable follow-up\n• Update FAQ if this question is frequent\n• Respond within SLA window",
    }
    return summaries.get(intent, "• Review and handle as appropriate")


# ── Real LLM pipeline ───────────────────────────────────────────────────────

def _call_openai(system: str, user: str, model: str = "gpt-4o", json_mode: bool = False) -> str:
    """Call OpenAI API."""
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        "temperature": 0.3,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    resp = client.chat.completions.create(**kwargs)
    return resp.choices[0].message.content.strip()


def _call_gemini(system: str, user: str, json_mode: bool = False) -> str:
    """Call Google Gemini API via openai-compatible endpoint."""
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(
        "gemini-1.5-pro",
        system_instruction=system
    )
    resp = model.generate_content(user)
    return resp.text.strip()


def _call_llm(system: str, user: str, json_mode: bool = False) -> str:
    """Route to available LLM."""
    if OPENAI_API_KEY:
        return _call_openai(system, user, json_mode=json_mode)
    elif GEMINI_API_KEY:
        return _call_gemini(system, user, json_mode=json_mode)
    raise RuntimeError("No LLM API key configured and DEMO_MODE is off.")


# ── Public API ──────────────────────────────────────────────────────────────

def classify_email(email: dict) -> dict:
    """
    Classify the intent of a customer email.

    Args:
        email: dict with keys: id, sender, subject, body, timestamp

    Returns:
        dict with: primary_intent, confidence_scores, urgency, sentiment, key_entities, mode
    """
    if DEMO_MODE:
        return _mock_classify(email)

    prompt = CLASSIFICATION_USER_PROMPT.format(
        subject=email.get("subject", ""),
        body=email.get("body", ""),
    )
    try:
        raw = _call_llm(CLASSIFICATION_SYSTEM_PROMPT, prompt, json_mode=True)
        result = json.loads(raw)
        result["mode"] = "live"
        return result
    except Exception as e:
        print(f"[Pipeline] Classification error: {e} — falling back to demo.")
        return _mock_classify(email)


def draft_reply(email: dict, classification: dict) -> dict:
    """
    Draft a reply for a classified email using RAG context.

    Args:
        email: dict with sender, subject, body
        classification: output from classify_email()

    Returns:
        dict with: draft_text, rag_context_used, action_summary, timestamp
    """
    intent = classification.get("primary_intent", "General Inquiry")
    urgency = classification.get("urgency", "medium")
    sentiment = classification.get("sentiment", "neutral")
    entities = classification.get("key_entities", [])

    # Retrieve RAG context
    query = f"{intent} {email.get('subject', '')} {email.get('body', '')[:300]}"
    rag_context = retrieve_context(query)

    if DEMO_MODE:
        draft_text = _mock_draft(email, classification)
        action_summary = _mock_action_summary(email, classification, draft_text)
    else:
        prompt = DRAFTING_USER_PROMPT.format(
            sender=email.get("sender", ""),
            subject=email.get("subject", ""),
            body=email.get("body", ""),
            intent=intent,
            urgency=urgency,
            sentiment=sentiment,
            entities=", ".join(entities) if entities else "None",
            rag_context=rag_context,
        )
        try:
            draft_text = _call_llm(DRAFTING_SYSTEM_PROMPT, prompt)
        except Exception as e:
            print(f"[Pipeline] Drafting error: {e} — falling back to demo.")
            draft_text = _mock_draft(email, classification)

        # Action summary
        try:
            summary_prompt = REVIEW_SUMMARY_PROMPT.format(
                intent=intent, body=email.get("body", ""), draft=draft_text
            )
            action_summary = _call_llm("You are a concise summarizer.", summary_prompt)
        except Exception:
            action_summary = _mock_action_summary(email, classification, draft_text)

    return {
        "draft_text": draft_text,
        "rag_context_used": rag_context,
        "action_summary": action_summary,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "mode": "demo" if DEMO_MODE else "live",
    }
