import folium
m = folium.Map(location = [10.7610532,106.6657831],zoom_start = 16)
folium.Marker([10.7610532,106.6657831], popup="UEH", tooltip = "University of Economics").add_to(m)
vi_tri = [("Bệnh viện", "Bệnh viện chợ rẫy", 10.7578646,106.6569382),
          ("Trung tâm thương mại", "Coop mart lý thường kiệt", 10.7596967,106.6587978),
          ("Trường học", "Trường kinh tế công nghệ", 10.7604347,106.6684828),
          ("Bến xe","Tuyến xe", 10.7611942,106.6687336),
          ("Văn phòng", "Văn phòng kinh tế văn hóa Đài Bắc", 10.7621171,106.6677278)]
for name, tool, lat, lon in vi_tri:
  folium.Marker([lat,lon], popup = name, tooltip = tool).add_to(m)
m