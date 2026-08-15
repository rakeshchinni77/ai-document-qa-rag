class PromptService:
    @staticmethod
    def build_prompt(user_question: str, retrieved_chunks: list[str]) -> str:
        formatted_context = ""
        for idx, chunk in enumerate(retrieved_chunks, 1):
            formatted_context += f"--- Context Chunk {idx} ---\n{chunk}\n\n"

        prompt = f"""You are an expert AI assistant answering user questions strictly based on the provided document context.

Context Information:
---------------------
{formatted_context.strip()}
---------------------

Given the context information above and no prior knowledge, answer the following user question.
Strict Rules:
1. Rely ONLY on the provided context information. Under no circumstances should you use outside knowledge or hallucinate.
2. If the answer cannot be found or logically inferred from the context, explicitly state "I cannot find the answer in the provided documents."

Question: {user_question}
Answer:"""
        return prompt
