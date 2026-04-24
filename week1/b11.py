import pandas as pd
import numpy as np
import folium
from sklearn.cluster import KMeans

np.random.seed(42)

center = [10.7769, 106.7009]

customer_data = pd.DataFrame({
    "lat": np.random.normal(10.7769, 0.02, 120),
    "lon": np.random.normal(106.7009, 0.02, 120)
})

X = customer_data[["lat", "lon"]]

kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

customer_data["cluster"] = kmeans.fit_predict(X)

warehouse_locations = pd.DataFrame(
    kmeans.cluster_centers_,
    columns=["lat", "lon"]
)

print("Vị trí kho hàng đề xuất:")
print(warehouse_locations)

m = folium.Map(
    location=center,
    zoom_start=12
)

colors = ["red", "blue", "green"]

for _, row in customer_data.iterrows():

    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=4,
        color=colors[int(row["cluster"])],
        fill=True,
        fill_opacity=0.6,
        popup=f"Cluster {int(row['cluster'])}"
    ).add_to(m)

for i, row in warehouse_locations.iterrows():

    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=f"Kho hàng tối ưu {i+1}",
        icon=folium.Icon(
            color=colors[i],
            icon="home"
        )
    ).add_to(m)

    folium.Circle(
        location=[row["lat"], row["lon"]],
        radius=3000,
        color=colors[i],
        fill=True,
        fill_opacity=0.08
    ).add_to(m)

m