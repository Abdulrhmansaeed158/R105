import re

def lire_fichier_ics(nom_fichier):
    with open(nom_fichier, 'r') as fichier:
        contenu = fichier.read()
    return contenu

def extraire_evenement(contenu):
    evenement = {}
    evenement['DTSTAMP'] = re.search(r'DTSTAMP:(.*)', contenu).group(1)
    evenement['DTSTART'] = re.search(r'DTSTART:(.*)', contenu).group(1)
    evenement['DTEND'] = re.search(r'DTEND:(.*)', contenu).group(1)
    evenement['SUMMARY'] = re.search(r'SUMMARY:(.*)', contenu).group(1)
    evenement['LOCATION'] = re.search(r'LOCATION:(.*)', contenu).group(1)
    evenement['DESCRIPTION'] = re.search(r'DESCRIPTION:(.*)', contenu).group(1).replace('\\n', '\n')
    evenement['UID'] = re.search(r'UID:(.*)', contenu).group(1)
    evenement['CREATED'] = re.search(r'CREATED:(.*)', contenu).group(1)
    evenement['LAST-MODIFIED'] = re.search(r'LAST-MODIFIED:(.*)', contenu).group(1)
    evenement['SEQUENCE'] = re.search(r'SEQUENCE:(.*)', contenu).group(1)
    return evenement

def convertir_en_csv(evenement):
    uid = evenement['UID']
    date = evenement['DTSTART'][:8]
    heure = evenement['DTSTART'][9:13]
    duree = evenement['DTEND'][9:13]
    modalite = "CM"  # Vous pouvez ajuster cette valeur selon vos besoins
    intitule = evenement['SUMMARY']
    salle = evenement['LOCATION']
    prof = evenement['DESCRIPTION'].split('\n')[2]
    groupe = evenement['DESCRIPTION'].split('\n')[1]
    
    date_formatee = f"{date[6:8]}-{date[4:6]}-{date[:4]}"
    heure_formatee = f"{heure[:2]}:{heure[2:]}"
    duree_formatee = f"{int(duree[:2]) - int(heure[:2]):02}:{int(duree[2:]) - int(heure[2:]):02}"
    
    csv = f"{uid};{date_formatee};{heure_formatee};{duree_formatee};{modalite};{intitule};{salle};{prof};{groupe}"
    return csv

def main():
    nom_fichier = 'evenementSAE_15.ics'
    contenu = lire_fichier_ics(nom_fichier)
    evenement = extraire_evenement(contenu)
    csv = convertir_en_csv(evenement)
    print(csv)

if __name__ == "__main__":
    main()
