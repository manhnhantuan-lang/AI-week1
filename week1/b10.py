import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

from geopy.distance import geodesic

ox.settings.use_cache = True
ox.settings.log_console = False

G = ox.graph_from_place(
    "District 1, Ho Chi Minh City, Vietnam",
    network_type="drive"
)

places = pd.DataFrame({
    "name": [
        "Bến Thành",
        "Nhà thờ Đức Bà",
        "Phố đi bộ Nguyễn Huệ",
        "Bitexco",
        "Chợ Tân Định",
        "Công viên Tao Đàn"
    ],
    "lat": [10.7724, 10.7798, 10.7740, 10.7716, 10.7905, 10.7755],
    "lon": [106.6980, 106.6990, 106.7030, 106.7049, 106.6865, 106.6917],
    "risk_score": [0.90, 0.85, 0.80, 0.65, 0.30, 0.45]
})

risk_dict = dict(zip(places["name"], places["risk_score"]))

source_name = "Bến Thành"
target_name = "Chợ Tân Định"

source_row = places.loc[places["name"] == source_name].iloc[0]
target_row = places.loc[places["name"] == target_name].iloc[0]

orig_node = ox.distance.nearest_nodes(
    G,
    X=source_row["lon"],
    Y=source_row["lat"]
)
dest_node = ox.distance.nearest_nodes(
    G,
    X=target_row["lon"],
    Y=target_row["lat"]
)

shortest_route = nx.shortest_path(G, orig_node, dest_node, weight="length")
shortest_length = nx.shortest_path_length(G, orig_node, dest_node, weight="length")

G_cost = G.copy()

high_risk_names = places.loc[places["risk_score"] >= 0.8, "name"].tolist()
high_risk_nodes = set()

for _, row in places.iterrows():
    if row["name"] in high_risk_names:
        node = ox.distance.nearest_nodes(G_cost, X=row["lon"], Y=row["lat"])
        high_risk_nodes.add(node)

for u, v, k, data in G_cost.edges(keys=True, data=True):
    base_length = data.get("length", 1)
    if u in high_risk_nodes or v in high_risk_nodes:
        data["cost"] = base_length * 5
    else:
        data["cost"] = base_length

alternative_route = nx.shortest_path(G_cost, orig_node, dest_node, weight="cost")
alternative_length = nx.shortest_path_length(G_cost, orig_node, dest_node, weight="cost")

fig, ax = ox.plot.plot_graph(
    G,
    show=False,
    close=False,
    node_size=0,
    edge_color="lightgray",
    edge_linewidth=0.6,
    bgcolor="white"
)

ox.plot.plot_graph_route(
    G,
    shortest_route,
    ax=ax,
    route_color="blue",
    route_linewidth=4,
    show=False,
    close=False
)

ox.plot.plot_graph_route(
    G_cost,
    alternative_route,
    ax=ax,
    route_color="red",
    route_linewidth=4,
    show=False,
    close=False
)

for _, row in places.iterrows():
    if row["risk_score"] >= 0.8:
        color = "red"
    elif row["risk_score"] >= 0.5:
        color = "orange"
    else:
        color = "green"

    ax.scatter(
        row["lon"],
        row["lat"],
        c=color,
        s=120,
        zorder=5
    )
    ax.text(
        row["lon"] + 0.0002,
        row["lat"] + 0.0002,
        row["name"],
        fontsize=9,
        zorder=6
    )

print("Tuyến ngắn nhất theo length:")
print(shortest_route)
print("Tổng chiều dài:", round(shortest_length, 2), "m")

print("\nTuyến thay thế tránh khu vực nguy cơ cao:")
print(alternative_route)
print("Tổng chi phí:", round(alternative_length, 2), "m-equivalent")

