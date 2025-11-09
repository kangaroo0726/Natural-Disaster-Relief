import streamlit as st
import pandas as pd

# --- Load data ---
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

pet_filter = st.sidebar.checkbox("Show Pet-Friendly Shelters")
medical_filter = st.sidebar.checkbox("Show Medical Shelters")

# --- Filter logic ---
if pet_filter and not medical_filter:
    filtered_df = df[df["pet_friendly"]]
elif medical_filter and not pet_filter:
    filtered_df = df[df["medical"]]
else:
    # Default: show only general shelters
    filtered_df = df[df["type"] == "General"]

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
    if not filtered_df.empty:
        st.map(filtered_df[["lat", "lon"]])
    else:
        st.info("No shelters available.")

# --- Footer ---
st.markdown("---")
st.caption("Data Source: Local Shelter Dataset")
