"""Exercice 1 – Implémentation d’un moteur de recherche"""

class Moteur:
    """Classe Moteur"""

    # inv_indx qui représente l’index inversé où les clés représentent les termes et les valeurs représente les documents sous la forme d’un ensemble « set() »
    inv_indx = {}

    # docs_links un dictionnaire qui a pour clés l’identifiant d’un document et pour valeur le nom du fichier
    docs_links = {}

    def __init__(self, index):
        """Constructeur de la classe Moteur"""
        self.index = index

    # Écrivez les méthodes add_to_index(self,word_list) et add_bulk(self, doc_list) qui permettent respectivement d’indexer un document (sous la forme d’une liste de mots) et d’indexer une liste de documents
    def add_to_index(self, word_list):
        """Méthode add_to_index"""
        for word in word_list:
            if word not in self.inv_indx:
                self.inv_indx[word] = set()
            self.inv_indx[word].add(self.index)

    def add_bulk(self, doc_list):
        """Méthode add_bulk"""
        for doc in doc_list:
            self.docs_links[self.index] = doc
            self.add_to_index(doc)
            self.index += 1

    # Écrivez les méthodes search_word(self, w) et search_inverse_word(self, w) qui permettent respectivement de renvoyer les documents dans lesquels le mot w apparaît et de renvoyer les documents qui ne contiennent pas le mot w
    def search_word(self, w):
        """Méthode search_word"""
        return self.inv_indx[w]

    def search_inverse_word(self, w):
        """Méthode search_inverse_word"""
        return set(self.docs_links.keys()) - self.inv_indx[w]




