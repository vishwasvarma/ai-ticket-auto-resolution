import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier

## Loading dataset
df = pd.read_csv(r"Q:\Projects\ai-ticket-auto-resolution\data\final_it_tickets.csv")

X = df["ticket"]
y = df["category_final"]

## Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

## TF-IDF Vectorization
vectorizer = TfidfVectorizer(
    max_features=15000,
    ngram_range=(1,2),
    stop_words="english",
    min_df=2,
    max_df=0.95
)

X_train = vectorizer.fit_transform(X_train)

## Hyperparameter tuning

param_grid = {
    "alpha": [1e-4, 1e-5, 1e-6],
    "loss": ["hinge", "log_loss"],
    "penalty": ["l2", "elasticnet"]
}

grid = GridSearchCV(
    SGDClassifier(max_iter=1000),
    param_grid,
    cv=3,
    n_jobs=-1
)

grid.fit(X_train, y_train)

print("Best params:", grid.best_params_)