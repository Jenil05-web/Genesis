from src.tools.maps_tool import geocode, find_nearest_shelter

geo = geocode("Assam, India")
print(geo)
print(find_nearest_shelter(geo["lat"], geo["lon"]))