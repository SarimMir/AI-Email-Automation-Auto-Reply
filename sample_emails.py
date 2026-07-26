"""
StyleSync AI Mail — 20 Sample Customer Emails
==============================================
Covers 8 intent categories across realistic e-commerce clothing scenarios.
"""

SAMPLE_EMAILS = [
    # ─── ORDER STATUS (3) ───────────────────────────────────────────────────
    {
        "id": "EM001",
        "sender": "aisha.khan@gmail.com",
        "subject": "Where is my order #SS-78234?",
        "body": (
            "Hi StyleSync team,\n\n"
            "I placed order #SS-78234 on July 20th and it's been 6 days "
            "now. I selected standard shipping but I still haven't received "
            "any tracking information. Can you please update me on the status? "
            "I needed this outfit for an event this weekend.\n\n"
            "Thanks,\nAisha"
        ),
        "intent": "Order Status",
        "timestamp": "2026-07-26T09:15:00Z"
    },
    {
        "id": "EM002",
        "sender": "m.tariq92@hotmail.com",
        "subject": "Order confirmation but no shipping update",
        "body": (
            "Hello,\n\n"
            "I received an order confirmation email for order #SS-79001 two "
            "days ago but I have not received any dispatch notification yet. "
            "Is my order being processed? The website says 1-2 business days "
            "for processing.\n\nRegards,\nMuhammad Tariq"
        ),
        "intent": "Order Status",
        "timestamp": "2026-07-25T14:22:00Z"
    },
    {
        "id": "EM003",
        "sender": "sara.ali.lahore@gmail.com",
        "subject": "Tracking number not working",
        "body": (
            "Dear Support,\n\n"
            "I received a shipping notification for order #SS-77890 with a "
            "tracking number TRK-445892. However, when I enter it on the courier "
            "website, it says 'tracking not found'. This has been happening for "
            "2 days. Is there an issue with my shipment?\n\nBest,\nSara Ali"
        ),
        "intent": "Order Status",
        "timestamp": "2026-07-24T11:05:00Z"
    },

    # ─── RETURN / EXCHANGE (3) ──────────────────────────────────────────────
    {
        "id": "EM004",
        "sender": "bilal.ahmed.khi@yahoo.com",
        "subject": "I want to return my dress",
        "body": (
            "Hi,\n\n"
            "I received the floral summer dress (order #SS-77112) yesterday "
            "but the color looks completely different in person than on the "
            "website — it's much darker and dull. I'd like to return it and "
            "get a refund. How do I proceed?\n\nThanks,\nBilal"
        ),
        "intent": "Return/Exchange",
        "timestamp": "2026-07-26T08:40:00Z"
    },
    {
        "id": "EM005",
        "sender": "nadia.ch@gmail.com",
        "subject": "Exchange request — wrong size delivered",
        "body": (
            "Hello StyleSync,\n\n"
            "I ordered a Medium in the Linen Co-ord set (order #SS-78560) "
            "but I received a Small. I would like to exchange it for the "
            "correct size. Please let me know the process and if Medium is "
            "currently in stock.\n\nRegards,\nNadia Chaudhry"
        ),
        "intent": "Return/Exchange",
        "timestamp": "2026-07-25T17:10:00Z"
    },
    {
        "id": "EM006",
        "sender": "usman.raza.isb@gmail.com",
        "subject": "Return policy question + refund timeline",
        "body": (
            "Hi,\n\n"
            "I bought a jacket 3 weeks ago (order #SS-76001) and it has a "
            "stitching defect near the collar that I only noticed after wearing "
            "it once. Am I still eligible for a return or exchange? Also, if "
            "a refund is approved, how long does it take to reflect in my "
            "account?\n\nThanks,\nUsman"
        ),
        "intent": "Return/Exchange",
        "timestamp": "2026-07-23T10:30:00Z"
    },

    # ─── SIZING HELP (2) ────────────────────────────────────────────────────
    {
        "id": "EM007",
        "sender": "hina.malik99@gmail.com",
        "subject": "What size should I order? (measurements included)",
        "body": (
            "Hi team,\n\n"
            "I want to buy the Vintage Denim Jacket. My measurements are: "
            "Bust 37\", Waist 29\", Hips 39\". I usually wear Medium but I've "
            "heard your denim runs small. Should I go with Medium or Large? "
            "I prefer a slightly relaxed fit.\n\nThanks,\nHina"
        ),
        "intent": "Sizing Help",
        "timestamp": "2026-07-26T12:00:00Z"
    },
    {
        "id": "EM008",
        "sender": "faisal.m.karachi@gmail.com",
        "subject": "Men's size chart confusion",
        "body": (
            "Hello,\n\n"
            "I'm confused between Large and XL for the Cargo Pants. "
            "My waist is 33\" and I have athletic/muscular legs. The size "
            "chart says L is for 34\" waist but I'm wondering if the "
            "leg opening would be comfortable. Do these run slim or relaxed?\n\n"
            "Faisal"
        ),
        "intent": "Sizing Help",
        "timestamp": "2026-07-24T15:45:00Z"
    },

    # ─── COMPLAINT (3) ──────────────────────────────────────────────────────
    {
        "id": "EM009",
        "sender": "zara.bashir@outlook.com",
        "subject": "Very disappointed — shirt fell apart after first wash",
        "body": (
            "I am extremely disappointed with the quality of the white shirt "
            "I ordered (order #SS-75230). After just ONE wash on a gentle cycle, "
            "the stitching on the shoulder has completely come apart. I paid "
            "Rs. 2,800 for this and expected much better quality from your brand. "
            "This is unacceptable. I want a full refund or replacement ASAP.\n\n"
            "Very frustrated,\nZara Bashir"
        ),
        "intent": "Complaint",
        "timestamp": "2026-07-26T07:20:00Z"
    },
    {
        "id": "EM010",
        "sender": "kamran.javed.pesh@gmail.com",
        "subject": "Wrong item in my package",
        "body": (
            "Hi,\n\n"
            "I opened my package today (order #SS-78990) and found a completely "
            "wrong item inside — I ordered a Navy Blue Polo shirt in size L but "
            "received a women's pink cardigan. This is a very basic error. "
            "I'm traveling next week and need my correct item urgently. "
            "Please fix this immediately.\n\nKamran Javed"
        ),
        "intent": "Complaint",
        "timestamp": "2026-07-25T13:00:00Z"
    },
    {
        "id": "EM011",
        "sender": "rehana.fatima2@gmail.com",
        "subject": "Customer service is very slow — still no response",
        "body": (
            "This is my third email regarding order #SS-77400. I first contacted "
            "you 5 days ago about a missing item in my order. I was told I'd "
            "receive a response in 24 hours but have heard nothing. I've sent "
            "follow-up emails and got no reply. This level of service is "
            "extremely unprofessional. I want this resolved today or I will "
            "dispute the charge with my bank.\n\nRehana Fatima"
        ),
        "intent": "Complaint",
        "timestamp": "2026-07-26T10:55:00Z"
    },

    # ─── COMPLIMENT (2) ─────────────────────────────────────────────────────
    {
        "id": "EM012",
        "sender": "ayesha.siddiqui.fbr@gmail.com",
        "subject": "Amazing quality! Will definitely order again",
        "body": (
            "Hi StyleSync team!\n\n"
            "I just wanted to say how impressed I am with my recent order "
            "(#SS-78100). The Summer Linen Co-ord set is absolutely gorgeous "
            "— the fabric quality is exceptional and the stitching is "
            "impeccable. I've received so many compliments already! "
            "Your packaging was also beautiful — felt like a luxury brand. "
            "Keep up the great work. You've gained a loyal customer!\n\n"
            "Warmly,\nAyesha Siddiqui"
        ),
        "intent": "Compliment",
        "timestamp": "2026-07-25T09:30:00Z"
    },
    {
        "id": "EM013",
        "sender": "omar.h.dubai@gmail.com",
        "subject": "Love the new collection!",
        "body": (
            "Hey StyleSync,\n\n"
            "Just browsed through your new Autumn '26 collection and I'm "
            "absolutely in love with the earth tones. Ordered 3 pieces already! "
            "Your designs are always on point and the prices are very fair "
            "for the quality. The free delivery was a great bonus too. "
            "Excited to receive my order!\n\nOmar"
        ),
        "intent": "Compliment",
        "timestamp": "2026-07-24T19:00:00Z"
    },

    # ─── SHIPPING DELAY (2) ─────────────────────────────────────────────────
    {
        "id": "EM014",
        "sender": "sana.mir.rwp@gmail.com",
        "subject": "Order is 4 days late — where is it?",
        "body": (
            "Hello,\n\n"
            "I placed order #SS-77650 on July 16th and selected express "
            "shipping (1-2 business days). Today is July 26th — my order "
            "is now 8 days late. The tracking still shows 'In Transit' since "
            "July 18th. I needed this dress for a wedding that already passed! "
            "What is going on? Will you compensate for this delay?\n\nSana Mir"
        ),
        "intent": "Shipping Delay",
        "timestamp": "2026-07-26T11:30:00Z"
    },
    {
        "id": "EM015",
        "sender": "adeel.ch.lhr@gmail.com",
        "subject": "Shipment stuck at Lahore hub for 3 days",
        "body": (
            "Hi,\n\n"
            "My order #SS-78300 has been stuck at the Lahore sorting hub since "
            "July 23rd according to the tracking. It hasn't moved at all. Is "
            "there an issue with the courier? What can you do to expedite this? "
            "I'm in Rawalpindi and it usually takes 1 day from Lahore.\n\n"
            "Adeel Chaudhry"
        ),
        "intent": "Shipping Delay",
        "timestamp": "2026-07-26T13:45:00Z"
    },

    # ─── PAYMENT ISSUE (2) ──────────────────────────────────────────────────
    {
        "id": "EM016",
        "sender": "hassan.ali.acc@gmail.com",
        "subject": "I was charged twice for the same order",
        "body": (
            "Hi StyleSync,\n\n"
            "I placed order #SS-79120 this morning and my bank statement shows "
            "two charges of Rs. 4,500 each from StyleSync — so I've been billed "
            "Rs. 9,000 instead of Rs. 4,500. I only placed one order. "
            "Please refund the extra charge immediately. I am attaching my "
            "bank statement screenshot.\n\nHassan Ali"
        ),
        "intent": "Payment Issue",
        "timestamp": "2026-07-26T10:10:00Z"
    },
    {
        "id": "EM017",
        "sender": "rabia.iqbal.acc@gmail.com",
        "subject": "Payment failed but amount deducted from account",
        "body": (
            "Hello,\n\n"
            "I tried to place an order today and the website showed a payment "
            "failure message. But my bank has already deducted the amount "
            "(Rs. 3,200). I don't have an order confirmation and no order appears "
            "in my account. Did my order go through? If not, when will the "
            "amount be reversed?\n\nRabia Iqbal"
        ),
        "intent": "Payment Issue",
        "timestamp": "2026-07-26T16:20:00Z"
    },

    # ─── GENERAL INQUIRY (3) ────────────────────────────────────────────────
    {
        "id": "EM018",
        "sender": "mehwish.t@gmail.com",
        "subject": "Do you offer gift wrapping?",
        "body": (
            "Hi,\n\n"
            "I'm buying a birthday gift for my friend and was wondering if "
            "StyleSync offers gift wrapping or a gift message service. "
            "Also, do you have gift cards? I couldn't find this option "
            "during checkout.\n\nThanks,\nMehwish"
        ),
        "intent": "General Inquiry",
        "timestamp": "2026-07-25T15:00:00Z"
    },
    {
        "id": "EM019",
        "sender": "junaid.q.sales@gmail.com",
        "subject": "Bulk/wholesale order inquiry",
        "body": (
            "Dear StyleSync,\n\n"
            "I run a boutique in Islamabad and I'm interested in stocking "
            "some of your pieces. Do you offer wholesale pricing for bulk "
            "orders (50+ units)? If so, could you please share your wholesale "
            "catalogue and terms?\n\nJunaid Qureshi\nOwner, Junaid's Boutique"
        ),
        "intent": "General Inquiry",
        "timestamp": "2026-07-24T10:00:00Z"
    },
    {
        "id": "EM020",
        "sender": "amna.baig.stud@gmail.com",
        "subject": "Is the Black Blazer restocking soon?",
        "body": (
            "Hi,\n\n"
            "I've been waiting for the Classic Black Blazer in size S to come "
            "back in stock for almost a month. It keeps saying 'Out of Stock' "
            "on the website. Is there any expected restock date? Can I sign up "
            "for a notification when it's back?\n\nAmna Baig"
        ),
        "intent": "General Inquiry",
        "timestamp": "2026-07-23T18:30:00Z"
    },
]

# Intent color mapping for UI
INTENT_COLORS = {
    "Order Status":    "#6366f1",   # indigo
    "Return/Exchange": "#f59e0b",   # amber
    "Sizing Help":     "#10b981",   # emerald
    "Complaint":       "#ef4444",   # red
    "Compliment":      "#22d3ee",   # cyan
    "Shipping Delay":  "#f97316",   # orange
    "Payment Issue":   "#ec4899",   # pink
    "General Inquiry": "#8b5cf6",   # violet
}

INTENT_ICONS = {
    "Order Status":    "📦",
    "Return/Exchange": "🔄",
    "Sizing Help":     "📏",
    "Complaint":       "⚠️",
    "Compliment":      "⭐",
    "Shipping Delay":  "🚚",
    "Payment Issue":   "💳",
    "General Inquiry": "💬",
}
