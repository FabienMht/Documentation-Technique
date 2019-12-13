# Fabien Mauhourat

# Fonctions qui initialise le dictionnaire pour une adresse mac donnée
def init_dictionnary (dic,addr,error):

    if addr not in dic:
        dic[addr] = {}
        dic[addr][error] = 0

    if error not in dic[addr]:
        dic[addr][error] = 0

# Variables
mac={}

# Ouverture du fichier et lecture des lignes
file=open("PCapDecode.csv", mode='r')
linefic=file.readlines()

# Remplissage du dictionnaire
# Séparateur de ligne : ";"
# Séparateur de champ : ","
for line in linefic:
    line=line.split(";")
    line.__delitem__(-1)

    for tab in line:
        tab=tab.split(",")
        macaddress=tab[1].replace(" ","")

        if 2 in range(0, len(tab)) and (tab[2] == "61" or tab[2] == "62"):
            init_dictionnary(mac, macaddress, tab[2])
            mac[macaddress][tab[2]] += 1

        if 3 in range(0, len(tab)) and tab[3] == "2":
            init_dictionnary(mac,macaddress,tab[3])
            mac[macaddress][tab[3]]+=1

        if 4 in range(0, len(tab)) and (tab[4] == "66" or tab[4] == "65" or tab[4] == "67" or tab[4] == "94"):
            init_dictionnary(mac, macaddress, tab[4])
            mac[macaddress][tab[4]] += 1

        if 9 in range(0, len(tab)) and tab[9] == "84":
            init_dictionnary(mac, macaddress, tab[9])
            mac[macaddress][tab[9]] += 1

        if 10 in range(0, len(tab)) and (tab[10] == "86" or tab[10] == "87" or tab[10] == "88" or tab[10] == "89" or tab[10] == "90" or tab[10] == "91" or tab[10] == "92"):
            init_dictionnary(mac, macaddress, tab[10])
            mac[macaddress][tab[10]] += 1

file.close()

# Affichage des résultats
for mac,errors in mac.items():
    print ("'"+mac+"'",end=" : ")
    count=0

    for valeur in errors:
        count+=1

        if count!=len(errors):
            print("'"+valeur+"'",errors[valeur],sep=" : ",end=", ")
        else:
            print("'" + valeur + "'", errors[valeur], sep=" : ", end="")

    print()


