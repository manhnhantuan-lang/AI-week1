import osmnx as ox
import networkx as nx
import folium
import pandas as pd
from datetime import datetime, timedelta
from folium.plugins import TimestampedGeoJson

ox.settings.use_cache = True
ox.settings.log_console = False

G = ox.graph_from_point(
    (10.7769, 106.7009),
    dist=2500,
    network_type="drive"
)

vehicles = pd.DataFrame({
    "vehicle_id": ["Xe 1", "Xe 2"],
    "start_lat": [10.7725, 10.7716],
    "start_lon": [106.6980, 106.7050],
    "dest_lat": [10.7798, 10.7755],
    "dest_lon": [106.6990, 106.6917]
})

colors = ["blue", "green"]
features = []

m = folium.Map(location=[10.7769, 106.7009], zoom_start=14, tiles="cartodbpositron")

start_time = datetime(2026, 4, 24, 8, 0, 0)

for idx, row in vehicles.iterrows():
    orig_node = ox.distance.nearest_nodes(G, X=row["start_lon"], Y=row["start_lat"])
    dest_node = ox.distance.nearest_nodes(G, X=row["dest_lon"], Y=row["dest_lat"])

    route = nx.shortest_path(G, orig_node, dest_node, weight="length")

    route_coords = []
    for node in route:
        route_coords.append((G.nodes[node]["y"], G.nodes[node]["x"]))

    folium.PolyLine(
        route_coords,
        color=colors[idx],
        weight=4,
        popup=row["vehicle_id"]
    ).add_to(m)

    folium.Marker(
        [row["start_lat"], row["start_lon"]],
        popup=f"{row['vehicle_id']} - Start",
        icon=folium.Icon(color=colors[idx])
    ).add_to(m)

    folium.Marker(
        [row["dest_lat"], row["dest_lon"]],
        popup=f"{row['vehicle_id']} - Destination",
        icon=folium.Icon(color="red", icon="flag")
    ).add_to(m)

    step_count = max(len(route_coords) - 1, 1)

    for t, (lat, lon) in enumerate(route_coords):
        current_time = start_time + timedelta(minutes=t * 2)

        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "properties": {
                "time": current_time.isoformat(),
                "popup": f"{row['vehicle_id']}<br>Step: {t}",
                "icon": "circle",
                "iconstyle": {
                    "fillColor": colors[idx],
                    "fillOpacity": 0.9,
                    "stroke": "true",
                    "radius": 6
                }
            }
        })

TimestampedGeoJson(
    {
        "type": "FeatureCollection",
        "features": features
    },
    period="PT2M",
    add_last_point=True,
    auto_play=False,
    loop=False,
    max_speed=1,
    loop_button=True,
    date_options="YYYY-MM-DD HH:mm:ss",
    time_slider_drag_update=True
).add_to(m)

m