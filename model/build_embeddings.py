import pandas as pd
import pickle
from sentence_transformers import SentenceTransformer

# Loading dataset
df = pd.read_csv("data/final_it_tickets.csv")

tickets = df["ticket"].tolist()
answers = df["answer"].tolist()
categories = df["category_final"].tolist()

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Encoding tickets...")

embeddings = model.encode(
    tickets,
    convert_to_tensor=True,
    show_progress_bar=True
)

# Save everything
data = {
    "tickets": tickets,
    "answers": answers,
    "categories": categories,
    "embeddings": embeddings
}

with open("model/embeddings.pkl", "wb") as f:
    pickle.dump(data, f)

print("Embeddings saved successfully!")