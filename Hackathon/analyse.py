import json
import matplotlib.pyplot as plt
import mplcursors
import matplotlib.image as mpimg 
from math import *

with open('Hackathon//données/donnee.json', 'r') as file:
    data = json.load(file)
with open('Hackathon/données/arrets.json', 'r') as file:
    arrets = json.load(file)
personne, temps, lat, lon, arretlat, arretlon, nom, distance, bus = [], [], [], [], [], [], [], [], []
with open('Hackathon/données/trajets.json', 'r') as file:
    lebus = json.load(file)
for i in range(len(data)):
    entree = data[i]["Nombre_gens"]["Entree"]
    sortie = data[i]["Nombre_gens"]["Sortie"]
    if entree - sortie >= data[i]["Places_bus"]:
        personne.append("plein")
    else:
        personne.append(entree - sortie)
    temps.append(data[i]["Horaire"]["heure"])

print(personne)

graph = []
for i in range(len(personne)):
    if personne[i] == "plein":
        graph.append(50)
    else:
        graph.append(personne[i])


fig, ax = plt.subplots()
plot = ax.scatter(temps, graph)  # Utilisation de scatter pour un nuage de points
ax.set_xlabel('Temps')
ax.set_ylabel('Nombre de personnes')
ax.set_title('Nombre de personnes dans le bus au fil du temps')
plt.xticks([temps[i] for i in range(len(temps)) if i % 5 == 0], rotation=45)
plt.tight_layout()

# Ajout du curseur interactif
cursor = mplcursors.cursor(plot, hover=True)
cursor.connect("add", lambda sel: sel.annotation.set_text(f'Temps: {temps[sel.index]}\nNombre de personnes: {graph[sel.index]}/60'))


plt.show()

#plan
for i in range(len(data)):
    lat.append(data[i]["GPS"]["Latitude"])
    lon.append(data[i]["GPS"]["Longitude"])
for i in range(len(lat)-1):
    latrad1 = lat[i] * pi / 180
    lonrad1 = lon[i] * pi / 180
    latrad2 = lat[i+1] * pi / 180
    lonrad2 = lon[i+1] * pi / 180
    distance.append(round(2*6371*asin(sqrt(sin((latrad1 - latrad2) / 2)**2 + cos(latrad1) * cos(latrad2) * sin((lonrad2 - lonrad1) / 2)**2)),2))
distance.append(0)
for i in range(len(arrets)):
    arretlat.append(arrets[i]["coordinates"]["lat"])
    arretlon.append(arrets[i]["coordinates"]["lon"])
    nom.append(arrets[i]["name"])
for i in range(len(lebus)):
    bus.append(lebus[i])
img=mpimg.imread('Hackathon/données/fond.png')
fig, ax = plt.subplots(figsize=(10,10))
ax.imshow(img, extent=[2.600175,4.176062,43.248829,43.94556])
plot,=ax.plot(lon,lat, label='Trajet du bus', color='blue')
scatter=ax.scatter(arretlon,arretlat,label='Arret', color='red') 
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.legend()
cursor = mplcursors.cursor(plot, hover=True)
cursor.connect("add", lambda sel: sel.annotation.set_text(f'Distance: {distance[int(sel.index)]} km \n Arrêts départ: {lebus[int(sel.index)]} \n Arrêts arrivée: {lebus[int(sel.index)+1]}'))
cursor.connect("add", lambda sel: sel.annotation.set_bbox(dict(facecolor='white', alpha=0.8, edgecolor='black', boxstyle='round,pad=0.5')))
cursor.connect("add", lambda sel: sel.annotation.set_zorder(10))
points_selectionnes = []
def onclick(event):
    if event.xdata is not None and event.ydata is not None:
        points_selectionnes.append((event.ydata, event.xdata))
        if len(points_selectionnes) == 2:
            lat1, lon1 = points_selectionnes[0]
            lat2, lon2 = points_selectionnes[1]
            latrad1 = lat1 * pi / 180
            lonrad1 = lon1 * pi / 180
            latrad2 = lat2 * pi / 180
            lonrad2 = lon2 * pi / 180
            distance = round(2*6371*asin(sqrt(sin((latrad1 - latrad2) / 2)**2 + cos(latrad1) * cos(latrad2) * sin((lonrad2 - lonrad1) / 2)**2)),2)
            annotation_actuelle = ax.annotate(f"Distance: {distance} km", xy=(lon2, lat2), xytext=(lon2+0.01, lat2+0.01),
                                    arrowprops=dict(facecolor='black', shrink=0.05),
                                    bbox=dict(facecolor='white', alpha=0.8, edgecolor='black', boxstyle='round,pad=0.5'))
            annotation_actuelle.set_zorder(15)
            plt.draw()
            print(f"Distance entre les points : {distance} km")
            points_selectionnes.clear()

fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()



