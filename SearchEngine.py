"""
Université de Bretagne Sud / ENSIBS

Un petit TP de TALN pour implémenter un moteur de recherche
Année 2022 – 2023

Author: Killian MONNIER

Vous devez réaliser pour ce TP des programmes ou scripts permettant d'appliquer les différents
outils aux documents pour extraire les termes à indexer, et les mettre dans le format d'entrée de
l'indexeur (défini ci-dessous). Vous êtes libres d'utiliser le(s) lagunage(s) que vous voulez pour cela
(je conseille l'utilisation de scripts Perl ou Python, mais un ensemble de scripts Shell ou des
programmes JAVA, C++ ou autres sont tout à fait envisageables).
Un moteur de recherche permet de trouver rapidement et de manière optimisée des ressources à
partir d’une requête.
La procédure qui permet à un moteur de recherche d’optimiser le temps nécessaire à l’exécution
d’une requête est l’indexation automatique de documents, qui consiste à réorganiser des documents
afin d’accélérer ultérieurement la recherche en se basant sur un index inversé.
Un index inversé est une correspondance entre le contenu d’un document (les mots qui le
constituent), et sa position dans un ensemble de données. Autrement dit il associe un terme et les
documents dans lesquels il apparaît.
La figure qui suit illustre un exemple d’index inversé.
"""

"""Exercice 1 – Implémentation d’un moteur de recherche"""

import pickle

