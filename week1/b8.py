import pandas as pd
import folium
from geopy.distance import geodesic

customers = pd.DataFrame({
    "name": ["C1", "C2", "C3"],
    "lat": [10.773, 10.760, 10.768],
    "lon": [106.700, 106.690, 106.680]
})

cars = pd.DataFrame({
    "car_id": ["A", "B", "C"],
    "lat": [10.761, 10.770, 10.755],
    "lon": [106.683, 106.695, 106.678]
})

matches = []
used_cars = []

m = folium.Map(
    location=[customers["lat"].mean(), customers["lon"].mean()],
    zoom_start=13
)

for _, row in customers.iterrows():
    folium.Marker(
        [row["lat"], row["lon"]],
        popup=f"Khách {row['name']}",
        icon=folium.Icon(color="blue")
    ).add_to(m)

for _, row in cars.iterrows():
    folium.Marker(
        [row["lat"], row["lon"]],
        popup=f"Xe {row['car_id']}",
        icon=folium.Icon(color="green")
    ).add_to(m)

for _, c in customers.iterrows():

    best_car = None
    best_dist = float("inf")
    best_coords = None

    for _, car in cars.iterrows():

        if car["car_id"] in used_cars:
            continue

        d = geodesic(
            (c["lat"], c["lon"]),
            (car["lat"], car["lon"])
        ).km

        if d < best_dist:
            best_dist = d
            best_car = car["car_id"]
            best_coords = (car["lat"], car["lon"])

    if best_car is not None:

        used_cars.append(best_car)

        matches.append([
            c["name"],
            best_car,
            best_dist
        ])

        folium.PolyLine(
            locations=[
                (c["lat"], c["lon"]),
                best_coords
            ],
            color="red",
            weight=3,
            popup=f"{c['name']} → Xe {best_car} ({best_dist:.2f} km)"
        ).add_to(m)

match_df = pd.DataFrame(
    matches,
    columns=["customer", "nearest_car", "distance_km"]
)

print(match_df)

m