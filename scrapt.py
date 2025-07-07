import wikipediaapi

# Initialisation de l'API Wikipedia
wiki = wikipediaapi.Wikipedia(
    language='fr',
    user_agent='https://meta.wikimedia.org/wiki/User-Agent_policy'
)

# Page à scraper
page_name = "Histoire de France"
page = wiki.page(page_name)

# Vérification de l'existence de la page et écriture dans un fichier
if page.exists():
    madagascar_details = page.text  # Récupération du texte complet
    file_path = "madagascar_wikipedia.txt"  # Nom du fichier de sortie

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(madagascar_details)  # Écrire le contenu complet dans le fichier

    print(f"Le contenu de la page Wikipedia sur '{page_name}' a été sauvegardé dans '{file_path}'.")
else:
    print(f"La page '{page_name}' n'existe pas.")

