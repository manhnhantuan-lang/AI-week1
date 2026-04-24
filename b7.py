import osmnx as ox
import networkx as nx
import folium
G = ox.graph_from_point(
    (10.7769, 106.7009),
    dist=3000,
    network_type="drive"
)
origin = ox.geocode("Chợ Bến Thành, Ho Chi Minh City, Vietnam")
destination = ox.geocode("Nhà thờ Đức Bà, Ho Chi Minh City, Vietnam")
orig_node = ox.distance.nearest_nodes(G, X=origin[1], Y=origin[0])
dest_node = ox.distance.nearest_nodes(G, X=destination[1], Y=destination[0])
route = nx.shortest_path(G, orig_node, dest_node, weight="length")
route_length = nx.shortest_path_length(
    G,
    orig_node,
    dest_node,
    weight="length"
)

print("Quãng đường (m):", round(route_length, 2))
m = folium.Map(location=origin, zoom_start=15)
folium.Marker(
    origin,
    popup="Start",
    icon=folium.Icon(color="green")
).add_to(m)
folium.Marker(
    destination,
    popup="Destination",
    icon=folium.Icon(color="red")
).add_to(m)
route_coords = []
for node in route:
    point = G.nodes[node]
    route_coords.append((point["y"], point["x"]))
folium.PolyLine(
    route_coords,
    color="blue",
    weight=5
).add_to(m)

m