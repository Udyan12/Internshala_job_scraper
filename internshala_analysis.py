import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("internshala_jobs.csv")

print("First 5 rows:")
print(df.head())

print("\nTotal jobs:", len(df))
print("\nMissing values:")
print(df.isnull().sum())

df.drop_duplicates(inplace=True)
df.fillna("Not Available", inplace=True)

df["title"] = df["title"].str.strip()
df["company"] = df["company"].str.strip()
df["location"] = df["location"].str.strip()
df["salary"] = df["salary"].str.strip()
df["experience"] = df["experience"].str.strip()

skill_keywords = [
    "python", "sql", "excel", "power bi", "tableau",
    "machine learning", "deep learning", "data analysis",
    "pandas", "numpy", "tensorflow", "pytorch",
    "nlp", "statistics", "django", "flask",
    "data science", "analytics", "ai"
]

def extract_skills(text):
    text = str(text).lower()
    found = []

    for skill in skill_keywords:
        if skill in text:
            found.append(skill)

    return ", ".join(found) if found else "Not Mentioned"

df["skills"] = df["title"].apply(extract_skills)

df.to_csv("cleaned_internshala_jobs.csv", index=False)

print("\nCleaned file created: cleaned_internshala_jobs.csv")

print("\nTop Locations:")
print(df["location"].value_counts().head(10))

df["location"].value_counts().head(10).plot(kind="bar")
plt.title("Top Internshala Job Locations")
plt.xlabel("Location")
plt.ylabel("Number of Jobs")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("internshala_top_locations.png")
plt.show()