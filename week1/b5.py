import folium
trungtam = (10.7618679,106.6676306)
m = folium.Map(location = trungtam, zoom_start = 13)
folium.Marker(trungtam, popup = "UEH", tooltip = "University of Economics").add_to(m)
for radi, co in [(3000, "green"),(5000,"red")]:
  folium.Circle(location = trungtam, radius = radi, color = co, fill = True).add_to(m)
m