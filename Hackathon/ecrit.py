import json
from random import randint, uniform
donnee, arretbus=[], []
# Modèle de données
with open('Hackathon/données/arrets.json', 'r') as file:
    arrets = json.load(file)
arretlat, arretlon = [], []
for i in range(len(arrets)):
    arretlat.append(arrets[i]["coordinates"]["lat"])
    arretlon.append(arrets[i]["coordinates"]["lon"])
j=randint(0,len(arretlat))
arretbus.append(arrets[j]["name"])
data = {
    "Nombre_gens":{ "Entree":randint(0,60) , "Sortie": 0},
    "Places_bus": 50,
    "GPS":{"Latitude":arretlat[j] , "Longitude": arretlon[j]},
    "BUS_ID":{"ID":1, "ligne":1},
    "Horaire":{"date": "2021-06-01", "heure": "12:00"}
}
# Écriture des données dans un fichier JSON
with open('Hackathon/données/donneeprovi.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)
donnee.append(data)

for i in range(5):    
    data={}
    with open('Hackathon/données/donneeprovi.json', 'r') as json_file:
        recup = json.load(json_file)
    entree=recup["Nombre_gens"]["Entree"]
    sortie=recup["Nombre_gens"]["Sortie"]
    placerestante=60-(entree-sortie)
    heure=recup["Horaire"]["heure"]
    splitheure=heure.split(":")
    minute=int(splitheure[1])+5
    heure=int(splitheure[0])
    if minute>=60:
        heure+=1
        minute=0
    nouvheure=str(heure)+":"+str(minute)
    j=randint(0,len(arretlat))
    arretbus.append(arrets[j]["name"])
#    print(f'entrée {entree}, sortie {sortie}, placerestante {placerestante}')
    if placerestante!=0:
        data = {
        "Nombre_gens":{ "Entree":randint(entree,entree+placerestante) , "Sortie": randint(sortie,entree)},
        "Places_bus": 60,
        "GPS":{"Latitude":arretlat[j] , "Longitude": arretlon[j]},
        "BUS_ID":{"ID":1, "ligne":1},
        "Horaire":{"date": "2021-06-01", "heure": nouvheure}
}
    else:
        data = {
        "Nombre_gens":{ "Entree":entree , "Sortie": randint(0,60)},
        "Places_bus": 60,
        "GPS":{"Latitude":arretlat[j], "Longitude": arretlon[j]},
        "BUS_ID":{"ID":1, "ligne":1},
        "Horaire":{"date": "2021-06-01", "heure": nouvheure}
    }
    with open('Hackathon/données/donneeprovi.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    donnee.append(data)
with open('Hackathon/données/donnee.json', 'w') as json_file:
    json.dump(donnee, json_file, indent=4)
with open('Hackathon/données/trajets.json', 'w') as json_file:  
    json.dump(arretbus, json_file, indent=4)





print("Le fichier donnee.json a été créé avec succès.")

