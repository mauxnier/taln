from SearchEngine import SearchEngine as Moteur

# Création d’un moteur de recherche
moteur = Moteur()

"""Exercice 1 – Implémentation d’un moteur de recherche"""

# Ajout de documents
moteur.add_bulk(["./data/docs/doc0.txt", "./data/docs/doc1.txt", "./data/docs/doc2.txt", "./data/docs/doc3.txt", "./data/docs/doc4.txt"])

# Recherche de documents contenant le mot "droit"
print("moteur.search_word('droit'): ", moteur.search_word("droit"))

# Recherche de documents ne contenant pas le mot "droit"
print("moteur.search_inverse_word('droit'): ", moteur.search_inverse_word("droit"))

# Recherche de documents contenant le mot "droit" et "fracture"
print("moteur.and_('droit', 'fracture'): ", moteur.and_("droit", "fracture"))

# Recherche de documents contenant le mot "droit" ou "fracture"
print("moteur.or_('droit', 'fracture'): ", moteur.or_("droit", "fracture"))

# Recherche de documents contenant le mot "droit" mais pas "fracture"
print("moteur.search_query('droit AND -fracture'): ", moteur.search_query("droit AND -fracture"))

"""Exercice 2 – Detecter la langue d’une chaine"""

