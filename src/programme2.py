import re
import os
from datetime import datetime
# Changement de l'import relatif en import absolu
from programme1 import parse_datetime, get_duration

def extract_events(calendar_content):
    """Extrait tous les événements d'un calendrier ICS"""
    event_pattern = r'BEGIN:VEVENT(.*?)END:VEVENT'
    events = re.finditer(event_pattern, calendar_content, re.DOTALL)
    return [event.group(1).strip() for event in events]

def parse_event(event_content):
    """Parse un événement ICS individuel"""
    try:
        # Extraction des champs obligatoires
        uid = re.search(r'UID:(.*?)\n', event_content).group(1)
        dtstart = re.search(r'DTSTART:(.*?)\n', event_content).group(1)
        dtend = re.search(r'DTEND:(.*?)\n', event_content).group(1)
        summary = re.search(r'SUMMARY:(.*?)\n', event_content).group(1)
        
        # Extraction des champs optionnels
        location_match = re.search(r'LOCATION:(.*?)\n', event_content)
        location = location_match.group(1) if location_match else "vide"
        
        description_match = re.search(r'DESCRIPTION:\\n\\n(.*?)\\n', event_content)
        description = description_match.group(1) if description_match else ""
    except AttributeError as e:
        print(f"Warning: Event skipped due to missing required field - {str(e)}")
        return None

    # Parsing de la date et l'heure
    date, heure = parse_datetime(dtstart)
    duree = get_duration(dtstart, dtend)
    
    # Détermination de la modalité
    modalite = "CM"
    if "TD" in summary or "-TD" in description:
        modalite = "TD"
    elif "TP" in summary or "-TP" in description:
        modalite = "TP"
    elif "DS" in summary:
        modalite = "DS"
    elif "Proj" in summary:
        modalite = "Proj"

    # Traitement des salles multiples
    salles = location.split(',') if ',' in location else [location]
    salles_str = '|'.join(s.strip() for s in salles if s.strip())
    
    # Extraction des professeurs et groupes depuis la description
    profs = []
    groupes = []
    if description:
        desc_parts = description.split('\\n')
        for part in desc_parts:
            if part.startswith('RT1-'):
                groupes.append(part.strip())
            elif part and not part.startswith('('):
                profs.append(part.strip())
    
    # Formatage du résultat CSV
    result = f"{uid};{date};{heure};{duree};{modalite};{summary};"
    result += f"{salles_str if salles_str else 'vide'};"
    result += f"{('|'.join(profs) if profs else 'vide')};"
    result += f"{('|'.join(groupes) if groupes else 'vide')}"
    
    return result

def parse_ics_calendar(filename):
    """Parse un fichier ICS de calendrier complet et retourne un tableau d'événements au format CSV"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extraction et parsing de chaque événement
        events = extract_events(content)
        results = []
        
        for event in events:
            parsed_event = parse_event(event)
            if parsed_event:  # Ignore les événements mal formés
                results.append(parsed_event)
        
        return results
    
    except FileNotFoundError:
        raise FileNotFoundError(f"Le fichier {filename} n'a pas été trouvé.")
    except Exception as e:
        raise Exception(f"Erreur lors du traitement du fichier: {str(e)}")

if __name__ == "__main__":
    # Définition des chemins
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_file = os.path.join(base_dir, 'data', 'ADE_RT1_Septembre2023_Decembre2023.ics')
    
    try:
        # Test avec le fichier exemple
        results = parse_ics_calendar(input_file)
        print(f"Nombre d'événements traités: {len(results)}")
        print("\nPremiers événements au format CSV:")
        for result in results[:5]:  # Affiche les 5 premiers événements
            print(result)
            print("-" * 80)
    except Exception as e:
        print(f"Erreur: {str(e)}")