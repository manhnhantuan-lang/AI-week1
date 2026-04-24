import folium
import numpy as np
from sklearn.cluster import KMeans
toado_tt = [10.7769, 106.7009]
khach_hang = np.random.randn(150, 2) * 0.04 + toado_tt
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(khach_hang)

nhan_cum = kmeans.labels_
vi_tri_kho = kmeans.cluster_centers_
m = folium.Map(location=toado_tt, zoom_start=13)
danh_sach_mau = ['red', 'blue', 'green']
for i, diem in enumerate(khach_hang):
    folium.CircleMarker(
        diem,
        radius=4,
        color=danh_sach_mau[nhan_cum[i]],
        fill=True, fill_opacity=0.6
    ).add_to(m)
for i, tam_cum in enumerate(vi_tri_kho):
    folium.Marker(
        tam_cum,
        popup=f"VỊ TRÍ KHO HÀNG TỐI ƯU SỐ {i+1}",
        icon=folium.Icon(color=danh_sach_mau[i], icon='star')
    ).add_to(m)
m