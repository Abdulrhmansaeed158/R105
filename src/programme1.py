import re
import os
from datetime import datetime

def parse_datetime(dt_string):
    """Parse une date/heure au format ICS vers le format demandé"""
    # Enlever le Z et le T
    dt_string = dt_string.rstrip('Z')
    date_part = dt_string[:8]
    time_part = dt_string[9:] if 'T' in dt_string else '000000'
    
    # Parser avec datetime
    dt = datetime.strptime(date_part + time_part, '%Y%m%d%H%M%S')
    
    # Formatter selon le format demandé
    return dt.strftime('%d-%m-%Y'), dt.strftime('%H:%M')

def get_duration(start_dt, end_dt):
    """Calcule la durée entre deux dates au format ICS"""
    start = datetime.strptime(start_dt.rstrip('Z'), '%Y%m%dT%H%M%S')
    end = datetime.strptime(end_dt.rstrip('Z'), '%Y%m%dT%H%M%S')
    duration = end - start
    hours = duration.seconds//3600
    minutes = (duration.seconds//60)%60
    return f"{hours:02d}:{minutes:02d}"

def parse_ics_event(filename):
    """Parse un fichier ICS contenant un seul événement et retourne le format CSV demandé"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraction des champs nécessaires avec gestion des erreurs
    try:
        uid = re.search(r'UID:(.*?)\n', content).group(1)
        dtstart = re.search(r'DTSTART:(.*?)\n', content).group(1)
        dtend = re.search(r'DTEND:(.*?)\n', content).group(1)
        summary = re.search(r'SUMMARY:(.*?)\n', content).group(1)
        location = re.search(r'LOCATION:(.*?)\n', content).group(1)
        description = re.search(r'DESCRIPTION:\\n\\n(.*?)\\n', content).group(1)
    except AttributeError as e:
        raise ValueError(f"Format de fichier ICS invalide: champ manquant. {str(e)}")

    # Parsing de la date et l'heure
    date, heure = parse_datetime(dtstart)
    
    # Calcul de la durée
    duree = get_duration(dtstart, dtend)
    
    # Détermination de la modalité
    modalite = "CM"
    if "TD" in summary or "-TD" in description:
        modalite = "TD"
    elif "TP" in summary or "-TP" in description:
        modalite = "TP"

    # Extraction des professeurs et groupes depuis la description
    profs = []
    groupes = []
    desc_parts = description.split('\\n')
    for part in desc_parts:
        if part.startswith('RT1-'):
            groupes.append(part.strip())
        elif part and not part.startswith('('):
            profs.append(part.strip())

    # Formatage du résultat CSV
    result = f"{uid};{date};{heure};{duree};{modalite};{summary};"
    result += f"{location};{('|'.join(profs) if profs else 'vide')};{('|'.join(groupes) if groupes else 'vide')}"
    
    return result

if __name__ == "__main__":
    # Définition des chemins
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_file = os.path.join(base_dir, 'data', 'evenementSAE_15GroupeA1.ics')
    
    try:
        # Test avec le fichier exemple
        result = parse_ics_event(input_file)
        print("Résultat au format CSV:")
        print(result)
    except Exception as e:
        print(f"Erreur lors du traitement du fichier: {str(e)}")