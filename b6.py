import osmnx as ox
import matplotlib.pyplot as plt

place = "District 1, Ho Chi Minh City, Vietnam"
G = ox.graph_from_place(place, network_type="drive")
thong_ke = ox.basic_stats(G)
print("Số lượng nút giao thông:", thong_ke['n'])
print("Tổng chiều dài các con đường (mét):", thong_ke['street_length_total'])

# 3. Vẽ trực tiếp đồ thị đường xá lên màn hình
ox.plot_graph(G)