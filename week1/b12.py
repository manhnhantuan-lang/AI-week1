import pandas as pd
import networkx as nx
import folium
from geopy.distance import geodesic

places = pd.DataFrame({
    "location": [
        "Kho hàng",
        "Quận 1",
        "Quận 3",
        "Quận 5",
        "Quận 10",
        "Bình Thạnh"
    ],
    "lat": [
        10.7618,
        10.7769,
        10.7828,
        10.7550,
        10.7700,
        10.8106
    ],
    "lon": [
        106.6676,
        106.7009,
        106.6870,
        106.6700,
        106.6670,
        106.7091
    ]
})

G = nx.Graph()

for i in range(len(places)):
    for j in range(i + 1, len(places)):

        p1 = (
            places.loc[i, "lat"],
            places.loc[i, "lon"]
        )

        p2 = (
            places.loc[j, "lat"],
            places.loc[j, "lon"]
        )

        dist = geodesic(p1, p2).km

        G.add_edge(
            places.loc[i, "location"],
            places.loc[j, "location"],
            weight=dist
        )

start = "Kho hàng"

visited = [start]
current = start

remaining = list(places["location"])
remaining.remove(start)

while len(remaining) > 0:

    nearest = None
    nearest_dist = float("inf")

    for node in remaining:

        dist = G[current][node]["weight"]

        if dist < nearest_dist:
            nearest_dist = dist
            nearest = node

    visited.append(nearest)
    current = nearest
    remaining.remove(nearest)

total_distance = 0

for i in range(len(visited) - 1):

    total_distance += G[
        visited[i]
    ][
        visited[i + 1]
    ]["weight"]

print("Tuyến giao hàng tối ưu:")
print(" → ".join(visited))

print("Tổng khoảng cách:", round(total_distance, 2), "km")

center_lat = places["lat"].mean()
center_lon = places["lon"].mean()

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=12
)

for _, row in places.iterrows():

    color = "red" if row["location"] == "Kho hàng" else "blue"

    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=row["location"],
        icon=folium.Icon(color=color)
    ).add_to(m)

for i in range(len(visited) - 1):

    start_name = visited[i]
    end_name = visited[i + 1]

    start_row = places[
        places["location"] == start_name
    ].iloc[0]

    end_row = places[
        places["location"] == end_name
    ].iloc[0]

    line_coords = [
        (start_row["lat"], start_row["lon"]),
        (end_row["lat"], end_row["lon"])
    ]

    folium.PolyLine(
        locations=line_coords,
        color="red",
        weight=4,
        popup=f"{start_name} → {end_name}"
    ).add_to(m)

m