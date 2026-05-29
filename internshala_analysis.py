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
    "data science", "analytics", "ai", "java",
    "javascript", "react", "cloud", "aws"
]


def extract_skills(text):
    text = str(text).lower()
    found = []

    for skill in skill_keywords:
        if skill in text:
            found.append(skill)

    return ", ".join(found) if found else "Not Mentioned"


def detect_job_type(text):
    text = str(text).lower()

    if "remote" in text or "work from home" in text:
        return "Remote"
    elif "hybrid" in text:
        return "Hybrid"
    else:
        return "Onsite"


def detect_experience_level(text):
    text = str(text).lower()

    if "intern" in text or "internship" in text:
        return "Internship"
    elif "fresher" in text or "0 year" in text or "0-1" in text:
        return "Fresher"
    elif "1" in text or "2" in text:
        return "Junior"
    elif "3" in text or "4" in text or "5" in text:
        return "Mid-Level"
    elif "senior" in text or "lead" in text or "manager" in text:
        return "Senior"
    else:
        return "Not Mentioned"


def detect_domain(text):
    text = str(text).lower()

    if "data scientist" in text or "data science" in text:
        return "Data Science"
    elif "data analyst" in text or "business analyst" in text:
        return "Data Analyst"
    elif "machine learning" in text or "ml" in text:
        return "ML Engineer"
    elif "ai" in text or "artificial intelligence" in text:
        return "AI Engineer"
    elif "python" in text or "developer" in text:
        return "Software Development"
    elif "analytics" in text:
        return "Analytics"
    else:
        return "Other"


df["combined_text"] = (
    df["title"].astype(str) + " " +
    df["location"].astype(str) + " " +
    df["experience"].astype(str)
)

df["skills"] = df["combined_text"].apply(extract_skills)
df["job_type"] = df["combined_text"].apply(detect_job_type)
df["experience_level"] = df["combined_text"].apply(detect_experience_level)
df["domain"] = df["combined_text"].apply(detect_domain)

df.drop(columns=["combined_text"], inplace=True)

df.to_csv("cleaned_internshala_jobs.csv", index=False)

print("\nCleaned enriched file created: cleaned_internshala_jobs.csv")
print("\nColumns:")
print(df.columns)

print("\nDomain Counts:")
print(df["domain"].value_counts())

print("\nExperience Level Counts:")
print(df["experience_level"].value_counts())

print("\nJob Type Counts:")
print(df["job_type"].value_counts())

df["location"].value_counts().head(10).plot(kind="bar")
plt.title("Top Internshala Job Locations")
plt.xlabel("Location")
plt.ylabel("Number of Jobs")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("internshala_top_locations.png")
plt.show()