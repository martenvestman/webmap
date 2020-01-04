import folium
from folium.plugins import FastMarkerCluster
import pandas

data = pandas.read_csv("poi.txt")

title = list(data["TITLE"])
desc = list(data["DESC"])
lat = list(data["LAT"])
lon = list(data["LON"])


def color_producer(t):
    if t == 'Stugan':
        return 'red'
    elif t == "Affärn":
        return 'green'
    elif t == "Gammelgårn":
        return 'blue'
    elif t == 'Saan' or t == 'Långnäse':
        return 'gray'
    elif t == 'Fäboern':
        return 'beige'
    else:
        return 'orange'

html="""
    <h4> %s</h4>
    %s
    """


map = folium.Map(location=[63.568886, 17.616050], zoom_start=12, tiles="Stamen Terrain")
fg = folium.FeatureGroup(name="My Map")

fgm = folium.FeatureGroup(name='Msjö')

for tit, dsc, lt, ln in zip(title, desc,  lat, lon):
    iframe = folium.IFrame(html=html % (tit, dsc), width=100, height=85)
    fgm.add_child(folium.Marker(location=(lt, ln), radius = 6, popup=folium.Popup(iframe),
                                     icon=folium.Icon(color=color_producer(tit))))

fgp = folium.FeatureGroup(name='Population')

fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
                            style_function=lambda x: {'fillColor': 'yellow' if x['properties']['POP2005'] < 10000000
                            else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))


map.add_child(fgm)
map.add_child(fgp)
map.add_child(folium.LayerControl())


map.save("Map1.html")
