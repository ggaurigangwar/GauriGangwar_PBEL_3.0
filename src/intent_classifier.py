import re

GREETINGS = {
    "hi", "hello", "hey", "hii", "hlo",
    "good morning", "good afternoon", "good evening"
}

CASUAL = {
    "how are you",
    "who are you",
    "what are you",
    "what can you do",
    "thanks",
    "thank you",
    "bye",
    "goodbye",
    "nice to meet you"
}

MEDICAL_KEYWORDS = {
    "pain","fever","headache","diabetes","cancer","medicine",
    "tablet","dose","infection","blood","pressure","heart",
    "covid","pregnancy","symptom","disease","treatment",
    "doctor","hospital","surgery","vomiting","cough",
    "cold","flu","acne","skin","allergy","infection",
    "asthma","thyroid","kidney","liver","cholesterol"
}


def classify_intent(question: str):

    q = question.lower().strip()

    if q in GREETINGS:
        return "greeting"

    if q in CASUAL:
        return "casual"

    for word in MEDICAL_KEYWORDS:
        if re.search(rf"\b{re.escape(word)}\b", q):
            return "medical"

    return "general"