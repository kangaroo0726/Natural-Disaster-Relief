import streamlit as st
import pandas as pd

# Load CSV data
@st.cache_data
def load_data():
    return pd.read_json("shelterData.csv")

df = load_data()

# --- Page config ---
st.set_page_config(
    page_title="Shelter Dashboard",
    page_icon="🏠",
    layout="wide"
)

# --- Header ---
st.title("🏠 County Shelter Information Dashboard")
st.markdown("View all open shelters, their locations, and available services.")

# --- Sidebar filters ---
st.sidebar.header("Filter Shelters")
type_filter = st.sidebar.multiselect("Shelter Type", df["type"].unique(), default=df["type"].unique())
pet_filter = st.sidebar.checkbox("Pet Friendly Only")
medical_filter = st.sidebar.checkbox("Medical Facilities Only")

filtered_df = df[df["type"].isin(type_filter)]
if pet_filter:
    filtered_df = filtered_df[filtered_df["pet_friendly"]]
if medical_filter:
    filtered_df = filtered_df[filtered_df["medical"]]

# --- Main section ---
col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("📋 Shelter List")
    st.dataframe(
        filtered_df[[
            "name", "address", "type", "capacity", "current_occupancy",
            "food", "water", "medical", "pet_friendly"
        ]],
        use_container_width=True,
        hide_index=True
    )

with col2:
    st.subheader("🗺️ Shelter Locations")
    st.map(filtered_df[["lat", "lon"]])

# --- Summary stats ---
st.markdown("### 📊 Summary Statistics")
colA, colB, colC, colD = st.columns(4)
colA.metric("Total Shelters", len(filtered_df))
colB.metric("Total Capacity", filtered_df["capacity"].sum())
colC.metric("Average Capacity", int(filtered_df["capacity"].mean()))
colD.metric("Pet Friendly", sum(filtered_df["pet_friendly"]))

# --- Footer ---
st.markdown("---")
st.caption("Data Source: Local Shelter Dataset | Streamlit App by You 😊")
