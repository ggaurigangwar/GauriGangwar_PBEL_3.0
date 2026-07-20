EMERGENCY_KEYWORDS = [
    "chest pain",
    "heart attack",
    "difficulty breathing",
    "unconscious",
    "stroke",
    "severe bleeding",
    "suicide",
    "poison",
    "overdose",
    "seizure"
]


class EmergencyAgent:

    def is_emergency(self, question):

        q = question.lower()

        return any(word in q for word in EMERGENCY_KEYWORDS)

    def emergency_response(self):

        return """
⚠️ Your symptoms may indicate a medical emergency.

Please seek immediate medical attention or contact your local emergency services.

I can continue providing general health information, but emergency care should be your priority.
"""