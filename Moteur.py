"""Exercice 1 – Implémentation d’un moteur de recherche"""

class Moteur:
    """Classe Moteur"""

    # inv_indx un dictionnaire qui représente l’index inversé où les clés représentent les termes et les valeurs représente les documents sous la forme d’un ensemble « set() ».
    inv_indx = {}

    # docs_links un dictionnaire qui a pour clés les identifiants des documents et pour valeur le nom des fichiers associés.
    docs_links = {}

    def __init__(self):
        """Constructeur de la classe Moteur"""
        self.inv_indx = {}
        self.docs_links = {}

    # Écrivez les méthodes add_to_index(self,word_list) et add_bulk(self, doc_list) qui permettent respectivement d’indexer un document (sous la forme d’une liste de mots) et d’indexer une liste de documents.
    def add_to_index(self, word_list, doc_id):
        """Méthode add_to_index"""
        for word in word_list:
            if word in self.inv_indx:
                self.inv_indx[word].add(doc_id)
            else:
                self.inv_indx[word] = {doc_id}

    def add_bulk(self, doc_list):
        """Méthode add_bulk"""
        for doc in doc_list:
            doc_id = len(self.docs_links)
            self.docs_links[doc_id] = doc

    # Écrivez les méthodes search_word(self, w) et search_inverse_word(self, w) qui permettent respectivement de renvoyer les documents dans lesquels le mot w apparaît et de renvoyer les documents qui ne contiennent pas le mot w.
    def search_word(self, w):
        """Méthode search_word"""
        if w in self.inv_indx:
            return self.inv_indx[w]
        else:
            return set()

    def search_inverse_word(self, w):
        """Méthode search_inverse_word"""
        if w in self.inv_indx:
            return set(self.docs_links.keys()) - self.inv_indx[w]
        else:
            return set(self.docs_links.keys())

    # Écrivez les méthodes and_(self, w1,w2) et or_(self,w1,w2) qui permettent de renvoyer respectivement les documents qui contiennent w1 et w2 et les documents qui contiennent w1 ou w2.
    def and_(self, w1, w2):
        """Méthode and_"""
        return self.search_word(w1) & self.search_word(w2)

    def or_(self, w1, w2):
        """Méthode or_"""
        return self.search_word(w1) | self.search_word(w2)

    # Écrivez la méthode data(self, query) qui permet de renvoyer les documents qui contiennent les mots de la requête query en respectant les conditions logiques exprimées par la requête (exemple: "droit AND -numérique")
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

    # Écrivez la méthode tokenize(self, s) qui à partir d’une chaîne de charactère renvoie une liste de termes.
    def tokenize(self, s):
        """Méthode tokenize"""
        return s.split()

    # Écrivez les méthodes add_to_index_file(self,fname) et add_bulk_file(self, filenames) qui permettent respectivement d’indexer un document (sous la forme d’un fichier texte) et d’indexer une liste de documents.
    def add_to_index_file(self, fname):
        filepath = "data/" + fname
        file = open(filepath, "r")
        doc_id = len(self.docs_links)
        self.docs_links[doc_id] = fname
        self.add_to_index(self.tokenize(file.read()), doc_id)

    def add_bulk_file(self, filenames):
        for filename in filenames:
            self.add_to_index_file(filename)

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

    # Écrivez la méthode search(self, must_include, at_least_one, exclude) qui retourne les documents qui contiennent tout les terms dans la liste must_include, les documents qui contiennent au moins un des terms dans la liste at_least_one et les documents qui ne contiennent aucun des mots de la liste exclude avce la fonction intersection_sets.
    def search(self, must_include, at_least_one, exclude):
        """Méthode search"""
        return self.intersection_sets([self.intersection_sets_terms(must_include), self.union_sets_terms(at_least_one), self.intersection_inv_sets_terms(exclude)])

    # Écrivez la méthode print_result(self, search_result, max_results ) qui permet d’afficher le nom et le contenue d’un ensemble de documents (le nombre de résultats à afficher sera déterminé par l’argument ‘max_results’).
    def print_result(self, search_result, max_results):



