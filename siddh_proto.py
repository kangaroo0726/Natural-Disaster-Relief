import streamlit as st
import pandas as pd
import folium
import write_to_file
from streamlit_folium import st_folium
from folium import IFrame
from random import randint
import math
from streamlit_geolocation import streamlit_geolocation  # Correct import


# --- Page config ---
st.set_page_config(
    page_title="Shelter Dashboard",
    page_icon="🏠",
    layout="wide"
)

# --- Load CSV data ---
@st.cache_data(ttl=1)
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

# --- Initialize session state ---
if "df" not in st.session_state:
    st.session_state.df = load_data()

# --- Haversine function ---
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Earth radius in km
    return c * r

# --- Header ---
st.title("🏠 County Shelter Information Dashboard")
st.markdown("View all open shelters, their locations, and available services.")


# --- Sidebar filters ---
st.sidebar.header("Filter Shelters")
pet_filter = st.sidebar.checkbox("Pet Friendly Only", key="pet_filter")
medical_filter = st.sidebar.checkbox("Medical Facilities Only", key="medical_filter")

# --- Filter Logic ---
df = st.session_state.df
if pet_filter and medical_filter:
    filtered_df = df[(df["pet_friendly"]) & (df["medical"])]
elif medical_filter:
    filtered_df = df[df["medical"]]
elif pet_filter:
    filtered_df = df[df["pet_friendly"]]
else:
    filtered_df = df

# --- Main layout ---
col1, col2 = st.columns([2, 3])

# --- Admin Panel ---
st.sidebar.header("Admin Panel")
with st.sidebar.expander("Update Your Shelter Info"):
    typed_name = st.text_input("Enter Your Shelter Name", key="typed_name")
    if typed_name and typed_name in df["name"].values:
        shelter_row = df[df["name"] == typed_name].iloc[0]

        # Initialize session_state for inputs
        if f"occupancy_{typed_name}" not in st.session_state:
            st.session_state[f"occupancy_{typed_name}"] = int(shelter_row["current_occupancy"])
        if f"food_{typed_name}" not in st.session_state:
            st.session_state[f"food_{typed_name}"] = bool(shelter_row["food"])
        if f"water_{typed_name}" not in st.session_state:
            st.session_state[f"water_{typed_name}"] = bool(shelter_row["water"])

        # Input widgets with unique keys
        st.session_state[f"occupancy_{typed_name}"] = st.number_input(
            "Current Occupancy",
            min_value=0,
            max_value=int(shelter_row["capacity"]),
            value=st.session_state[f"occupancy_{typed_name}"],
            key=f"occupancy_input_{typed_name}"
        )
        st.session_state[f"food_{typed_name}"] = st.checkbox(
            "Food Available",
            value=st.session_state[f"food_{typed_name}"],
            key=f"food_checkbox_{typed_name}"
        )
        st.session_state[f"water_{typed_name}"] = st.checkbox(
            "Water Available",
            value=st.session_state[f"water_{typed_name}"],
            key=f"water_checkbox_{typed_name}"
        )

        # Update Button
        if st.button("Update Shelter", key=f"update_button_{typed_name}"):
            st.session_state.df.loc[df["name"] == typed_name, "current_occupancy"] = st.session_state[f"occupancy_{typed_name}"]
            st.session_state.df.loc[df["name"] == typed_name, "food"] = st.session_state[f"food_{typed_name}"]
            st.session_state.df.loc[df["name"] == typed_name, "water"] = st.session_state[f"water_{typed_name}"]

            # Recalculate remaining capacity
            st.session_state.df["remaining_capacity"] = st.session_state.df["capacity"] - st.session_state.df["current_occupancy"]

            # Write to CSV
            write_to_file.write_df_to_csv(st.session_state.df, "shelters.csv")
            st.success(f"{typed_name} updated successfully!")

# --- Shelter List ---
# Column 1: Shelter list + nearest shelter
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

    # --- Geolocation & nearest shelter ---
    st.subheader("📍 Find Nearest Shelter")
    user_location = streamlit_geolocation()

    # Only calculate distances if coordinates exist
    if (
        user_location
        and isinstance(user_location, dict)
        and user_location.get("latitude") is not None
        and user_location.get("longitude") is not None
    ):
        user_lat = user_location["latitude"]
        user_lon = user_location["longitude"]

        filtered_df = filtered_df.copy()
        filtered_df["distance_km"] = filtered_df.apply(
            lambda row: haversine(user_lat, user_lon, row["lat"], row["lon"]),
            axis=1,
        )

        nearest = filtered_df.loc[filtered_df["distance_km"].idxmin()]
        st.success(f"Nearest shelter: **{nearest['name']}** ({nearest['distance_km']:.1f} km away)")
        maps_link = f"https://www.google.com/maps/dir/{user_lat},{user_lon}/{nearest['lat']},{nearest['lon']}/"
        st.markdown(f"[Get Directions on Google Maps]({maps_link})")

    else:
        st.info("Please allow location access in your browser or your browser does not support geolocation.")

# --- Shelter Map ---
with col2:
    st.subheader("🗺️ Shelter Locations")
    midpoint = (
        filtered_df["lat"].mean() if not filtered_df.empty else 27.76,
        filtered_df["lon"].mean() if not filtered_df.empty else -82.66
    )
    m = folium.Map(location=midpoint, zoom_start=10, tiles="OpenStreetMap")

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
        folium.Marker(location=[row["lat"], row["lon"]], tooltip=row["name"], popup=popup).add_to(m)

    st_folium(m, width=700, height=500)

# --- Footer ---
st.markdown("---")
st.caption("Data Source: Local Shelter Dataset")
