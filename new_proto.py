import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- Page config ---
st.set_page_config(
    page_title="Shelter Dashboard",
    page_icon="🏠",
    layout="wide"
)

# --- Load CSV data ---
@st.cache_data
def load_data():
    return pd.read_json("shelterData.csv")

df = load_data()

# --- Clean type column for consistent comparison ---
df["type"] = df["type"].astype(str).str.strip().str.lower()

# --- Header ---
st.title("🏠 County Shelter Information Dashboard")
st.markdown("View all open shelters, their locations, and available services.")

# --- Sidebar filters ---
st.sidebar.header("Filter Shelters")

pet_filter = st.sidebar.checkbox("Pet Friendly Only")
medical_filter = st.sidebar.checkbox("Medical Facilities Only")

# --- Filter Logic ---
if pet_filter and medical_filter:
    filtered_df = df[(df["pet_friendly"]) & (df["medical"])]
elif medical_filter:
    filtered_df = df[df["medical"]]
elif pet_filter:
    filtered_df = df[df["pet_friendly"]]
else:
    filtered_df = df[df["type"].str.contains("general", case = False, na = False)]


# --- Main section ---
col1, col2 = st.columns([2, 3])

# Column 1: Shelter list
with col1:
    st.subheader("📋 Shelter List")
    st.dataframe(
        filtered_df[
            [
                "name",
                "address",
                "capacity",
                "current_occupancy",
                "food",
                "water",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

# Column 2: Map
with col2:
    st.subheader("🗺️ Shelter Locations")

    # Center the map
    midpoint = (filtered_df["lat"].mean(), filtered_df["lon"].mean())
    m = folium.Map(location=midpoint, zoom_start=10, tiles="OpenStreetMap")

    # Add markers
    for _, row in filtered_df.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            tooltip=row["name"],
            popup=(
                f"<b>{row['name']}</b><br>"
                f"Address: {row['address']}<br>"
                f"Type: {row['type']}<br>"
                f"Capacity: {row['capacity']}<br>"
                f"Food: {'Yes' if row['food'] else 'No'}<br>"
                f"Water: {'Yes' if row['water'] else 'No'}<br>"
                f"Medical: {'Yes' if row['medical'] else 'No'}<br>"
                f"Pet Friendly: {'Yes' if row['pet_friendly'] else 'No'}"
            ),
        ).add_to(m)

    # Render map
    st_folium(m, width=700, height=500)

# --- Footer ---
st.markdown("---")
st.caption("Data Source: Local Shelter Dataset")
