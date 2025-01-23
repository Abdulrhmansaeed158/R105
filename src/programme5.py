import markdown
import os
# Changement des imports relatifs en imports absolus
from programme2 import parse_ics_calendar
from programme3 import extract_r107_sessions, format_table
from programme4 import count_sessions_by_month, create_bar_chart, create_pie_chart

def generate_markdown_report(sessions, monthly_counts):
    """Génère le contenu du rapport en format Markdown"""
    markdown_content = """
# Rapport d'analyse des séances R1.07

## Tableau des séances

Voici la liste complète des séances R1.07 pour le groupe TP A1 :

{}

## Analyse statistique

### Répartition mensuelle des séances TP

Nombre de séances TP par mois :

{}

## Visualisations

### Diagramme en bâtons
![Diagramme en bâtons des séances par mois](r107_sessions_bar.png)

### Diagramme circulaire
![Diagramme circulaire des séances par mois](r107_sessions_pie.png)
""".format(
        format_table(sessions),
        "\n".join([f"- {month}: {count} séances" for month, count in monthly_counts.items()])
    )
    
    return markdown_content

def generate_html_report(markdown_content):
    """Convertit le contenu Markdown en HTML avec un style CSS basique"""
    # HTML template avec CSS intégré
    html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Rapport R1.07</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        img {
            max-width: 100%;
            height: auto;
            margin: 20px 0;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
        h1, h2, h3 {
            color: #333;
        }
    </style>
</head>
<body>
    {}
</body>
</html>
"""
    
    # Conversion du Markdown en HTML
    html_content = markdown.markdown(markdown_content, extensions=['tables'])
    
    # Insertion du HTML dans le template
    return html_template.format(html_content)

if __name__ == "__main__":
    try:
        # Définition des chemins
        base_dir = os.path.dirname(os.path.dirname(__file__))
        input_path = os.path.join(base_dir, 'data', 'ADE_RT1_Septembre2023_Decembre2023.ics')
        output_dir = os.path.join(base_dir, 'output')
        
        # Chargement et analyse du calendrier
        calendar_data = parse_ics_calendar(input_path)
        
        # Extraction des données
        sessions = extract_r107_sessions(calendar_data, "RT1-TP A1")
        monthly_counts = count_sessions_by_month(sessions)
        
        # Génération des graphiques
        create_bar_chart(monthly_counts)
        create_pie_chart(monthly_counts)
        
        # Génération du rapport
        markdown_content = generate_markdown_report(sessions, monthly_counts)
        html_content = generate_html_report(markdown_content)
        
        # Sauvegarde du rapport
        output_path = os.path.join(output_dir, 'rapport_r107.html')
        
        # Assure que le dossier output existe
        os.makedirs(output_dir, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("Le rapport HTML a été généré avec succès dans le dossier output!")
        
    except Exception as e:
        print(f"Erreur lors de la génération du rapport: {str(e)}")