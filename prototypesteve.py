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

# --- Header ---
st.title("🏠 County Shelter Information Dashboard")
st.markdown("View all open shelters, their locations, and available services.")

# --- Sidebar filters ---
st.sidebar.header("Filter Shelters")
type_filter = st.sidebar.multiselect(
    "Shelter Type", df["type"].unique(), default=df["type"].unique()
)
pet_filter = st.sidebar.checkbox("Pet Friendly Only")
medical_filter = st.sidebar.checkbox("Medical Facilities Only")

filtered_df = df[df["type"].isin(type_filter)]
if pet_filter:
    filtered_df = filtered_df[filtered_df["pet_friendly"]]
if medical_filter:
    filtered_df = filtered_df[filtered_df["medical"]]

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
                "type",
                "capacity",
                "current_occupancy",
                "food",
                "water",
                "medical",
                "pet_friendly",
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
