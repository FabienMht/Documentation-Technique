# Fabien mauhourat
from math import *

def distance (latvahic,longvehic,latant,longant):
    latvahic, longvehic, latant, longant = map(radians, [latvahic, longvehic, latant, longant])
    return 6371 * acos(sin(latvahic) * sin(latant) + cos(latvahic) * cos(latant) * cos(longvehic - longant))

# Ouverture du fichier et lecture des lignes
fileantenne=open("antenne", mode='r')
fileevents=open("events", mode='r')
lineficantenne=fileantenne.readlines()
lineficevents=fileevents.readlines()

for lineev in lineficevents:
    linevehic=lineev.split(";")
    tabvehic = []
    dicant={}
    tabant=[]
    tabvehic.append(int(linevehic[7]))
    tabvehic.append(float(linevehic[9]))
    tabvehic.append(float(linevehic[10]))

    for linefican in lineficantenne:
        lineant=linefican.split(",")
        macaddress=lineant[1].replace(" ","")

        if ":" in lineant[0]:
            timestamp = int(lineant[0].split(":")[1])
        else:
            timestamp = int(lineant[0])

        if timestamp > tabvehic[0] and timestamp < tabvehic[0] + 9:
            dicant[macaddress]=[float(lineant[7]),float(lineant[8])]

    print(tabvehic[0],"avec timestamp",end=" : ")
    count = 0
    for mac in dicant.keys():
        count+=1
        if count!=len(dicant.keys()):
            print(mac,end=", ")
        else:
            print(mac)

    for mac in dicant.keys():
        if distance(tabvehic[1],tabvehic[2],dicant[mac][0],dicant[mac][1]) < 300:
            tabant.append(mac)

    print(tabvehic[0], "avec timestamp + long/lat", end=" : ")
    count = 0
    for mac in tabant:
        count += 1
        if count != len(tabant):
            print(mac, end=", ")
        else:
            print(mac)

fileantenne.close()
fileevents.close()