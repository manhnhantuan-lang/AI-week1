import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

place_name = "District 1, Ho Chi Minh City, Vietnam"
print(f"Đang tải dữ liệu mạng lưới giao thông cho: {place_name}...")
G = ox.graph_from_place(place_name, network_type='drive')

origin_coord = (10.7725, 106.6980) 
dest_coord = (10.7876, 106.7052)   

orig_node = ox.distance.nearest_nodes(G, X=origin_coord[1], Y=origin_coord[0])
dest_node = ox.distance.nearest_nodes(G, X=dest_coord[1], Y=dest_coord[0])

print("Đang tính toán bằng Dijkstra...")
route_dijkstra = nx.shortest_path(G, orig_node, dest_node, weight='length')
length_dijkstra = nx.shortest_path_length(G, orig_node, dest_node, weight='length')
print(f"-> Quãng đường (Dijkstra): {length_dijkstra:.2f} mét")

print("Đang tính toán bằng A*...")
def haversine_heuristic(node1, node2):
    y1, x1 = G.nodes[node1]['y'], G.nodes[node1]['x']
    y2, x2 = G.nodes[node2]['y'], G.nodes[node2]['x']
    # Đã sửa lại thành great_circle cho chuẩn với OSMnx mới
    return ox.distance.great_circle(y1, x1, y2, x2)

route_astar = nx.astar_path(G, orig_node, dest_node, heuristic=haversine_heuristic, weight='length')
length_astar = nx.astar_path_length(G, orig_node, dest_node, heuristic=haversine_heuristic, weight='length')
print(f"-> Quãng đường (A*): {length_astar:.2f} mét")

print("Đang hiển thị bản đồ...")
fig, ax = ox.plot_graph_routes(
    G, 
    routes=[route_dijkstra, route_astar], 
    route_colors=['r', 'b'], 
    route_linewidth=4, 
    node_size=0,
    show=False,
    close=False
)

ax.set_title("So sánh tuyến đường: Dijkstra (Đỏ) và A* (Xanh dương)", fontsize=12)
plt.show()