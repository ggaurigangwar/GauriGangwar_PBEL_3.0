class ConversationMemory:

    def __init__(self):
        self.history = []

    def add_user_message(self, message):
        self.history.append({
            "role": "user",
            "content": message
        })

    def add_ai_message(self, message):
        self.history.append({
            "role": "assistant",
            "content": message
        })

    def get_history(self):
        return self.history

    def get_recent_history(self, limit=6):
        return self.history[-limit:]

    def clear(self):
        self.history.clear()