import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score, classification_report

print("Loading cleaned dataset...")

df = pd.read_csv(r"Q:\Projects\ai-ticket-auto-resolution\data\final_it_tickets.csv")

print("Dataset shape:", df.shape)


# Features & Labels
X = df["ticket"]
y = df["category_final"]

# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Train size:", len(X_train))
print("Test size:", len(X_test))


# Vectorization
print("Vectorizing...")


vectorizer = TfidfVectorizer(
    max_features=15000,
    ngram_range=(1,2),
    stop_words="english",
    min_df=2,
    max_df=0.95
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)


print("Training model...")

model = SGDClassifier(
    alpha=1e-5,
    loss="log_loss",
    penalty="elasticnet",
    max_iter=3000,
    n_jobs=-1,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train_vec, y_train)


print("Evaluating...")

y_pred = model.predict(X_test_vec)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))


print("Saving model...")

pickle.dump(model, open("model/model.pkl", "wb"))
pickle.dump(vectorizer, open("model/vectorizer.pkl", "wb"))

print("Model saved successfully!")