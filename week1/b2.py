from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import folium
geolocator = Nominatim(user_agent="geoapi", timeout = 10)
trung_tam = "Trường Đại học Kinh Tế cơ sở B, TP.HCM"
trung_tam_loca = geolocator.geocode(trung_tam)
trung_tam_vitri = (trung_tam_loca.latitude, trung_tam_loca.longitude)
noi = [
    "Landmark 81, HCM",
    "Bitexco Financial Tower, HCM",
    "Công viên 23 Tháng 9, HCM",
    "Bảo tàng Chứng tích Chiến tranh, HCM",
    "Chợ An Đông, HCM",
    "Bến Nhà Rồng, HCM",
    "AEON Mall Tân Phú, HCM",
    "Crescent Mall, HCM",
    "Bệnh viện Chợ Rẫy, HCM",
    "Nhà hát Thành phố, HCM"
]
m = folium.Map(location = trung_tam_vitri, zoom_start = 17)
folium.Marker(location = trung_tam_vitri, popup ="UEH cơ sở B").add_to(m)
for i in noi:
  try:
    vitri = geolocator.geocode(i)
    diachi = (vitri.latitude, vitri.longitude)
    khoangcach = geodesic(trung_tam_vitri, diachi).km

    folium.Marker(location = diachi, popup =f"{i} cách UEH cơ sở B {khoangcach:.2f} km").add_to(m)
  except:
    print("lỗi")
m