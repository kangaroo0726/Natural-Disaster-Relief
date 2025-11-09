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

# --- Load JSON data ---
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
    filtered_df = df[df["type"].str.contains("general", case=False, na=False)]

# --- Create map ---
midpoint = (filtered_df["lat"].mean(), filtered_df["lon"].mean())
m = folium.Map(location=midpoint, zoom_start=10, tiles="OpenStreetMap")

# Add smaller blue circle markers with tooltip
for _, row in filtered_df.iterrows():
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=4,           # smaller marker
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.7,
        tooltip=row["name"],  # show name on hover
    ).add_to(m)

# --- Layout ---
col1, col2 = st.columns([2, 3])

# Column 2: Map
with col2:
    st.subheader("🗺️ Shelter Locations")
    map_data = st_folium(m, width=700, height=500)

# Column 1: Shelter list / selected info
with col1:
    st.subheader("📋 Shelter Information")

    # If a marker was clicked, display info
    if map_data and map_data.get("last_object_clicked_tooltip"):
        selected_name = map_data["last_object_clicked_tooltip"]
        selected = filtered_df[filtered_df["name"] == selected_name].iloc[0]

        st.markdown(f"### 🏠 {selected['name']}")
        st.write(f"**Address:** {selected['address']}")
        st.write(f"**Food Available:** {'✅' if selected['food'] else '❌'}")
        st.write(f"**Water Available:** {'✅' if selected['water'] else '❌'}")
        st.write(f"**Capacity:** {selected['capacity']}")
        st.write(f"**Current Occupancy:** {selected['current_occupancy']}")
        st.write(f"**Medical:** {'✅' if selected['medical'] else '❌'}")
        st.write(f"**Pet Friendly:** {'✅' if selected['pet_friendly'] else '❌'}")

    else:
        # Show the default shelter list
        st.dataframe(
            filtered_df[
                ["name", "address", "food", "water"]
            ],
            use_container_width=True,
            hide_index=True,
        )

# --- Footer ---
st.markdown("---")
st.caption("Data Source: Local Shelter Dataset")
