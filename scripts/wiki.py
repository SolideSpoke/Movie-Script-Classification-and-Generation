import wikipediaapi
import re
import requests

def get_movie_synopsis(titre_film, langue='en'):
    """
    Récupère le synopsis d'un film depuis l'API Wikipédia.
    
    Args:
        titre_film (str): Le titre du film à rechercher
        langue (str): Code de langue pour Wikipédia (défaut: 'en' pour anglais)
        
    Returns:
        str: Le synopsis du film ou un message d'erreur
    """
    # Initialiser l'API Wikipédia avec un user-agent approprié
    wiki = wikipediaapi.Wikipedia(
        language=langue,
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent='SynopsisFilmScript/1.0 (contact@example.com)'
    )
    
    try:
        # Rechercher la page
        page = wiki.page(titre_film)
        
        # Vérifier si la page existe
        if not page.exists():
            return None
        
        # Récupérer toutes les sections
        sections = page.sections
        
        # Chercher une section Plot, Synopsis ou Storyline (termes utilisés en anglais)
        synopsis_section = None
        for section in sections:
            if re.search(r'Plot|Synopsis|Storyline|Summary', section.title, re.IGNORECASE):
                synopsis_section = section
                break
        
        # Si une section Synopsis est trouvée, retourner son contenu
        if synopsis_section and synopsis_section.text.strip():
            return synopsis_section.text.strip()
        
        # Si aucune section Synopsis n'est trouvée ou si elle est vide,
        # essayer d'extraire un résumé du début de l'article
        summary = page.summary
        if summary:
            # Supprimer la première phrase si elle ne fait que mentionner le nom du film
            summary_lines = summary.split('\n')
            if re.match(r'^.*is a film.*|^.*is a \d+ .*film.*', summary_lines[0]):
                if len(summary_lines) > 1:
                    return '\n'.join(summary_lines[1:])
            
            return summary
        
        return None
    
    except Exception as e:
        return None

def search_movie(terme_recherche, langue='en', max_resultats=5):
    """
    Recherche des films sur Wikipédia correspondant au terme de recherche.
    Utilise l'API MediaWiki directement.
    
    Args:
        terme_recherche (str): Le terme à rechercher
        langue (str): Code de langue pour Wikipédia (défaut: 'en')
        max_resultats (int): Nombre maximum de résultats à retourner
        
    Returns:
        list: Liste des titres de films correspondants
    """
    # Construire l'URL de l'API MediaWiki
    api_url = f"https://{langue}.wikipedia.org/w/api.php"
    
    # Paramètres de la requête
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': f"{terme_recherche} film",  # Ajouter "film" pour cibler les films
        'format': 'json',
        'srlimit': max_resultats
    }
    
    try:
        # Effectuer la requête
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extraire les titres
        resultats = []
        if 'query' in data and 'search' in data['query']:
            for item in data['query']['search']:
                resultats.append(item['title'])
        
        return resultats
    except Exception as e:
        print(f"Erreur lors de la recherche: {e}")
        return []

def traduire_texte(texte, langue_source='en', langue_cible='fr'):
    """
    Fonction pour traduire le texte (à implémenter avec une API de traduction).
    Cette fonction est un placeholder - vous devrez implémenter une solution
    de traduction réelle en utilisant par exemple Google Translate API,
    DeepL API, etc.
    
    Args:
        texte (str): Le texte à traduire
        langue_source (str): La langue source
        langue_cible (str): La langue cible
        
    Returns:
        str: Le texte traduit ou le texte original si la traduction échoue
    """
    # Ceci est un placeholder - à remplacer par une vraie API de traduction
    print("Note: La traduction automatique n'est pas implémentée dans cette version.")
    return texte

# Exemple d'utilisation
# if __name__ == "__main__":
#     print("Recherche de films sur Wikipedia en anglais")
#     mode = input("Mode (1: recherche par titre exact, 2: recherche par mot-clé): ")
    
#     if mode == "1":
#         titre = input("Entrez le titre du film (en anglais): ")
#         synopsis = get_movie_synopsis(titre)
#         print("\n=== SYNOPSIS ===\n")
#         print(synopsis)
        
#         # Option pour traduire
#         if input("\nVoulez-vous essayer de traduire ce synopsis en français? (o/n): ").lower() == 'o':
#             synopsis_traduit = traduire_texte(synopsis)
#             print("\n=== SYNOPSIS TRADUIT ===\n")
#             print(synopsis_traduit)
    
#     elif mode == "2":
#         terme = input("Entrez un terme de recherche (en anglais): ")
#         resultats = search_movie(terme)
        
#         if resultats:
#             print("\nFilms trouvés:")
#             for i, titre in enumerate(resultats, 1):
#                 print(f"{i}. {titre}")
            
#             choix = input("\nEntrez le numéro du film à consulter (ou 0 pour quitter): ")
#             if choix.isdigit() and 1 <= int(choix) <= len(resultats):
#                 synopsis = get_movie_synopsis(resultats[int(choix)-1])
#                 print("\n=== SYNOPSIS ===\n")
#                 print(synopsis)
                
#                 # Option pour traduire
#                 if input("\nVoulez-vous essayer de traduire ce synopsis en français? (o/n): ").lower() == 'o':
#                     synopsis_traduit = traduire_texte(synopsis)
#                     print("\n=== SYNOPSIS TRADUIT ===\n")
#                     print(synopsis_traduit)
#         else:
#             print("Aucun film trouvé avec ce terme.")
    
#     else:
#         print("Mode non reconnu.")

print(get_movie_synopsis("Iron Man", "en"))
