import re

def lire_fichier_ics(nom_fichier):
    with open(nom_fichier, 'r') as fichier:
        contenu = fichier.read()
    return contenu

def extraire_evenements(contenu):
    # Trouver tous les événements dans le fichier ICS en utilisant une expression régulière
    evenements = []
    pattern = r'BEGIN:VEVENT(.*?)END:VEVENT'
    matchs = re.findall(pattern, contenu, re.DOTALL)

    # Extraire les informations de chaque événement
    for match in matchs:
        evenement = {}
        evenement['DTSTAMP'] = re.search(r'DTSTAMP:(.*)', match).group(1) if re.search(r'DTSTAMP:(.*)', match) else "vide"
        evenement['DTSTART'] = re.search(r'DTSTART:(.*)', match).group(1) if re.search(r'DTSTART:(.*)', match) else "vide"
        evenement['DTEND'] = re.search(r'DTEND:(.*)', match).group(1) if re.search(r'DTEND:(.*)', match) else "vide"
        evenement['SUMMARY'] = re.search(r'SUMMARY:(.*)', match).group(1) if re.search(r'SUMMARY:(.*)', match) else "vide"
        evenement['LOCATION'] = re.search(r'LOCATION:(.*)', match).group(1) if re.search(r'LOCATION:(.*)', match) else "vide"
        evenement['DESCRIPTION'] = re.search(r'DESCRIPTION:(.*)', match).group(1).replace('\\n', '\n') if re.search(r'DESCRIPTION:(.*)', match) else "vide"
        evenement['UID'] = re.search(r'UID:(.*)', match).group(1) if re.search(r'UID:(.*)', match) else "vide"
        evenement['CREATED'] = re.search(r'CREATED:(.*)', match).group(1) if re.search(r'CREATED:(.*)', match) else "vide"
        evenement['LAST-MODIFIED'] = re.search(r'LAST-MODIFIED:(.*)', match).group(1) if re.search(r'LAST-MODIFIED:(.*)', match) else "vide"
        evenement['SEQUENCE'] = re.search(r'SEQUENCE:(.*)', match).group(1) if re.search(r'SEQUENCE:(.*)', match) else "vide"
        
        evenements.append(evenement)
    
    return evenements

def convertir_en_csv(evenement):
    # Extraire et formater les informations de l'événement
    uid = evenement['UID']
    date = evenement['DTSTART'][:8]
    heure = evenement['DTSTART'][9:13]
    duree = evenement['DTEND'][9:13]
    modalite = "CM"  # Vous pouvez ajuster cette valeur selon vos besoins
    intitule = evenement['SUMMARY']
    salle = evenement['LOCATION']
    prof = evenement['DESCRIPTION'].split('\n')[2] if len(evenement['DESCRIPTION'].split('\n')) > 2 else "vide"
    groupe = evenement['DESCRIPTION'].split('\n')[1] if len(evenement['DESCRIPTION'].split('\n')) > 1 else "vide"
    
    date_formatee = f"{date[6:8]}-{date[4:6]}-{date[:4]}"
    heure_formatee = f"{heure[:2]}:{heure[2:]}"
    duree_formatee = f"{int(duree[:2]) - int(heure[:2]):02}:{int(duree[2:]) - int(heure[2:]):02}"
    
    # Création du format CSV
    csv = f"{uid};{date_formatee};{heure_formatee};{duree_formatee};{modalite};{intitule};{salle};{prof};{groupe}"
    return csv

def main():
    nom_fichier = 'ADE_RT1_Septembre2023_Decembre2023.ics'  # Remplacer par le chemin correct
    contenu = lire_fichier_ics(nom_fichier)
    evenements = extraire_evenements(contenu)

    # Convertir chaque événement en ligne CSV et les afficher
    for evenement in evenements:
        csv = convertir_en_csv(evenement)
        print(csv)

if __name__ == "__main__":
    main()
