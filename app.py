import streamlit as st
import pandas as pd
import plotly.express as px
import subprocess

st.set_page_config(
    page_title="Internshala Job Market Analyzer",
    page_icon="💼",
    layout="wide"
)
if st.button("🔄 Refresh Job Data"):
    with st.spinner("Scraping latest jobs from Internshala..."):
        subprocess.run(["python", "internshala_scraper.py"])
        subprocess.run(["python", "internshala_analysis.py"])
    st.success("Latest job data updated successfully!")
    
try:
    df = pd.read_csv("cleaned_internshala_jobs.csv")
except FileNotFoundError:
    st.error("cleaned_internshala_jobs.csv not found. Please run scraper first.")
    st.stop()

st.markdown("""
# 💼 Internshala Job Market Analyzer
Analyze real job listings scraped from Internshala with filters, charts, insights, and skill recommendations.
""")

st.sidebar.title("🔍 Filters")

search = st.sidebar.text_input("Search job title/company/skill")

selected_locations = st.sidebar.multiselect(
    "Select Location",
    sorted(df["location"].unique()),
    default=sorted(df["location"].unique())
)

selected_companies = st.sidebar.multiselect(
    "Select Company",
    sorted(df["company"].unique()),
    default=sorted(df["company"].unique())
)

filtered_df = df[
    (df["location"].isin(selected_locations)) &
    (df["company"].isin(selected_companies))
]

if search:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(search, case=False, na=False) |
        filtered_df["company"].str.contains(search, case=False, na=False) |
        filtered_df["location"].str.contains(search, case=False, na=False) |
        filtered_df["skills"].str.contains(search, case=False, na=False)
    ]

st.divider()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Jobs", len(filtered_df))
col2.metric("Companies", filtered_df["company"].nunique())
col3.metric("Locations", filtered_df["location"].nunique())
col4.metric("Skills Found", filtered_df["skills"].nunique())

st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "🧠 Skills",
    "🔎 Job Explorer",
    "🎯 Recommendation"
])

with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("🏙️ Top Locations")
        loc_data = filtered_df["location"].value_counts().head(10).reset_index()
        loc_data.columns = ["Location", "Jobs"]

        fig1 = px.bar(
            loc_data,
            x="Jobs",
            y="Location",
            orientation="h",
            title="Top Job Locations"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.subheader("🏢 Top Companies")
        comp_data = filtered_df["company"].value_counts().head(10).reset_index()
        comp_data.columns = ["Company", "Jobs"]

        fig2 = px.bar(
            comp_data,
            x="Jobs",
            y="Company",
            orientation="h",
            title="Top Hiring Companies"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("💼 Top Job Roles")
    role_data = filtered_df["title"].value_counts().head(15).reset_index()
    role_data.columns = ["Job Title", "Jobs"]

    fig3 = px.bar(
        role_data,
        x="Jobs",
        y="Job Title",
        orientation="h",
        title="Most Common Job Roles"
    )
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    st.subheader("🧠 Most Demanded Skills")

    skills_series = filtered_df["skills"].dropna().str.split(", ").explode()
    skills_series = skills_series[skills_series != "Not Mentioned"]

    if len(skills_series) > 0:
        skill_data = skills_series.value_counts().head(15).reset_index()
        skill_data.columns = ["Skill", "Jobs"]

        fig4 = px.bar(
            skill_data,
            x="Jobs",
            y="Skill",
            orientation="h",
            title="Top Skills in Job Listings"
        )
        st.plotly_chart(fig4, use_container_width=True)

        st.info(f"Most demanded skill: {skill_data.iloc[0]['Skill'].title()}")
    else:
        st.warning("No skills found in current filtered data.")

with tab3:
    st.subheader("🔎 Job Explorer")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=450
    )

    csv = filtered_df.to_csv(index=False)

    st.download_button(
        label="⬇️ Download Filtered Jobs CSV",
        data=csv,
        file_name="filtered_internshala_jobs.csv",
        mime="text/csv"
    )

with tab4:
    st.subheader("🎯 Skill Recommendation System")

    user_skills = st.text_input(
        "Enter your current skills",
        placeholder="Example: python, sql, excel"
    )

    if user_skills:
        user_skills_list = [
            skill.strip().lower()
            for skill in user_skills.split(",")
        ]

        all_required_skills = filtered_df["skills"].dropna().str.split(", ").explode()
        all_required_skills = all_required_skills[
            all_required_skills != "Not Mentioned"
        ].str.lower()

        top_required_skills = all_required_skills.value_counts().head(10).index.tolist()

        missing_skills = [
            skill for skill in top_required_skills
            if skill not in user_skills_list
        ]

        if missing_skills:
            st.warning("You should learn these skills:")
            for skill in missing_skills:
                st.write(f"✅ {skill.title()}")
        else:
            st.success("Great! Your skills match current job demand.")

st.divider()

if len(filtered_df) > 0:
    st.success("Dashboard updated successfully with real Internshala job data.")
else:
    st.error("No jobs found for selected filters.")