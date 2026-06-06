import streamlit as st
import pandas as pd
import plotly.express as px
import subprocess

st.set_page_config(
    page_title="AI Job Market Intelligence Platform",
    page_icon="💼",
    layout="wide"
)

# ---------- STITCH DESIGN SYSTEM THEME ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #0b1326;
    --surface-low: #131b2e;
    --surface: #171f33;
    --surface-high: #222a3d;
    --surface-highest: #2d3449;
    --text: #dae2fd;
    --muted: #bac9cc;
    --cyan: #00e5ff;
    --cyan-soft: #c3f5ff;
    --blue: #0068ed;
    --purple: #7c4dff;
    --border: #3b494c;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(0, 229, 255, 0.18), transparent 32%),
        radial-gradient(circle at top right, rgba(124, 77, 255, 0.16), transparent 30%),
        linear-gradient(180deg, #0b1326 0%, #060e20 100%);
    color: var(--text);
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060e20 0%, #131b2e 100%);
    border-right: 1px solid rgba(0, 229, 255, 0.18);
}

.hero-card {
    padding: 28px 30px;
    border-radius: 18px;
    background:
        linear-gradient(135deg, rgba(0, 229, 255, 0.20), rgba(124, 77, 255, 0.14)),
        rgba(23, 31, 51, 0.90);
    border: 1px solid rgba(0, 229, 255, 0.35);
    box-shadow: 0 0 35px rgba(0, 229, 255, 0.13);
    margin-bottom: 22px;
}

.hero-title {
    font-size: 42px;
    line-height: 1.08;
    font-weight: 800;
    color: var(--text);
    margin-bottom: 8px;
    letter-spacing: -0.03em;
}

.hero-subtitle {
    color: var(--muted);
    font-size: 16px;
    margin-bottom: 0px;
}

.pill {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    background: rgba(0, 229, 255, 0.12);
    border: 1px solid rgba(0, 229, 255, 0.35);
    color: var(--cyan-soft);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 12px;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(23,31,51,0.95), rgba(34,42,61,0.95));
    padding: 18px;
    border-radius: 14px;
    border: 1px solid rgba(0, 229, 255, 0.18);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.04), 0 8px 25px rgba(0,0,0,0.22);
}

[data-testid="stMetricLabel"] {
    color: var(--muted);
    font-size: 14px;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    color: var(--cyan);
    font-size: 30px;
    font-weight: 800;
    font-family: 'Inter', sans-serif;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(23,31,51,0.85);
    border: 1px solid rgba(186,201,204,0.12);
    border-radius: 999px;
    padding: 8px 16px;
    color: var(--muted);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #00e5ff, #b0c6ff);
    color: #001f24;
    font-weight: 800;
}

h1, h2, h3 {
    color: var(--text) !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid rgba(0, 229, 255, 0.18);
    border-radius: 12px;
    overflow: hidden;
}

.stAlert {
    border-radius: 12px;
}

