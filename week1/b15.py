import pandas as pd
import folium
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

history = pd.DataFrame({
    "district": [
        "Quận 1", "Quận 3", "Quận 5", "Quận 7",
        "Quận 10", "Bình Thạnh", "Phú Nhuận", "Tân Bình"
    ],
    "lat": [10.7769, 10.7828, 10.7550, 10.7297, 10.7700, 10.8106, 10.7990, 10.8010],
    "lon": [106.7009, 106.6870, 106.6700, 106.7210, 106.6670, 106.7091, 106.6800, 106.6520],
    "population_density": [18000, 15000, 14000, 10000, 13000, 12000, 11000, 10500],
    "income": [28, 24, 20, 22, 18, 17, 19, 16],
    "traffic_level": [9, 8, 7, 5, 6, 7, 6, 5],
    "competitor_count": [12, 10, 9, 6, 8, 7, 7, 5],
    "store_performance": [420, 360, 320, 250, 290, 270, 260, 230]
})

features = [
    "population_density",
    "income",
    "traffic_level",
    "competitor_count",
    "lat",
    "lon"
]

X = history[features]
y = history["store_performance"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42
)

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

pred = model.predict(X_test)
mae = mean_absolute_error(y_test, pred)

print("MAE:", round(mae, 2))

result = pd.DataFrame({
    "District": history.loc[y_test.index, "district"].values,
    "Latitude": history.loc[y_test.index, "lat"].values,
    "Longitude": history.loc[y_test.index, "lon"].values,
    "Actual": y_test.values,
    "Predicted": pred
})

print(result)

candidates = pd.DataFrame({
    "district": ["Quận 2", "Quận 4", "Thủ Đức", "Gò Vấp", "Quận 11"],
    "lat": [10.7870, 10.7580, 10.8440, 10.8390, 10.7760],
    "lon": [106.7420, 106.7040, 106.7620, 106.6650, 106.6560],
    "population_density": [11000, 14000, 12500, 13000, 14500],
    "income": [24, 20, 22, 18, 19],
    "traffic_level": [6, 7, 5, 6, 7],
    "competitor_count": [4, 8, 5, 7, 9]
})

candidates["predicted_score"] = model.predict(candidates[features])

best_site = candidates.loc[candidates["predicted_score"].idxmax()]

print("Đề xuất vị trí cửa hàng:")
print(best_site[["district", "lat", "lon", "predicted_score"]])

m = folium.Map(
    location=[history["lat"].mean(), history["lon"].mean()],
    zoom_start=11,
    tiles="cartodbpositron"
)

for _, row in history.iterrows():
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=5,
        color="blue",
        fill=True,
        fill_opacity=0.6,
        popup=f"{row['district']}<br>Performance: {row['store_performance']}"
    ).add_to(m)

for _, row in candidates.iterrows():
    color = "red" if row["predicted_score"] >= best_site["predicted_score"] else "orange"
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=8,
        color=color,
        fill=True,
        fill_opacity=0.7,
        popup=f"{row['district']}<br>Predicted score: {row['predicted_score']:.2f}"
    ).add_to(m)

folium.Marker(
    location=[best_site["lat"], best_site["lon"]],
    popup=f"Đề xuất đặt cửa hàng: {best_site['district']}",
    icon=folium.Icon(color="red", icon="star")
).add_to(m)

folium.Circle(
    location=[best_site["lat"], best_site["lon"]],
    radius=3000,
    color="red",
    fill=True,
    fill_opacity=0.12
).add_to(m)

m