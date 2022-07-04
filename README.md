# `text2web` : transformation d'un texte brut vers une édition web et visualisation en python

---

## Présentation

---

## Structure du dépôt

```
/
|__img/ : dossier contenant les images
|
|__input/ : dossier contenant le texte utilisé comme source pour le tutoriel
|
|__output/ : dossier pour stocker les fichiers produits (pas sur github)
|
|__src/ : scripts python à la base des notebooks
|   |__text2web_html.py : création automatique de HTML à partir d'un texte brut
|   |__text2web_viz.py : analyse statistique du fichier et visualisation de données
|
|__utils/ : fichiers utilisés pendant le tutoriel
|   |__static/ : dossier contenant une feuille de style CSS et les fontes utilisées par notre site web (toutes deux open source)
|   |__to_text.py : script python utilisé pour la création du fichier source (dans input/)
|   |__catalog_web_skeleton.html : squelette de HTML auquel on viendra ajouter le contenu créé pendant les tutoriels
|
|__0_text2web_intro.ipynb : 1er notebook introductif
|__1_text2web_html.ipynb : 2e notebook: traitement du document source et création automatique d'un fichier HTML
|__2_text2web_viz.ipynb : 3e notebook: analyse statistique basique du document source et création de visualisations
|__install.sh : script d'installation du notebook
|__requirements.txt : librairies à installer
```

---

## Installation

Cette installation fonctionne sur Linux (ubuntu et distributions dérivées de debian) et MacOS

### Installation automatique

Un script shell a été créé pour installer tout ce dont on a besoin en 2 étapes toutes simples:
```
git clone https://github.com/paulhectork/tutorials/tree/main/text2web.git  # cloner le dossier 

### Installation manuelle
