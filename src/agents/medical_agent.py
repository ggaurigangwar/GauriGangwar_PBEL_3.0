class MedicalAgent:

    def __init__(self, retriever, rag_chain):
        self.retriever = retriever
        self.rag_chain = rag_chain

    def answer(self, question):

        try:
            docs = self.retriever.invoke(question)

            if not docs:
                return None

            result = self.rag_chain.invoke(
                {
                    "input": question
                }
            )

            return result["answer"]

        except Exception as e:
            print(f"[MedicalAgent Error] {e}")
            return None