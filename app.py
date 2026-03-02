# ================================
# Employee Engagement & Burnout Dashboard
# Frontend: Streamlit
# Role: Data Analyst / Frontend Dashboard
# ================================

# ---------- 1. IMPORT LIBRARIES ----------
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- 2. PAGE CONFIG ----------
st.set_page_config(
    page_title="Employee Engagement & Burnout Dashboard",
    layout="wide"
)

# ---------- 3. TITLE ----------
st.title("Employee Engagement, Satisfaction & Burnout Dashboard")

# ---------- 4. LOAD DATA ----------
@st.cache_data
def load_data():
    df = pd.read_csv("data/Palo_Alto_Networks.csv")
    return df

df = load_data()

# ---------- 5. FEATURE ENGINEERING ----------
df["Engagement_Index"] = (
    df["JobInvolvement"] +
    df["JobSatisfaction"] +
    df["EnvironmentSatisfaction"] +
    df["RelationshipSatisfaction"]
) / 4

def burnout_level(row):
    if row["OverTime"] == "Yes" and row["WorkLifeBalance"] <= 2:
        return "High"
    elif row["OverTime"] == "Yes":
        return "Medium"
    else:
        return "Low"

df["Burnout_Level"] = df.apply(burnout_level, axis=1)

# ---------- 6. SIDEBAR FILTERS ----------
st.sidebar.header("Filters")

department_filter = st.sidebar.selectbox(
    "Select Department",
    ["All"] + sorted(df["Department"].unique().tolist())
)

overtime_filter = st.sidebar.selectbox(
    "Overtime",
    ["All", "Yes", "No"]
)

min_engagement = st.sidebar.slider(
    "Minimum Engagement Index",
    float(df["Engagement_Index"].min()),
    float(df["Engagement_Index"].max()),
    float(df["Engagement_Index"].mean())
)

# ---------- 7. APPLY FILTERS ----------
filtered_df = df.copy()

if department_filter != "All":
    filtered_df = filtered_df[filtered_df["Department"] == department_filter]

if overtime_filter != "All":
    filtered_df = filtered_df[filtered_df["OverTime"] == overtime_filter]

filtered_df = filtered_df[
    filtered_df["Engagement_Index"] >= min_engagement
]

# ---------- 8. KPI METRICS ----------
st.subheader("Engagement Health Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Engagement Index",
        round(filtered_df["Engagement_Index"].mean(), 2)
    )

with col2:
    st.metric(
        "Average Work-Life Balance",
        round(filtered_df["WorkLifeBalance"].mean(), 2)
    )

with col3:
    high_burnout_pct = (
        filtered_df["Burnout_Level"].value_counts(normalize=True).get("High", 0) * 100
    )
    st.metric(
        "High Burnout %",
        f"{round(high_burnout_pct, 2)}%"
    )

# ---------- 9. VISUALIZATIONS ----------
st.subheader("Engagement Distribution")
fig1 = px.histogram(
    filtered_df,
    x="Engagement_Index",
    nbins=20,
    title="Distribution of Engagement Index"
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Engagement by Department")
fig2 = px.bar(
    filtered_df,
    x="Department",
    y="Engagement_Index",
    color="Department",
    title="Average Engagement by Department",
    barmode="group"
)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Burnout Level Distribution")
fig3 = px.pie(
    filtered_df,
    names="Burnout_Level",
    title="Burnout Level Distribution"
)
st.plotly_chart(fig3, use_container_width=True)

# ---------- 10. DATA PREVIEW ----------
with st.expander("View Filtered Dataset"):
    st.dataframe(filtered_df)
