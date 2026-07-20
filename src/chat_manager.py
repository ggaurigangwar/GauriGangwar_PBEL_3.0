from src.intent_classifier import classify_intent
from src.memory import ConversationMemory
from src.agents.conversation_agent import ConversationAgent
from src.agents.medical_agent import MedicalAgent


class ChatManager:

    def __init__(self, retriever, rag_chain, llm):
        self.retriever = retriever
        self.rag_chain = rag_chain
        self.llm = llm

        self.memory = ConversationMemory()
        self.conversation = ConversationAgent()
        self.medical = MedicalAgent(
            retriever,
            rag_chain
        )

    def handle_query(self, question):
        self.memory.add_user_message(question)

        intent = classify_intent(question)

        if intent == "greeting":
            return self._handle_greeting()

        if intent == "casual":
            return self._handle_casual(question)

        return self._handle_medical(question)

    def _handle_greeting(self):
        response = self.conversation.greeting()
        self.memory.add_ai_message(response)
        return response

    def _handle_casual(self, question):
        response = self.llm.invoke(question).content
        self.memory.add_ai_message(response)
        return response

    def _handle_medical(self, question):
        answer = self.medical.answer(question)

        if answer:
            self.memory.add_ai_message(answer)
            return answer

        response = self.llm.invoke(question).content
        self.memory.add_ai_message(response)
        return response