import ollama


class AnswerGenerator:
    """
    Generates answers using the retrieved document context.
    """

    def __init__(self, model="llama3.2"):
        self.model = model

    def generate(self, question, context):

        prompt = f"""
You are an AI research assistant.

Use ONLY the provided context to answer the question.

If the answer is partially available, answer with the available information.

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