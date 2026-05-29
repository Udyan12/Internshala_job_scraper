# AI Job Market Intelligence Dashboard

An end-to-end data science project that scrapes real job listings from Internshala, cleans the data, extracts skills, analyzes job trends, and presents insights through an interactive Streamlit dashboard.

## Features

- Real-time job scraping using Selenium
- Data cleaning using Pandas
- Skill extraction from job titles
- Interactive dashboard using Streamlit
- Location-wise job analysis
- Company-wise hiring analysis
- Job role analysis
- Skill demand analysis
- Skill recommendation system
- CSV download option
- Refresh job data button

## Tech Stack

- Python
- Selenium
- Pandas
- Plotly
- Streamlit
- Matplotlib
- WebDriver Manager

## Project Workflow

```text
Internshala Job Listings
        ↓
Selenium Web Scraper
        ↓
Raw CSV Data
        ↓
Data Cleaning
        ↓
Skill Extraction
        ↓
EDA & Visualization
        ↓
Streamlit Dashboard

pip install -r requirements.txt
python internshala_scraper.py
python internshala_analysis.py
streamlit run app.py

