from datetime import datetime
import os
# Changement de l'import relatif en import absolu
from programme2 import parse_ics_calendar

def extract_r107_sessions(calendar_data, tp_group="RT1-TP A1"):
    """
    Extrait les séances de R1.07 pour un groupe de TP spécifique
    Retourne une liste de tuples (date, durée, type)
    """
    r107_sessions = []
    
    for event in calendar_data:
        # Découpage des champs du CSV
        fields = event.split(';')
        if len(fields) < 9:  # Vérification du format
            continue
            
        summary = fields[5]
        groups = fields[8]
        
        # Vérifie si c'est un cours de R1.07 pour le bon groupe
        if "R1.07" in summary and (tp_group in groups or "RT1-S1" in groups):
            date = fields[1]
            duree = fields[3]
            type_seance = fields[4]
            
            r107_sessions.append({
                'date': datetime.strptime(date, '%d-%m-%Y'),  # Pour le tri
                'date_str': date,
                'duree': duree,
                'type': type_seance
            })
    
    # Tri des séances par date
    r107_sessions.sort(key=lambda x: x['date'])
    
    # Conversion en liste de tuples avec le format demandé
    return [(session['date_str'], session['duree'], session['type']) 
            for session in r107_sessions]

def format_table(sessions):
    """Formate les sessions en tableau pour affichage"""
    if not sessions:
        return "Aucune séance trouvée."
        
    header = "| Date | Durée | Type |\n"
    separator = "|------|--------|------|\n"
    
    rows = [f"| {date} | {duree} | {type_} |" 
            for date, duree, type_ in sessions]
    
    return header + separator + "\n".join(rows)

if __name__ == "__main__":
    # Chargement et analyse du calendrier
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_path = os.path.join(base_dir, 'data', 'ADE_RT1_Septembre2023_Decembre2023.ics')
    
    calendar_data = parse_ics_calendar(input_path)
    
    # Extraction des séances R1.07 pour le groupe TP A1
    sessions = extract_r107_sessions(calendar_data, "RT1-TP A1")
    
    # Affichage des résultats
    print("Séances de R1.07 pour le groupe TP A1:")
    print(format_table(sessions))