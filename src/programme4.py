import matplotlib.pyplot as plt
import os
from collections import defaultdict
from datetime import datetime
# Changement des imports relatifs en imports absolus
from programme3 import extract_r107_sessions
from programme2 import parse_ics_calendar

def count_sessions_by_month(sessions):
    """Compte le nombre de séances TP par mois"""
    monthly_counts = defaultdict(int)
    
    for date_str, _, type_seance in sessions:
        if type_seance == "TP":
            date = datetime.strptime(date_str, '%d-%m-%Y')
            month = date.strftime('%B %Y')  # nom du mois et année
            monthly_counts[month] += 1
    
    return monthly_counts

def create_bar_chart(monthly_counts):
    """Crée un diagramme en bâtons des séances par mois"""
    plt.figure(figsize=(10, 6))
    
    months = list(monthly_counts.keys())
    counts = list(monthly_counts.values())
    
    # Création du diagramme en bâtons
    bars = plt.bar(months, counts, color='skyblue')
    
    # Personnalisation du graphique
    plt.title('Nombre de séances TP de R1.07 par mois')
    plt.xlabel('Mois')
    plt.ylabel('Nombre de séances')
    
    # Rotation des labels de l'axe x pour une meilleure lisibilité
    plt.xticks(rotation=45, ha='right')
    
    # Ajout des valeurs sur les barres
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom')
    
    # Ajustement automatique de la mise en page
    plt.tight_layout()
    
    # Sauvegarde dans le dossier output
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'r107_sessions_bar.png')
    plt.savefig(output_path)
    plt.close()  # Ferme la figure pour libérer la mémoire

def create_pie_chart(monthly_counts):
    """Crée un diagramme circulaire des séances par mois"""
    plt.figure(figsize=(8, 8))
    
    # Création du diagramme circulaire
    plt.pie(monthly_counts.values(), 
            labels=monthly_counts.keys(),
            autopct='%1.1f%%',
            startangle=90)
    
    plt.title('Répartition des séances TP de R1.07 par mois')
    
    # Ajustement automatique de la mise en page
    plt.axis('equal')
    plt.tight_layout()
    
    # Sauvegarde dans le dossier output
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'r107_sessions_pie.png')
    plt.savefig(output_path)
    plt.close()  # Ferme la figure pour libérer la mémoire

if __name__ == "__main__":
    try:
        # Définition des chemins
        base_dir = os.path.dirname(os.path.dirname(__file__))
        input_path = os.path.join(base_dir, 'data', 'ADE_RT1_Septembre2023_Decembre2023.ics')
        
        # Chargement et analyse du calendrier
        calendar_data = parse_ics_calendar(input_path)
        
        # Extraction des séances R1.07 pour le groupe TP A1
        sessions = extract_r107_sessions(calendar_data, "RT1-TP A1")
        
        # Comptage des séances par mois
        monthly_counts = count_sessions_by_month(sessions)
        
        # Création des visualisations
        create_bar_chart(monthly_counts)
        create_pie_chart(monthly_counts)
        
        print("Les graphiques ont été sauvegardés avec succès dans le dossier output!")
    except Exception as e:
        print(f"Erreur lors de la génération des graphiques: {str(e)}")