class SearchEngine:
    """Classe Moteur"""

    """Exercice 1 - Partie 1 :"""

    # 1. On considère un moteur de recherche implémenté avec la classe suivante Moteur. La classe Moteur doit avoir comme attributs deux dictionnaires :

    # inv_indx un dictionnaire qui représente l’index inversé où les clés représentent les termes et les valeurs représente les documents sous la forme d’un ensemble « set() ».
    inv_indx = {}

    # docs_links un dictionnaire qui a pour clés les identifiants des documents et pour valeur le nom des fichiers associés.
    docs_links = {}

    def __init__(self):
        """Constructeur de la classe Moteur"""
        self.inv_indx = {}
        self.docs_links = {}
        self.inv_indx_lang = {}
        self.docs_links_lang = {}

    # 2. Écrivez les méthodes add_to_index(self,word_list) et add_bulk(self, doc_list) qui permettent respectivement d’indexer un document (sous la forme d’une liste de mots) et d’indexer une liste de documents.
    def add_to_index(self, word_list):
        """Méthode add_to_index"""
        for word in word_list:
            if word in self.inv_indx:
                # Ajout de l'identifiant du document dans l'index inversé
                self.inv_indx[word].add(str(len(self.docs_links)))
            else:
                # Création d'une nouvelle entrée dans l'index inversé
                self.inv_indx[word] = set(str(len(self.docs_links)))

    def add_bulk(self, doc_list):
        """Méthode add_bulk"""
        for doc in doc_list:
            # Ouverture du document et ajout des mots dans l'index inversé
            open_doc = open(doc, 'r', encoding="utf-8")
            word_list = open_doc.read().split()
            self.add_to_index(word_list)
            open_doc.close()

            # Ajout du document dans le dictionnaire des documents si il n'y est pas déjà
            if doc not in self.docs_links:
                self.docs_links[str(len(self.docs_links))] = doc

    # 3. Écrivez les méthodes search_word(self, w) et search_inverse_word(self, w) qui permettent respectivement de renvoyer les documents dans lesquels le mot w apparaît et de renvoyer les documents qui ne contiennent pas le mot w.
    def search_word(self, w):
        """Méthode search_word"""
        if w in self.inv_indx:
            return self.inv_indx[w]
        else:
            return set()

    def search_inverse_word(self, w):
        """Méthode search_inverse_word"""
        docs = set(self.docs_links.keys()) # Ensemble des documents
        if w in self.inv_indx:
            return set(docs).difference(self.inv_indx[w]) # Retourne les documents qui ne contiennent pas le mot w
        else:
            return set(docs)

    # 4. Écrivez les méthodes and_(self, w1,w2) et or_(self,w1,w2) qui permettent de renvoyer respectivement les documents qui contiennent w1 et w2 et les documents qui contiennent w1 ou w2.
    def and_(self, w1, w2):
        """Méthode and_"""
        if w1 in self.inv_indx and w2 in self.inv_indx:
            return self.inv_indx[w1].intersection(self.inv_indx[w2])

    def or_(self, w1, w2):
        """Méthode or_"""
        if w1 in self.inv_indx and w2 in self.inv_indx:
            return self.inv_indx[w1].union(self.inv_indx[w2])

    # 5. Écrivez la méthode qui permet de renvoyer les documents qui contiennent les mots de la requête query en respectant les conditions logiques exprimées par la requête (exemple: "droit AND -numérique")
    def search_query(self, query):
        """Méthode data"""
        query = query.split()
        result = set()
        for i in range(len(query)):
            if query[i] == "AND":
                result = self.and_(query[i-1], query[i+1])
            elif query[i] == "OR":
                result = self.or_(query[i-1], query[i+1])
            elif query[i][0] == "-":
                result = self.search_inverse_word(query[i][1:])
            else:
                result = self.search_word(query[i])
        return result

    """Exercice 1 - Partie 2 :"""

    # 1. Écrivez la méthode tokenize(self, s) qui à partir d’une chaîne de charactère renvoie une liste de termes.
    def tokenize(self, s):
        """Méthode tokenize"""
        return s.split()

    # 2. Écrivez les méthodes add_to_index_file(self,fname) et add_bulk_file(self, filenames) qui permettent respectivement d’indexer un document (sous la forme d’un fichier texte) et d’indexer une liste de documents.
    def add_to_index_file(self, fname):
        filepath = "data/" + fname
        file = open(filepath, "r")
        doc_id = len(self.docs_links)
        self.docs_links[doc_id] = fname
        self.add_to_index(self.tokenize(file.read()))

    def add_bulk_file(self, filenames):
        for filename in filenames:
            self.add_to_index_file(filename)

    # 3. Écrivez les méthodes suivantes:

    # intersection_sets_terms(self,terms) qui renvoie les documents qui résultent de l’intersection d’une liste de termes.
    def intersection_sets_terms(self, terms):
        result = set()
        for term in terms:
            result = result & self.search_word(term)
        return result

    # union_sets_terms(self,terms) qui renvoie les documents qui résultent de l’union d’une liste de termes.
    def union_sets_terms(self, terms):
        result = set()
        for term in terms:
            result = result | self.search_word(term)
        return result

    # intersection_inv_sets_terms(self,terms) qui renvoie les documents qui ne contiennent pas une liste de termes.
    def intersection_inv_sets_terms(self, terms):
        result = set(self.docs_links.keys())
        for term in terms:
            result = result & self.search_inverse_word(term)
        return result

    # intersection_sets(self, sets) qui renvoie les documents qui résultent de l’intersection d’une liste de « set ».
    def intersection_sets(self, sets):
        result = set()
        for set_ in sets:
            result = result & set_
        return result

    # 4. Écrivez la méthode search(self, must_include, at_least_one, exclude) qui retourne les documents qui contiennent tout les terms dans la liste must_include, les documents qui contiennent au moins un des terms dans la liste at_least_one et les documents qui ne contiennent aucun des mots de la liste exclude avce la fonction intersection_sets.
    def search(self, must_include, at_least_one, exclude):
        """Méthode search"""
        return self.intersection_sets([self.intersection_sets_terms(must_include), self.union_sets_terms(at_least_one), self.intersection_inv_sets_terms(exclude)])

    # Écrivez la méthode print_result(self, search_result, max_results ) qui permet d’afficher le nom et le contenue d’un ensemble de documents (le nombre de résultats à afficher sera déterminé par l’argument ‘max_results’).
    def print_result(self, search_result, max_results):
        """Méthode print_result"""
        content = dict()
        # if search_result is not None
        if search_result != None and search_result != [] and search_result != 0:
            for id in search_result:
                id = str(id)
                if id in self.docs_links:
                    # ouverture du fichier en lecture
                    doc = open(self.docs_links[id], 'r', encoding="utf-8")
                    # lecture du fichier et ajout dans le dictionnaire
                    content[self.docs_links[id]] = doc.read().splitlines()[:int(max_results)]
                    doc.close()
                else:
                    print("id not found")
            return content
        else:
            return None

    # Écrivez les méthodes save(self, file) et load(self, file) qui permettent respectivement de
    # sauvegarder et de charger les indexes de notre moteur de recherche ( self.inv_indx et
    # self.docs_links ).
    def save(self, file):
        # save inv_indx and docs_links
        with open(file, 'wb') as f:
            pickle.dump(self.inv_indx, f)
            pickle.dump(self.docs_links, f)

    def load(self, file):
        # load inv_indx and docs_links
        with open(file, 'rb') as f:
            self.inv_indx = pickle.load(f)
            self.docs_links = pickle.load(f)

    """Exercice 2 – Detecter la langue d’une chaine"""
    # 1. Copier contenu d’une dizaine de pages internet libre de droit (par exemple, wikipedia, et
    # coller les dans un fichier texte pour chacune des langues (par exemple, francais.txt,
    # espagnol.txt, anglais.txt).