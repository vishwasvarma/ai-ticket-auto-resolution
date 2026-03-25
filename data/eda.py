import pandas as pd

df = pd.read_csv(r"Q:\Projects\ai-ticket-auto-resolution\data\synthetic-it-call-center-tickets.csv")

print("Shape:", df.shape)
print("\nInfo:")
print(df.info())

print("\nMissing values:")
print(df.isnull().sum())

print("\nColumns:")
print(df.columns)

print("\nSample:")
print(df.head())



print("\nDropping irrelevant columns...")

drop_cols = [
    "Unnamed: 0",
    "number",
    "customer",
    "agent",
    "item_id"
]

df = df.drop(columns=drop_cols, errors="ignore")

print("Remaining columns:", df.columns)



print("\nHandling missing values...")

# Drop rows where category/subcategory missing
df = df.dropna(subset=["category", "subcategory"])

# Fill text columns
text_fill_cols = [
    "close_notes",
    "assignment_group"
]

for col in text_fill_cols:
    df[col] = df[col].fillna("unknown")

# Fill numeric columns
numeric_cols = [
    "info_score_close_notes",
    "info_score_poor_close_notes"
]

for col in numeric_cols:
    df[col] = df[col].fillna(df[col].median())




print("\nFixing datatypes...")

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["resolved_at"] = pd.to_datetime(df["resolved_at"], errors="coerce")

df["reassigned_count"] = pd.to_numeric(df["reassigned_count"], errors="coerce")
df["resolution_time"] = pd.to_numeric(df["resolution_time"], errors="coerce")



print("\nRemoving duplicates...")

before = df.shape[0]

df = df.drop_duplicates()

after = df.shape[0]

print("Duplicates removed:", before - after)


print("\nCleaning text columns...")

text_columns = [
    "short_description",
    "content",
    "close_notes",
    "category",
    "subcategory",
    "issue/request",
    "software/system"
]

for col in text_columns:
    df[col] = df[col].astype(str)
    df[col] = df[col].str.lower()
    df[col] = df[col].str.strip()




print("\nCreating ticket column...")

df["ticket"] = (
    df["short_description"] + " " +
    df["content"] + " " +
    df["issue/request"] + " " +
    df["software/system"]
)



print("\nCreating category_final...")

df["category_final"] = df["category"] + "_" + df["subcategory"]


print("\nRemoving rare categories...")

counts = df["category_final"].value_counts()

threshold = 10

valid_categories = counts[counts > threshold].index

df = df[df["category_final"].isin(valid_categories)]

print("Remaining categories:", df["category_final"].nunique())


print("\nCreating answer column...")

df["answer"] = df["close_notes"]



print("\nRemoving empty rows...")

df = df.dropna(subset=["ticket", "answer"])

df = df[
    (df["ticket"].str.len() > 15) &
    (df["answer"].str.len() > 15)
]



final_df = df[[
    "ticket",
    "category_final",
    "answer"
]]


rare_threshold = 50

rare_categories = final_df["category_final"].value_counts()
rare_categories = rare_categories[rare_categories < rare_threshold].index

final_df["category_final"] = final_df["category_final"].replace(
    rare_categories, "other_issue"
)

print("\nBalancing dataset...")

min_samples = 500


balanced_df = (
    final_df.groupby("category_final")
    .apply(lambda x: x.sample(min(len(x), min_samples), random_state=42))
    .reset_index(drop=True)
)

print("\nBalanced Dataset Shape:", balanced_df.shape)

print("\nBalanced Category Distribution:")
print(balanced_df["category_final"].value_counts())


print("\nFinal Dataset Shape:", final_df.shape)

print("\nCategory Distribution:")
print(final_df["category_final"].value_counts().head(20))



balanced_df.to_csv("data/final_it_tickets.csv", index=False)

print("\nFinal dataset saved:")
print("data/final_it_tickets.csv")



print("\nFinal Sample:")
print(balanced_df.head())