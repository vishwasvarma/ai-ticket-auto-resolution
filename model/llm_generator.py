import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key = os.getenv("GROQ_API_KEY")
)

def generate_response(ticket, solutions):
    solutions_text = "\n".join([f"- {s}" for s in solutions])

    prompt = f"""
You are an IT support assistant.
User issue:
{ticket}

Possible solutions:
{solutions_text}

Give a short and clear solution (2-3 sentences).
"""
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role":"user",
                    "content":prompt,
                }
            ],
            model = "llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content

    except Exception as e:
        print("GROQ ERROR:", e)
        return solutions[0]