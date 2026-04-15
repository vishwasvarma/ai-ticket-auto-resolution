import pickle
from model.retrieval import retrieve_solution
from groq import Groq
import os
from dotenv import load_dotenv
from model.spell_checker import correct_spelling
from model.classifier import classify_ticket, is_query_too_short

load_dotenv()

# Load classifier
model = pickle.load(open("model/model.pkl", "rb"))

# Load vectorizer
vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))

# Spell checker

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_with_groq(ticket_text, category, retrieved_solutions):
    solutions_text = "\n\n".join(
        [f"Past Resolution {i+1}:\n{sol}" for i, sol in enumerate(retrieved_solutions)]
    )

    prompt = f"""You are a helpful IT support agent. A user submitted this support ticket:

Ticket: {ticket_text}
Category: {category}

Here are similar past resolutions for reference:
{solutions_text}

Write a clear, friendly, step-by-step support response directly addressing the user's issue.
Use simple language. Format as numbered steps where applicable.
Do not copy the past solutions verbatim — use them as context only.
Keep the response concise and professional

Guidelines:
- Use simple and direct language
- Do NOT include greetings like "Dear User"
- Do NOT include signatures like "Best regards" or "IT Support Agent"
- Keep it concise and practical
- Focus only on solving the issue."""

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful IT support agent."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.3-70b-versatile",  
        temperature=0.4,
        max_tokens=512,
    )

    return chat_completion.choices[0].message.content.strip()


def solve_ticket(ticket_text: str) -> dict:
    try:
        # Step 1 — Spell correction (symspellpy, Fix 1)
        corrected_text = correct_spelling(ticket_text)

        # Step 2 — Short query guard + keyword pre-classifier + ML fallback (Fix 2 & 3)
        result = classify_ticket(corrected_text, model, vectorizer)

        # Short query or manual review from classifier
        if result["band"] == "manual_review":
            return {
                "category":   result["category"],
                "confidence": result["confidence"],
                "band":       result["band"],
                "source":     result.get("source", "unknown"),
                "response":   result.get("message", "This issue requires manual review by a support agent."),
            }

        category = str(result["category"]).replace("_", " ").title()

        # Step 3 — Semantic retrieval
        solutions, scores = retrieve_solution(corrected_text)

        if not solutions or not scores:
            return {
                "category":   category,
                "confidence": result["confidence"],
                "response":   "No similar resolutions found. Please contact support directly.",
            }

        # Step 4 — LLM response generation
        generated_response = generate_with_groq(corrected_text, category, solutions[:3])

        return {
            "user_view": {
            "category": category,
            "response": generated_response,
            },
            "internal": {
            "confidence": result["confidence"],
            "band": result["band"],
            "source": result["source"],
            }
        }

    except Exception as e:
        return {"error": str(e)}