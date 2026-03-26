import pickle
from retrieval import retrieve_solution
from spellchecker import SpellChecker

# Load classifier
model = pickle.load(open("model/model.pkl", "rb"))

# Load vectorizer
vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))

# Spell checker
spell = SpellChecker()


# Format response properly
def format_response(text):

    if not text:
        return text

    sentences = text.split(". ")
    sentences = [s.strip().capitalize() for s in sentences]

    formatted = ". ".join(sentences)

    return formatted


# Spell correction
def correct_spelling(text):

    corrected = []

    for word in text.split():
        corrected_word = spell.correction(word)

        # Handle None from spellchecker
        if corrected_word is None:
            corrected_word = word

        corrected.append(corrected_word)

    return " ".join(corrected)


def solve_ticket(ticket_text):

    try:

        # Spell Correction
        ticket_text = correct_spelling(ticket_text)

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

        best_solution = solutions[0]
        best_score = scores[0]

        # Short query check
        if len(ticket_text.split()) < 3:
            return {
                "category": "Unknown",
                "confidence": 0.0,
                "response": "Please provide more details about the issue."
            }

        # Manual review threshold
        if best_score < 0.45:
            return {
                "category": "Unknown",
                "Confidence Score": round(best_score * 100, 2),
                "response": "This issue requires manual review."
            }

        # Format response
        formatted_response = format_response(best_solution)

        return {
            "category": str(category).replace("_", " ").title(),
            "Confidence Score": round(best_score * 100, 2),
            "response": formatted_response
        }

    except Exception as e:

        return {
            "error": str(e)
        }