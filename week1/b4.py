import geopandas as gpd
import numpy as np
url = "https://raw.githubusercontent.com/TungTh/tungth.github.io/master/data/vn-provinces.json"
gdf = gpd.read_file(url)
gdf['DonHang'] = np.random.randint(50, 500, size=len(gdf))
m = gdf.explore(column="DonHang", cmap="Oranges")
m