"""Exercice 1 – Implémentation d’un moteur de recherche"""

from Moteur import Moteur

# Création d’un moteur de recherche
moteur = Moteur(0)

# Ajout de documents
moteur.add_bulk(["doc1.txt", "doc2.txt", "doc3.txt", "doc4.txt", "doc5.txt"])

# Recherche de documents contenant le mot "droit"
print(moteur.search_word("droit"))

# Recherche de documents ne contenant pas le mot "droit"
print(moteur.search_inverse_word("droit"))

# Recherche de documents contenant le mot "droit" et "fracture"
print(moteur.and_("droit", "fracture"))

# Recherche de documents contenant le mot "droit" ou "fracture"
print(moteur.or_("droit", "fracture"))

# Recherche de documents contenant le mot "droit" mais pas "fracture"
print(moteur.search(["droit", "AND", "-fracture"]))

