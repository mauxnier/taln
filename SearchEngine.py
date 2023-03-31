"""
Université de Bretagne Sud / ENSIBS

Un petit TP de TALN pour implémenter un moteur de recherche
Année 2022 – 2023

Author : Killian MONNIER

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
"""
import pickle
import string

from collections import Counter

"""Exercice 1 – Implémentation d’un moteur de recherche"""


class SearchEngine:
    """Classe Moteur"""

    """Exercice 1 - Partie 1 :"""

    # 1. On considère un moteur de recherche implémenté avec la classe suivante Moteur. La classe Moteur doit avoir
    # comme attributs deux dictionnaires :

    def __init__(self):
        """Constructeur de la classe Moteur"""
        self.inv_index = {}  # inv_index un dictionnaire qui représente l’index inversé où les clés représentent les
        # termes et les valeurs représentent les documents sous la forme d’un ensemble « set() ».
        self.docs_links = {}  # docs_links un dictionnaire qui a pour clés les identifiants des documents et pour
        # valeur le nom des fichiers associés.
        self.inv_index_lang = {}
        self.docs_links_lang = {}

    # 2. Écrivez les méthodes add_to_index (self, word_list) et add_bulk (self, doc_list) qui permettent respectivement
    # d’indexer un document (sous la forme d’une liste de mots) et d’indexer une liste de documents.
    def add_to_index(self, word_list):
        """Méthode add_to_index"""
        for word in word_list:
            if word in self.inv_index:
                # Ajout de l'identifiant du document dans l'index inversé
                self.inv_index[word].add(str(len(self.docs_links)))
            else:
                # Création d'une nouvelle entrée dans l'index inversé
                self.inv_index[word] = set(str(len(self.docs_links)))

    def add_bulk(self, doc_list):
        """Méthode add_bulk"""
        for doc in doc_list:
            # Ouverture du document et ajout des mots dans l'index inversé
            open_doc = open(doc, 'r', encoding="utf-8")
            word_list = open_doc.read().split()
            self.add_to_index(word_list)
            open_doc.close()

            # Ajout du document dans le dictionnaire des documents s'il n'y est pas déjà
            if doc not in self.docs_links:
                self.docs_links[str(len(self.docs_links))] = doc

    # 3. Écrivez les méthodes search_word (self, w) et search_inverse_word (self, w) qui permettent respectivement de
    # renvoyer les documents dans lesquels le mot w apparaît et de renvoyer les documents qui ne contiennent pas le
    # mot w.
    def search_word(self, w):
        """Méthode search_word"""
        if w in self.inv_index:
            return self.inv_index[w]
        else:
            return set()

    def search_inverse_word(self, w):
        """Méthode search_inverse_word"""
        docs = set(self.docs_links.keys())  # Ensemble des documents
        if w in self.inv_index:
            return set(docs).difference(self.inv_index[w])  # Retourne les documents qui ne contiennent pas le mot w
        else:
            return set(docs)

    # 4. Écrivez les méthodes and_(self, w1,w2) et or_(self,w1,w2) qui permettent de renvoyer respectivement les
    # documents qui contiennent w1 et w2 et les documents qui contiennent w1 ou w2.
    def and_(self, w1, w2):
        """Méthode and_"""
        if w1 in self.inv_index and w2 in self.inv_index:
            return self.inv_index[w1].intersection(self.inv_index[w2])

    def or_(self, w1, w2):
        """Méthode or_"""
        if w1 in self.inv_index and w2 in self.inv_index:
            return self.inv_index[w1].union(self.inv_index[w2])

    # 5. Écrivez la méthode qui permet de renvoyer les documents qui contiennent les mots de la requête query en
    # respectant les conditions logiques exprimées par la requête (exemple: "droit AND -numérique")
    def search_query(self, query):
        """Méthode data"""
        query = query.split()
        result = set()
        for i in range(len(query)):
            if query[i] == "AND":
                result = self.and_(query[i - 1], query[i + 1])
            elif query[i] == "OR":
                result = self.or_(query[i - 1], query[i + 1])
            elif query[i][0] == "-":
                result = self.search_inverse_word(query[i][1:])
            else:
                result = self.search_word(query[i])
        return result

    """Exercice 1 - Partie 2 :"""

    # 1. Écrivez la méthode tokenize (self, s) qui a partir d’une chaîne de caractère renvoie une liste de termes.
    def tokenize(self, s):
        """Méthode tokenize"""
        return s.split()

    # 2. Écrivez les méthodes add_to_index_file (self, fname) et add_bulk_file(self, filenames) qui permettent
    # respectivement d’indexer un document (sous la forme d’un fichier texte) et d’indexer une liste de documents.
    def add_to_index_file(self, fname):
        file = open(fname, "r")
        doc_id = len(self.docs_links)
        self.docs_links[doc_id] = fname
        self.add_to_index(self.tokenize(file.read()))

    def add_bulk_file(self, filenames):
        for filename in filenames:
            self.add_to_index_file(filename)

    # 3. Écrivez les méthodes suivantes :

    # intersection_sets_terms (self, terms) qui renvoie les documents qui résultent de l’intersection d’une liste de
    # termes.
    def intersection_sets_terms(self, terms):
        result = set()
        for term in terms:
            result = result & self.search_word(term)
        return result

    # union_sets_terms (self, terms) qui renvoie les documents qui résultent de l’union d’une liste de termes.
    def union_sets_terms(self, terms):
        result = set()
        for term in terms:
            result = result | self.search_word(term)
        return result

    # intersection_inv_sets_terms (self, terms) qui renvoie les documents qui ne contiennent pas une liste de termes.
    def intersection_inv_sets_terms(self, terms):
        result = set(self.docs_links.keys())
        for term in terms:
            result = result & self.search_inverse_word(term)
        return result

    # intersection_sets (self, sets) qui renvoie les documents qui résultent de l’intersection d’une liste de « set ».
    def intersection_sets(self, sets):
        result = set()
        for set_ in sets:
            result = result & set_
        return result

    # 4. Écrivez la méthode recherche (self, must_include, at_least_one, exclude) qui retourne les documents qui
    # contiennent tout les terms dans la liste must_include, les documents qui contiennent au moins un des terms dans
    # la liste at_least_one et les documents qui ne contiennent aucun des mots de la liste exclude avec la fonction
    # intersection_sets.
    def search(self, must_include, at_least_one, exclude):
        """Méthode search"""
        return self.intersection_sets([self.intersection_sets_terms(must_include), self.union_sets_terms(at_least_one),
                                       self.intersection_inv_sets_terms(exclude)])

    # Écrivez la méthode print_result (self, search_result, max_results) qui permet d’afficher le nom et le contenu
    # d’un ensemble de documents (le nombre de résultats à afficher sera déterminé par l’argument ‘max_results’).
    def print_result(self, search_result, max_results):
        """Méthode print_result"""
        content = dict()
        # if search_result is not None
        if search_result is not None and search_result != [] and search_result != 0:
            for doc_id in search_result:
                doc_id = str(doc_id)
                if doc_id in self.docs_links:
                    # ouverture du fichier en lecture
                    doc = open(self.docs_links[doc_id], 'r', encoding="utf-8")
                    # lecture du fichier et ajout dans le dictionnaire
                    content[self.docs_links[doc_id]] = doc.read().splitlines()[:int(max_results)]
                    doc.close()
                else:
                    print("id not found")
            return content
        else:
            return None

    # Écrivez les méthodes save (self, file) et load(self, file) qui permettent respectivement de
    # sauvegarder et de charger les indexés de notre moteur de recherche (self.inv_index et
    # self.docs_links ).
    def save(self, file):
        # save inv_index and docs_links
        with open(file, 'wb') as f:
            pickle.dump(self.inv_index, f)
            pickle.dump(self.docs_links, f)

    def load(self, file):
        # load inv_index and docs_links
        with open(file, 'rb') as f:
            self.inv_index = pickle.load(f)
            self.docs_links = pickle.load(f)

    """Exercice 2 – Detecter la langue d’une chaine"""

    # 1. Copier contenu d’une dizaine de pages internet libre de droit (par exemple, Wikipédia, et coller les dans un
    # fichier texte pour chacune des langues (par exemple, francais.txt, espagnol.txt, anglais.txt).

    # 2. Écrivez une ou plusieurs fonctions qui prennent en charge la lecture de chacun de ces fichiers et qui
    # construit un index pour chaque langue (sur le même principe que les dictionnaires d’index vu à l’exercice 1).
    def add_to_index_lang(self, word_list, doc_lang):
        """Méthode add_to_index_lang"""
        if doc_lang not in self.inv_index_lang:
            self.inv_index_lang[doc_lang] = {}

        for word in word_list:
            if word not in self.inv_index_lang[doc_lang]:
                self.inv_index_lang[doc_lang][word] = set()  # Création d'une nouvelle entrée dans l'index inversé
            self.inv_index_lang[doc_lang][word].add(
                str(len(self.docs_links_lang)))  # Ajout de l'identifiant du document dans l'index inversé

    def add_bulk_lang(self, doc_list):
        """Méthode add_bulk_lang"""
        for doc in doc_list:
            filepath = "./data/lang/" + doc
            # Ouverture du document et ajout des mots dans l'index inversé
            open_doc = open(filepath, 'r', encoding="utf-8")
            word_list = open_doc.read().split()
            word_list = [word.strip(string.punctuation) for word in word_list]  # Suppression de la ponctuation

            # Enlève .txt de la fin du nom du fichier
            lang = doc[:-4]
            self.add_to_index_lang(word_list, lang)

            open_doc.close()

            # Ajout du document dans le dictionnaire des documents s'il n'y est pas déjà
            if lang not in self.docs_links_lang:
                self.docs_links_lang[str(len(self.docs_links_lang))] = lang
            # print(self.docs_links_lang)

    # 3. Nous allons utiliser les fréquences calculées à la question précédente pour prédire la langue l, d'un mot.
    # Pour cela, nous allons considérer la fonction de décision suivante : l* = argmaxl∈L P(l|w) Où L est l'ensemble
    # des langues que notre système connaît, et est le résultat de la prédiction et P le score du mot w dans la
    # langue l. écrivez une fonction qui prend en paramètre une phrase et qui retourne. Tester votre système avec
    # des exemples de phrases simples.
    def predict_lang(self, phrase):
        # Initialisation des variables
        word_counts = {}
        total_word_count = 0

        # Comptage des mots dans la phrase
        for word in phrase.split():
            total_word_count += 1
            # print("====== > Mot: " + word + " < ======")
            for doc_id, lang in self.docs_links_lang.items():
                # print("Id du document: " + doc_id)
                # print("Langue du document: " + lang)
                lang_list = self.inv_index_lang[lang]
                # print("Liste des mots dans la langue: " + str(lang_list))

                if any(doc_id in docs for docs in lang_list.values()):  # Si la langue est détectée
                    if word in lang_list:  # Si le mot est dans la langue
                        if lang not in word_counts:  # Si la langue n'est pas dans le dictionnaire
                            word_counts[lang] = 1
                            # print("Ajout de la langue " + lang + " dans le dictionnaire")
                        else:  # Si la langue est déjà dans le dictionnaire
                            word_counts[lang] += 1
                #             print("Ajout d'un mot dans la langue: " + lang)
                #     else:
                #         print("Le mot n'est pas dans la langue: " + lang)
                # else:
                #     print("Aucune langue détectée")

        # Calcul des pourcentages
        percentages = {}
        for lang, count in word_counts.items():
            # Traduction des langues en français
            if lang == "fr":
                lang_word = "français"
            elif lang == "en":
                lang_word = "anglais"
            elif lang == "es":
                lang_word = "espagnol"
            else:
                lang_word = lang
            percentages[lang_word] = count / total_word_count

        # Tri des pourcentages par ordre décroissant
        sorted_percentages = sorted(percentages.items(), key=lambda x: x[1], reverse=True)

        # Affichage des pourcentages pour chaque langue
        for lang, percentage in sorted_percentages:
            print(f"Résultat: {lang} {percentage * 100:.2f}%")

        # Prédiction de la langue avec le pourcentage le plus élevé
        if sorted_percentages:
            predicted_lang = sorted_percentages[0][0]
            return predicted_lang
        else:
            return "Aucune langue détectée"
