import pandas as pd
import folium
import streamlit as st
from streamlit_folium import st_folium


# ============================================================
# NASTAVENÍ STREAMLIT
# ============================================================

st.set_page_config(
    page_title="Mapa FVE a meteorologických stanic",
    layout="wide"
)

st.title("Mapa FVE a meteorologických stanic")


# ============================================================
# NAČTENÍ DAT
# ============================================================

sheet_id = "1pxAvPoklHC35djjyYYGxc4tr8HBxtetL"
xlsx_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"


@st.cache_data
def nacti_data():

    meteo = pd.read_excel(
        xlsx_url,
        sheet_name="Data"
    )

    fve = pd.read_excel(
        xlsx_url,
        sheet_name="FVE"
    )

    return meteo, fve


meteo, fve = nacti_data()


# ============================================================
# RGLB10
# ============================================================

rglb10 = meteo[
    meteo["EG_EL_ABBREVIATION"] == "RGLB10"
].copy()


# ============================================================
# MAPA ČESKÉ REPUBLIKY
# ============================================================

m = folium.Map(
    location=[49.8, 15.5],
    zoom_start=7,
    tiles=(
        "https://server.arcgisonline.com/ArcGIS/rest/services/"
        "World_Street_Map/MapServer/tile/{z}/{y}/{x}"
    ),
    attr="Tiles © Esri"
)


# ============================================================
# RGLB10 – MODRÉ BODY
# ============================================================

for _, row in rglb10.iterrows():

    folium.CircleMarker(
        location=[
            row["Latitude"],
            row["Longtitude"]
        ],
        radius=6,
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.8,
        popup="RGLB10"
    ).add_to(m)


# ============================================================
# FVE – ČERVENÉ BODY
# ============================================================

for _, row in fve.iterrows():

    folium.CircleMarker(
        location=[
            row["Latitude"],
            row["Longitude"]
        ],
        radius=4,
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=0.8,
        popup=str(row["Název"])
    ).add_to(m)


# ============================================================
# ZOBRAZENÍ MAPY
# ============================================================

st_folium(
    m,
    width=None,
    height=700
)