div.stButton > button, div.stDownloadButton > button {
    background: linear-gradient(135deg, #00e5ff, #b0c6ff);
    color: #001f24;
    border: none;
    border-radius: 10px;
    font-weight: 800;
    padding: 0.65rem 1rem;
}

.footer {
    text-align: center;
    color: var(--muted);
    padding: 18px;
    border-top: 1px solid rgba(0, 229, 255, 0.12);
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

PLOT_BG = "#0b1326"
PAPER_BG = "#171f33"
FONT = "#dae2fd"
CYAN_SCALE = ["#006875", "#00daf3", "#c3f5ff"]


def style_chart(fig):
    fig.update_layout(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font_color=FONT,
        title_font_color=FONT,
        title_font_size=18,
        margin=dict(l=20, r=20, t=55, b=20),
        legend=dict(bgcolor="rgba(0,0,0,0)")
    )
    fig.update_xaxes(gridcolor="rgba(218,226,253,0.08)", zerolinecolor="rgba(218,226,253,0.15)")
    fig.update_yaxes(gridcolor="rgba(218,226,253,0.08)", zerolinecolor="rgba(218,226,253,0.15)")
    return fig


with st.sidebar:
    if st.button("🔄 Refresh Job Data", use_container_width=True):
        with st.spinner("Scraping latest jobs from Internshala..."):
            subprocess.run(["python", "internshala_scraper.py"])
            subprocess.run(["python", "internshala_analysis.py"])
        st.success("Latest job data updated successfully!")
        st.rerun()

try:
    df = pd.read_csv("cleaned_internshala_jobs.csv")
except FileNotFoundError:
    st.error("cleaned_internshala_jobs.csv not found. Please run scraper first.")
    

required_columns = ["title", "company", "location", "salary", "experience", "skills", "job_type", "experience_level", "domain"]
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    st.error(f"Missing columns in dataset: {missing_columns}")
    

st.markdown("""
<div class="hero-card">
    <div class="pill">Live labor market intelligence</div>
    <div class="hero-title">🚀 AI Job Market Intelligence Platform</div>
    <p class="hero-subtitle">Analyze Internshala job listings, hiring domains, skills, work modes, experience demand, and career gaps using a modern data command-center dashboard.</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
# 🎯 Smart Filters
Use filters to explore job trends, domains, skills, and hiring insights.
""")

search = st.sidebar.text_input("Search job title/company/skill")
selected_locations = st.sidebar.multiselect(
    "Select Location",
    sorted(df["location"].dropna().unique()),
    default=sorted(df["location"].dropna().unique())
)
selected_companies = st.sidebar.multiselect(
    "Select Company",
    sorted(df["company"].dropna().unique()),
    default=sorted(df["company"].dropna().unique())
)

filtered_df = df[
    (df["location"].isin(selected_locations)) &
    (df["company"].isin(selected_companies))
].copy()

if search:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(search, case=False, na=False) |
        filtered_df["company"].str.contains(search, case=False, na=False) |
        filtered_df["location"].str.contains(search, case=False, na=False) |
        filtered_df["skills"].str.contains(search, case=False, na=False)
    ]

st.divider()
col1, col2, col3, col4 = st.columns(4)
col1.metric("💼 Total Jobs", len(filtered_df))
col2.metric("🏢 Companies", filtered_df["company"].nunique())
col3.metric("📍 Locations", filtered_df["location"].nunique())
col4.metric("🧠 Skill Groups", filtered_df["skills"].nunique())
st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "🧠 Skills",
    "🔎 Job Explorer",
    "🎯 Recommendation",
    "📈 Domain Analytics"
])

with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("🏙️ Top Locations")
        loc_data = filtered_df["location"].value_counts().head(10).reset_index()
        loc_data.columns = ["Location", "Jobs"]
        fig1 = px.bar(loc_data, x="Jobs", y="Location", orientation="h", title="Top Job Locations", color="Jobs", color_continuous_scale=CYAN_SCALE)
        st.plotly_chart(style_chart(fig1), use_container_width=True)

    with c2:
        st.subheader("🏢 Top Companies")
        comp_data = filtered_df["company"].value_counts().head(10).reset_index()
        comp_data.columns = ["Company", "Jobs"]
        fig2 = px.bar(comp_data, x="Jobs", y="Company", orientation="h", title="Top Hiring Companies", color="Jobs", color_continuous_scale="Blues")
        st.plotly_chart(style_chart(fig2), use_container_width=True)

    st.subheader("💼 Top Job Roles")
    role_data = filtered_df["title"].value_counts().head(15).reset_index()
    role_data.columns = ["Job Title", "Jobs"]
    fig3 = px.bar(role_data, x="Jobs", y="Job Title", orientation="h", title="Most Common Job Roles", color="Jobs", color_continuous_scale="Purples")
    st.plotly_chart(style_chart(fig3), use_container_width=True)

