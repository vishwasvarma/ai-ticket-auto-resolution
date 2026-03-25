import pickle
from retrieval import retrieve_solution


# Load classifier
model = pickle.load(open("model/model.pkl", "rb"))

# Load vectorizer
vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))


# Format response properly
def format_response(text):

    if not text:
        return text

    # Split sentences
    sentences = text.split(". ")

    # Capitalize each sentence
    sentences = [s.strip().capitalize() for s in sentences]

    # Join back
    formatted = ". ".join(sentences)

    return formatted


def solve_ticket(ticket_text):

    try:

        # Classification
        ticket_vec = vectorizer.transform([ticket_text])
        category = model.predict(ticket_vec)[0]

        # Confidence (fallback safe)
        try:
            classifier_confidence = model.predict_proba(ticket_vec).max()
        except:
            classifier_confidence = 0.8


        # Retrieval
        solutions, scores = retrieve_solution(ticket_text)

        # No solution found
        if not solutions:
            return {
                "category": str(category).replace("_", " ").title(),
                "confidence": float(classifier_confidence),
                "response": "No solution found. Please contact support."
            }


        best_solution = solutions[0]
        best_score = scores[0]


        # Low confidence fallback
        if best_score < 0.40:
            return {
                "category": str(category).replace("_", " ").title(),
                "response": "This issue requires manual review."
            }


        # Format response properly
        formatted_response = format_response(best_solution)


        return {
            "category": str(category).replace("_", " ").title(),
            "response": formatted_response
        }


    except Exception as e:

        return {
            "error": str(e)
        }