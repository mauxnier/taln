# Traitement automatique du langage naturel 🗣️

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

## Indexation avec stoplist
Stoplist en ligne : site de Jacques Savoy : http://www.unine.ch/info/CLEF/frenchST.txt

## Lemmatisation du texte
Tutorial Lemmatisation avec nltk (python)
https://stacklima.com/python-approches-de-lemmatisation-avec-exemples/
https://www.geeksforgeeks.org/python-lemmatization-with-nltk/