with tab2:
    st.subheader("🧠 Advanced Skill Analytics")
    skills_series = filtered_df["skills"].dropna().str.split(", ").explode()
    skills_series = skills_series[skills_series != "Not Mentioned"]

    if len(skills_series) > 0:
        skill_data = skills_series.value_counts().head(15).reset_index()
        skill_data.columns = ["Skill", "Jobs"]

        fig4 = px.bar(skill_data, x="Jobs", y="Skill", orientation="h", title="Top Skills in Job Listings", color="Jobs", color_continuous_scale="Teal")
        st.plotly_chart(style_chart(fig4), use_container_width=True)

        c1, c2 = st.columns(2)
        c1.success(f"🔥 Most Demanded Skill: {skill_data.iloc[0]['Skill'].title()}")
        c2.info(f"📌 Unique Skills Found: {skill_data['Skill'].nunique()}")

        st.subheader("🏆 Top Skills Leaderboard")
        st.dataframe(skill_data.reset_index(drop=True), use_container_width=True)

        selected_skill = st.selectbox("🎯 Filter Jobs By Skill", skill_data["Skill"].tolist())
        filtered_skill_jobs = filtered_df[
            filtered_df["skills"].str.contains(selected_skill, case=False, na=False)
        ]
        filtered_skill_jobs = filtered_skill_jobs[filtered_skill_jobs["title"] != "Not Available"]

        st.write(f"Jobs requiring **{selected_skill.title()}**: {len(filtered_skill_jobs)}")
        st.dataframe(
            filtered_skill_jobs[["title", "company", "location", "job_type", "experience_level", "domain"]].reset_index(drop=True),
            use_container_width=True
        )
    else:
        st.warning("No skills found in current filtered data.")

with tab3:
    st.subheader("🔎 Job Explorer")
    st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True, height=460)
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="⬇️ Download Filtered Jobs CSV",
        data=csv,
        file_name="filtered_internshala_jobs.csv",
        mime="text/csv"
    )

with tab4:
    st.subheader("🎯 Skill Recommendation System")
    user_skills = st.text_input("Enter your current skills", placeholder="Example: python, sql, excel")
    user_skills_list = []
    readiness_score = 0
    
    user_skills_list = []

    if user_skills:
    
        user_skills_list = [skill.strip().lower() for skill in user_skills.split(",")]

        # Match jobs
        skill_aliases = {
        "python": ["python", "data", "analytics", "data analyst", "data science", "machine learning", "ai"],
        "sql": ["sql", "data", "analytics", "data analyst", "business analyst", "database"],
        "excel": ["excel", "data", "analytics", "business analyst"],
        "power bi": ["power bi", "bi", "business intelligence", "analytics"],
        "machine learning": ["machine learning", "ml", "ai", "artificial intelligence"],
        "ai": ["ai", "artificial intelligence", "generative ai", "machine learning"],
        }

        expanded_skills = []

        for skill in user_skills_list:
            expanded_skills.append(skill)
            expanded_skills.extend(skill_aliases.get(skill, []))

        search_columns = [
        "title",
        "company",
        "location",
        "skills",
        "domain",
        "job_type",
         "experience_level"
        ]

        filtered_jobs = filtered_df[
            filtered_df[search_columns]
            .astype(str)
            .apply(lambda row: " ".join(row).lower(), axis=1)
            .apply(lambda text: any(f" {skill} " in f" {text} " for skill in expanded_skills))
        ]
        total_jobs = len(filtered_jobs)

        st.metric("🎯 Matching Jobs Found", total_jobs)

        if total_jobs > 0:

                st.success("Recommended Jobs Based On Your Skills")

                st.dataframe(
                    filtered_jobs.head(10),
                    use_container_width=True
                )

        # Missing Skills
        all_skills = filtered_jobs["skills"].dropna().str.split(", ").explode()
        
        if len(filtered_jobs) == 0:
                st.warning("No matching jobs found for these skills.")
                

        top_skills = all_skills.value_counts().head(10).index.tolist()

        missing_skills = [
            skill for skill in top_skills
            if skill.lower() not in user_skills_list
        ]

        st.subheader("📚 Skills You Should Learn")

        for skill in missing_skills[:5]:
            st.write(f"✅ {skill.title()}")
    
        matched_skills = [
            skill for skill in top_skills
            if skill.lower() in user_skills_list
            ]

        if len(top_skills) > 0:
            readiness_score = int((len(matched_skills) / len(top_skills)) * 100)
        else:
            readiness_score = 0

        st.subheader("📊 Career Readiness Score")
        st.progress(readiness_score / 100)
        st.metric("Readiness Score", f"{readiness_score}%")

        if readiness_score >= 80:
            recommended_role = "Data Analyst / AI Analyst"
            st.success(f"Recommended Role: {recommended_role}")
        elif readiness_score >= 50:
            recommended_role = "Junior Data Analyst"
            st.info(f"Recommended Role: {recommended_role}")
        else:
            recommended_role = "Beginner Data Science Learner"
            st.warning(f"Recommended Role: {recommended_role}")      
            
            
            
    st.subheader("📄 Resume Strength Analyzer")

    resume_score = readiness_score

    st.metric("Resume Fit Score", f"{resume_score}%")

    if resume_score >= 80:
            st.success("Your resume is strongly aligned with current job demand.")
    elif resume_score >= 50:
            st.info("Your resume is moderately aligned. Add missing skills to improve.")
    else:
            st.warning("Your resume needs improvement. Focus on the recommended missing skills.")

        
  

