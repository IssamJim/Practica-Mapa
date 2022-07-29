import folium
import pandas

data = pandas.read_excel("parquesyjardines1.xlsx", sheet_name = 0)
lat = list(data["Lat"])
lon = list(data["Lon"])
dir = list(data["Dirección"])
pla = list(data["Plaza"])
sup = list(data["Superficie"])

data = pandas.read_csv("volcanoes.txt")
lat1 = list(data["LAT"])
lon1 = list(data["LON"])
elev = list(data["ELEV"])

html1 = """<h4>Volcano information:</h4>
Height: %s m
"""

def color_producer(superficie):
    if superficie < 960:
        return 'green'
    elif 960 <= superficie < 3350:
        return 'orange'
    else:
        return 'red'


map = folium.Map(location = [29, -111.30], zoom_start=10, tiles="Stamen Terrain")

fgvol = folium.FeatureGroup(name="Volcanoes")

for lt1, ln1, el in zip (lat1, lon1, elev):
    iframe = folium.IFrame(html=html1 % str(el), width=200, height=100)
    fgvol.add_child(folium.CircleMarker(location=[lt1,ln1], fill=True, fill_color=color_producer(el), color=color_producer(el), radius=8,
    popup=folium.Popup(iframe)))

fgp = folium.FeatureGroup(name="Parques")

for lt, ln, dr, pl, sp in zip(lat, lon, dir, pla, sup):
    fgp.add_child(folium.CircleMarker(location=[lt, ln], fill=True, fill_color=color_producer(sp), color=color_producer(sp), radius=8,
    popup="Plaza: " + str(pl) +  "\nDirección: " + str(dr) + "\nSuperficie: " + str(sp) + " m²"))

fgv = folium.FeatureGroup(name="Population")


fgv.add_child(folium.GeoJson(data=open(file='world.json', mode='r', encoding='utf-8-sig').read(),
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x ['properties']['POP2005'] < 20000000 else 'red'}))


map.add_child(fgv)
map.add_child(fgp)
map.add_child(fgvol)

map.add_child(folium.LayerControl())

map.save("Map1.html")
