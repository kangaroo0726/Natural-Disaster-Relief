import streamlit as st
import pandas as pd
import pydeck as pdk

# --- Page config ---
st.set_page_config(
    page_title="Shelter Dashboard",
    page_icon="🏠",
    layout="wide"
)

# --- Load CSV data ---
@st.cache_data
def load_data():
    return pd.read_json("shelterData.csv")  # make sure this is a proper CSV

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

# --- Color markers by type ---
type_colors = {
    "General Shelter": [0, 100, 255, 180],   # blue
    "Special Needs": [255, 0, 0, 180],       # red
    "Pet Friendly": [0, 200, 0, 180],        # green
}

# Add a 'color' column to filtered_df
filtered_df["color"] = filtered_df["type"].map(type_colors)

# --- Main section ---
col1, col2 = st.columns([2, 3])

with col1:
    # Shelter list in an expander
    with st.expander("📋 Shelter List", expanded=True):
        st.dataframe(
            filtered_df[[
                "name", "address", "type", "capacity", "current_occupancy",
                "food", "water", "medical", "pet_friendly"
            ]],
            use_container_width=True,
            hide_index=True
        )

    # Dropdown to select a shelter for details
    selected_shelter = st.selectbox(
        "Select a Shelter to See Details",
        filtered_df["name"]
    )

    if selected_shelter:
        shelter_info = filtered_df[filtered_df["name"] == selected_shelter].iloc[0]
        st.markdown("### 🏠 Shelter Details")
        st.write({
            "Name": shelter_info["name"],
            "Address": shelter_info["address"],
            "Type": shelter_info["type"],
            "Capacity": shelter_info["capacity"],
            "Current Occupancy": shelter_info["current_occupancy"],
            "Food Available": shelter_info["food"],
            "Water Available": shelter_info["water"],
            "Medical Facilities": shelter_info["medical"],
            "Pet Friendly": shelter_info["pet_friendly"]
        })

with col2:
    st.subheader("🗺️ Shelter Locations")

    midpoint = (filtered_df["lat"].mean(), filtered_df["lon"].mean())

    st.pydeck_chart(
        pdk.Deck(
            map_provider="openstreetmap",
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=midpoint[0],
                longitude=midpoint[1],
                zoom=10,
                pitch=0,
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=filtered_df,
                    get_position=["lon", "lat"],
                    get_color="color",
                    get_radius=150,
                    pickable=True,
                ),
            ],
            tooltip={
                "html": "<b>{name}</b><br/>{address}<br/>Type: {type}<br/>Capacity: {capacity}",
                "style": {"color": "white"}
            }
        )
    )

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