with tab5:
    st.subheader("📈 Domain Analytics")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🧩 Domain Distribution")
        domain_data = filtered_df["domain"].value_counts().reset_index()
        domain_data.columns = ["Domain", "Jobs"]
        fig_domain = px.pie(domain_data, names="Domain", values="Jobs", hole=0.45, title="Job Distribution by Domain", color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(style_chart(fig_domain), use_container_width=True)

    with col2:
        st.markdown("### 👨‍💼 Experience Level Distribution")
        exp_data = filtered_df["experience_level"].value_counts().reset_index()
        exp_data.columns = ["Experience Level", "Jobs"]
        fig_exp = px.bar(exp_data, x="Experience Level", y="Jobs", color="Experience Level", title="Jobs by Experience Level", color_discrete_sequence=px.colors.qualitative.Bold)
        st.plotly_chart(style_chart(fig_exp), use_container_width=True)

    st.markdown("### 🏢 Job Type Analysis")
    job_type_data = filtered_df["job_type"].value_counts().reset_index()
    job_type_data.columns = ["Job Type", "Jobs"]
    fig_type = px.bar(job_type_data, x="Job Type", y="Jobs", color="Job Type", title="Remote vs Hybrid vs Onsite Jobs", color_discrete_sequence=px.colors.qualitative.Vivid)
    st.plotly_chart(style_chart(fig_type), use_container_width=True)

    st.markdown("### 📌 Executive Insights")
    if len(filtered_df) > 0:
        top_domain = filtered_df["domain"].value_counts().idxmax()
        top_exp = filtered_df["experience_level"].value_counts().idxmax()
        top_type = filtered_df["job_type"].value_counts().idxmax()
        c1, c2, c3 = st.columns(3)
        c1.success(f"🔥 Top Domain: {top_domain}")
        c2.info(f"📊 Most Common Experience: {top_exp}")
        c3.warning(f"💼 Most Common Job Type: {top_type}")
    else:
        st.error("No data available")

st.markdown("""
<div class="footer">
Built with Python • Selenium • Pandas • Plotly • Streamlit<br>
AI Job Market Intelligence Platform
</div>
""", unsafe_allow_html=True)
