import folium
from folium.plugins import HeatMap
import pandas as pd

data = pd.DataFrame({
    "lat": [10.7626, 10.7630, 10.7615, 10.7640, 10.7608],
    "lon": [106.6821, 106.6815, 106.6832, 106.6840, 106.6805]
})

m = folium.Map(location=[10.7626, 106.6821], zoom_start=14)
HeatMap(data[["lat", "lon"]].values.tolist()).add_to(m)

m