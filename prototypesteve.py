import streamlit as st
import pandas as pd
import folium
import write_to_file
from streamlit_folium import st_folium
from folium import IFrame

# --- Page config ---
st.set_page_config(
    page_title="Shelter Dashboard",
    page_icon="🏠",
    layout="wide"
)

# --- Load CSV data ---
@st.cache_data
def load_data():
    data = write_to_file.read_csv_to_dict("shelters.csv")
    all_shelters = {}
    for category, shelters in data.items():
        for s in shelters:
            name = s[0]
            if name not in all_shelters:
                all_shelters[name] = {
                    "name": s[0],
                    "type": s[1],
                    "address": s[2],
                    "lat": s[3],
                    "lon": s[4],
                    "capacity": s[5],
                    "current_occupancy": s[6],
                    "food": s[7],
                    "water": s[8],
                    "medical": (category == "medical"),
                    "pet_friendly": (category == "pet_friendly")
                }   
            if category == "medical":
                all_shelters[name]["medical"] = True
            if category == "pet_friendly":
                all_shelters[name]["pet_friendly"] = True

    df = pd.DataFrame(all_shelters.values())
    df["remaining_capacity"] = df["capacity"] - df["current_occupancy"]
    return df
 
df = load_data()

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
    filtered_df = df


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
                "remaining_capacity",
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
    midpoint = (
        filtered_df["lat"].mean() if not filtered_df.empty else 27.76,
        filtered_df["lon"].mean() if not filtered_df.empty else -82.66
    )
    m = folium.Map(location=midpoint, zoom_start=10, tiles="OpenStreetMap")

    # Add markers
    for _, row in filtered_df.iterrows():
        html_content = f"""
        <div style="width: 250px; font-family: Arial; line-height: 1.4; padding: 5px;">
            <b>{row['name']}</b><br>
            Address: {row['address']}<br>
            Remaining Capacity: {row['remaining_capacity']}<br>
            Food: {'Yes' if row['food'] else 'No'}<br>
            Water: {'Yes' if row['water'] else 'No'}<br>
            Medical: {'Yes' if row['medical'] else 'No'}<br>
            Pet Friendly: {'Yes' if row['pet_friendly'] else 'No'}
        </div>
        """
        iframe = IFrame(html=html_content, width=270, height=180)
        popup = folium.Popup(iframe, max_width=300)

        folium.Marker(
            location=[row["lat"], row["lon"]],
            tooltip=row["name"],
            popup=popup,
        ).add_to(m)

    # Render map
    st_folium(m, width=700, height=500)

# --- Footer ---
st.markdown("---")
st.caption("Data Source: Local Shelter Dataset") 