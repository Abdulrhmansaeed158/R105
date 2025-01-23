import os
import sys
import subprocess
import pkg_resources
import shutil

class ProjectSetup:
    def __init__(self):
        # Définition des chemins absolus
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.src_dir = os.path.join(self.base_dir, 'src')
        self.data_dir = os.path.join(self.base_dir, 'data')
        self.output_dir = os.path.join(self.base_dir, 'output')
        
        # Ajout du dossier src au PYTHONPATH
        sys.path.insert(0, self.src_dir)
        
        # Création de la structure des dossiers
        self.create_directory_structure()

    def create_directory_structure(self):
        """Crée la structure des dossiers nécessaires"""
        for directory in [self.src_dir, self.data_dir, self.output_dir]:
            os.makedirs(directory, exist_ok=True)

    def check_and_install_dependencies(self):
        """Vérifie et installe les dépendances requises"""
        required_packages = {
            'matplotlib': '3.8.2',
            'markdown': '3.5.1'
        }
        
        for package, version in required_packages.items():
            try:
                pkg_resources.require(f"{package}=={version}")
                print(f"✓ {package} {version} est déjà installé")
            except (pkg_resources.VersionConflict, pkg_resources.DistributionNotFound):
                print(f"Installation de {package} {version}...")
                subprocess.check_call([
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    f"{package}=={version}"
                ])

    def check_input_files(self):
        """Vérifie la présence des fichiers d'entrée nécessaires"""
        required_files = [
            ('evenementSAE_15GroupeA1.ics', os.path.join(self.data_dir, 'evenementSAE_15.ics')),
            ('ADE_RT1_Septembre2023_Decembre2023.ics', os.path.join(self.data_dir, 'ADE_RT1_Septembre2023_Decembre2023.ics'))
        ]
        
        all_present = True
        for filename, filepath in required_files:
            if not os.path.exists(filepath):
                print(f"✗ Fichier manquant: {filename}")
                all_present = False
        
        return all_present

    def clean_output_directory(self):
        """Nettoie le dossier de sortie"""
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir)

    def execute_programs(self):
        """Exécute les programmes dans l'ordre"""
        # Liste des programmes à exécuter
        programs = [
            ('programme1.py', "Traitement d'un événement unique"),
            ('programme2.py', "Traitement du calendrier complet"),
            ('programme3.py', "Extraction des séances R1.07"),
            ('programme4.py', "Génération des visualisations"),
            ('programme5.py', "Génération du rapport final")
        ]

        # Change le répertoire de travail vers src
        original_dir = os.getcwd()
        os.chdir(self.src_dir)

        try:
            # Définit les variables d'environnement pour les chemins
            os.environ['PROJECT_DATA_DIR'] = self.data_dir
            os.environ['PROJECT_OUTPUT_DIR'] = self.output_dir

            for program_file, description in programs:
                print(f"\n=== {description} ===")
                program_path = os.path.join(self.src_dir, program_file)
                try:
                    # Exécute le programme comme un sous-processus
                    subprocess.run([sys.executable, program_path], check=True)
                    print(f"✓ {program_file} exécuté avec succès")
                except subprocess.CalledProcessError as e:
                    print(f"✗ Erreur lors de l'exécution de {program_file}:")
                    print(f"  {str(e)}")
                    return False
        finally:
            # Restaure le répertoire de travail original
            os.chdir(original_dir)

        return True

    def check_output_files(self):
        """Vérifie la présence des fichiers de sortie"""
        expected_files = [
            'r107_sessions_bar.png',
            'r107_sessions_pie.png',
            'rapport_r107.html'
        ]
        
        missing_files = []
        for filename in expected_files:
            filepath = os.path.join(self.output_dir, filename)
            if not os.path.exists(filepath):
                missing_files.append(filename)
        
        return missing_files

def main():
    print("=== Démarrage de l'exécution du projet SAÉ 1.5 ===\n")
    
    setup = ProjectSetup()
    
    # Vérification et installation des dépendances
    print("Vérification des dépendances...")
    setup.check_and_install_dependencies()
    
    # Vérification des fichiers d'entrée
    print("\nVérification des fichiers d'entrée...")
    if not setup.check_input_files():
        print("\n⚠ Des fichiers d'entrée sont manquants. Veuillez les placer dans le dossier 'data'.")
        return
    
    # Nettoyage du dossier de sortie
    print("\nNettoyage du dossier de sortie...")
    setup.clean_output_directory()
    
    # Exécution des programmes
    if not setup.execute_programs():
        print("\n⚠ L'exécution s'est terminée avec des erreurs.")
        return
    
    # Vérification des fichiers de sortie
    missing_files = setup.check_output_files()
    if missing_files:
        print("\n⚠ Certains fichiers de sortie sont manquants:")
        for file in missing_files:
            print(f"✗ output/{file}")
    else:
        print("\n✓ Tous les fichiers ont été générés avec succès!")
        print("\nVous pouvez consulter les résultats dans le dossier 'output':")
        print("- r107_sessions_bar.png")
        print("- r107_sessions_pie.png")
        print("- rapport_r107.html")

if __name__ == "__main__":
    main()