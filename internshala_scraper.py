import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://internshala.com/jobs/data-science-jobs/"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

response = requests.get(URL, headers=headers, timeout=20)

print("Status Code:", response.status_code)

if response.status_code != 200:
    print("Failed to fetch page. Old CSV preserved.")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

jobs = soup.select(".individual_internship")

print("Jobs found:", len(jobs))

job_data = []

for job in jobs:
    title = job.select_one(".job-title-href")
    company = job.select_one(".company-name")
    location = job.select_one(".locations")
    salary = job.select_one(".stipend")
    experience = job.select_one(".desktop-text")

    job_data.append({
        "title": title.get_text(strip=True) if title else "Not Available",
        "company": company.get_text(strip=True) if company else "Not Available",
        "location": location.get_text(strip=True) if location else "Not Available",
        "salary": salary.get_text(strip=True) if salary else "Not Available",
        "experience": experience.get_text(strip=True) if experience else "Not Available",
        "source": "Internshala"
    })

df = pd.DataFrame(job_data)

df = df[
    ~(
        (df["title"] == "Not Available") &
        (df["company"] == "Not Available") &
        (df["location"] == "Not Available")
    )
]

if len(df) < 5:
    print("Too few valid jobs scraped. Old CSV preserved.")
    exit()

df.drop_duplicates(inplace=True)

df.to_csv("internshala_jobs.csv", index=False)

print(df.head())
print("Total jobs scraped:", len(df))
print("Internshala scraping completed")