import pickle
from model.retrieval import retrieve_solution
from spellchecker import SpellChecker
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

# Load classifier
model = pickle.load(open("model/model.pkl", "rb"))

# Load vectorizer
vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))

# Spell checker
spell = SpellChecker()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Spell correction
def correct_spelling(text):
    corrected = []
    for word in text.split():
        corrected_word = spell.correction(word)
        if corrected_word is None:
            corrected_word = word
        corrected.append(corrected_word)
    return " ".join(corrected)

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
Keep the response concise and professional."""

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


def solve_ticket(ticket_text):
    try:
        # Spell Correction
        ticket_text = correct_spelling(ticket_text)

        # Short query check
        if len(ticket_text.split()) < 3:
            return {
                "category": "Unknown",
                "confidence": 0.0,
                "response": "Please provide more details about the issue."
            }

        # Classification
        ticket_vec = vectorizer.transform([ticket_text])
        category = model.predict(ticket_vec)[0]

        # Retrieval
        solutions, scores = retrieve_solution(ticket_text)

        # No solution found
        if not solutions or len(scores) == 0:
            return {
                "category": "Unknown",
                "confidence": 0.0,
                "response": "No solution found. Please contact support."
            }

        best_score = scores[0]

        # Manual review threshold
        if best_score < 0.45:
            return {
                "category": "Unknown",
                "Confidence Score": round(best_score * 100, 2),
                "response": "This issue requires manual review."
            }

        top_solutions = solutions[:3]
        category_label = str(category).replace("_", " ").title()

        # Generate response using Groq LLM
        generated_response = generate_with_groq(ticket_text, category_label, top_solutions)

        return {
            "category": category_label,
            "Confidence Score": round(best_score * 100, 2),
            "response": generated_response
        }

    except Exception as e:
        return {
            "error": str(e)
        }