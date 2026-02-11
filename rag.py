import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_CHAT_MODEL
from embeddings import search_similar

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(GEMINI_CHAT_MODEL)


def build_prompt(context_chunks, question):
    context = "\n\n".join(context_chunks)

    return f"""
You are a senior cloud architect and Terraform expert.

Analyze the FULL infrastructure configuration below.

When answering:
- Identify all resources
- Explain how they connect
- Describe dependency flow
- Describe networking layout
- Mention compute components
- Mention outputs
- Suggest improvements if relevant

If the question asks for architecture summary,
structure your response exactly like this:

1. Overview
2. Resources Created
3. Networking Architecture
4. Dependency Flow
5. Recommendations

Terraform Configuration:
{context}

User Question:
{question}
"""


def ask_terraform_ai(question: str):
    try:
        question_lower = question.lower()

        # More context for architecture questions
        if "architecture" in question_lower or "overall" in question_lower:
            context_chunks = search_similar(question, n_results=6)
        else:
            context_chunks = search_similar(question, n_results=4)

        if not context_chunks:
            return "No Terraform code indexed yet. Please index a project first."

        prompt = build_prompt(context_chunks, question)

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.2,
                "max_output_tokens": 350
            }
        )

        return response.text

    except Exception as e:
        return f"Error in RAG pipeline: {str(e)}"
