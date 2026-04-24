import folium
import pandas as pd
from folium.plugins import HeatMap

center = (10.7618, 106.6676)

locations = pd.DataFrame({
    "district": [
        "Quận 1",
        "Quận 3",
        "Quận 5",
        "Quận 7",
        "Quận 10",
        "Bình Thạnh"
    ],
    "lat": [
        10.7769,
        10.7828,
        10.7550,
        10.7297,
        10.7700,
        10.8106
    ],
    "lon": [
        106.7009,
        106.6870,
        106.6700,
        106.7210,
        106.6670,
        106.7091
    ],
    "demand": [
        420,
        360,
        320,
        250,
        290,
        270
    ]
})

m = folium.Map(
    location=center,
    zoom_start=11
)

folium.Marker(
    location=center,
    popup="Kho trung tâm",
    icon=folium.Icon(color="red")
).add_to(m)

for _, row in locations.iterrows():

    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=f"""
        {row['district']}<br>
        Demand: {row['demand']}
        """,
        icon=folium.Icon(color="blue")
    ).add_to(m)

heat_data = []

for _, row in locations.iterrows():

    heat_data.append([
        row["lat"],
        row["lon"],
        row["demand"]
    ])

HeatMap(
    heat_data,
    radius=25,
    blur=20
).add_to(m)

for radius in [3000, 6000, 9000]:

    folium.Circle(
        location=center,
        radius=radius,
        color="green",
        fill=False,
        popup=f"Service Area {radius/1000:.0f} km"
    ).add_to(m)

m