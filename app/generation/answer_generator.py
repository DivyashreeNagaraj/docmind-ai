import ollama


class AnswerGenerator:
    """
    Generates answers using the retrieved document context.
    """

    def __init__(self, model="llama3.2"):
        self.model = model

    def generate_answer(self, question, retrieved_chunks):

        context = "\n\n".join(
    chunk["text"] for chunk in retrieved_chunks
)

        prompt = f"""
You are DocMind AI, an intelligent research assistant.

Answer the user's question ONLY using the provided context.

If the answer cannot be found in the context, say:

"I couldn't find enough information in the uploaded document to answer this question."

Do not make up facts.

Context:
{context}

Question:
{question}

Answer:
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]