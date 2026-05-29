from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

url = "https://internshala.com/jobs/data-science-jobs/"
driver.get(url)

time.sleep(5)

# Close signup / popup if it appears
popup_xpaths = [
    "//button[contains(text(),'Skip')]",
    "//button[contains(text(),'No thanks')]",
    "//button[contains(text(),'Maybe later')]",
    "//button[contains(text(),'Later')]",
    "//span[contains(text(),'×')]",
    "//span[contains(text(),'✕')]",
    "//button[contains(@class,'close')]",
    "//div[contains(@class,'close')]",
    "//i[contains(@class,'close')]"
]

for xpath in popup_xpaths:
    try:
        popup = driver.find_element(By.XPATH, xpath)
        popup.click()
        time.sleep(2)
        break
    except:
        pass

# Scroll page to load jobs
for i in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

jobs = driver.find_elements(By.CLASS_NAME, "individual_internship")

job_data = []

for job in jobs:
    try:
        title = job.find_element(By.CLASS_NAME, "job-title-href").text.strip()
    except:
        title = "Not Available"

    try:
        company = job.find_element(By.CLASS_NAME, "company-name").text.strip()
    except:
        company = "Not Available"

    try:
        location = job.find_element(By.CLASS_NAME, "locations").text.strip()
    except:
        location = "Not Available"

    try:
        salary = job.find_element(By.CLASS_NAME, "stipend").text.strip()
    except:
        salary = "Not Available"

    try:
        experience = job.find_element(By.CLASS_NAME, "desktop-text").text.strip()
    except:
        experience = "Not Available"

    job_data.append({
        "title": title,
        "company": company,
        "location": location,
        "salary": salary,
        "experience": experience,
        "source": "Internshala"
    })

df = pd.DataFrame(job_data)

df.drop_duplicates(inplace=True)

df.to_csv("internshala_jobs.csv", index=False)

print(df)
print("Total jobs scraped:", len(df))
print("Internshala scraping completed")

driver.quit()