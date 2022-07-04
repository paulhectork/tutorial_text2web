from lxml import etree
from glob import glob
import re


# dans ce script, on produit les données utilisées dans le reste du tutoriel.
# on minimise l'usage de lxml (librairie qui sert à parser du xml), vu que la
# librairie demande des bonnes bases en xml, xpath et python et que ce n'est pas
# le but de l'exercice. on s'appuyera donc surtout sur des aspects basiques de
# python (les boucles, les listes, la concaténation de chaînes de caractères) et
# sur expressions régulières qui sont expliquées.

# source des données: https://github.com/katabase/1_OutputData.git


def makeinput():
    """
    fonction permettant de produire le texte brut utilisé en source à partir de
    catalogues structurés en xml-tei
    :return: None
    """
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}  # espace de nom tei, pour les xpath
    out = ""  # variable pour stocker le texte à écrire en sortie

    # itérer sur tous les fichiers à traiter: ceux du dossier 1-100/.
    # à l'intérieur de cette boucle for, on travaille donc au niveau du
    # fichier xml
    n = 0  # compter le nombre d'itérations
    for f in glob("./1_OutputData/1-100/*.xml"):
        if n < 20:  # permet de compter les itérations et de ne travailler qu'avec 30 catalogues
            # ouvrir les fichiers en lecture avec open()
            with open(f, mode="r"):
                author = ""  # auteur.ice du document, correspondant au <name> du document source
                number = ""  # numéro de l'item, correspondant au <num>
                trait = ""  # description de l'auteur.ice, dans un <trait>
                desc = ""  # description de l'élément vendu, correspondant aux <desc> et <note>
                price = ""  # prix, correspondant à l'élément <measure>
                tree = etree.parse(f)  # parser le xml

                # récupérer tous les <item>, c-a-d les éléments de catalogue qui nous intéressent
                items = tree.xpath(".//tei:body//tei:item", namespaces=ns)

                # itérer sur tous les items. dans la boucle for qui suit,
                # on travaille donc au niveau de l'<item>
                for item in items:

                    # le contenu des <item> sans balise est transformé en liste: le contenu d'une balise
                    # correspond à un item d'une liste ; les espaces vides à l'intérieur d'un <item>
                    # forment eux aussi des items dans la liste. l'ordre des items correspond à celui des
                    # éléments dans le fichier originel; on pourra donc s'appuyer sur cet ordre pour extraire
                    # le texte !
                    # faire "print(text)" pour voir la liste produite par lxml.
                    text = item.xpath(".//text()", namespaces=ns)

                    # on commence par extraire le numéro de l'item vendu et son titre.
                    # ces 2 syntaxes en une ligne fort peu élégantes permettent de récupérer le numéro
                    # de l'item vendu et son prix:
                    # - le numéro de l'item correspond à la première suite de chiffres dans la liste text
                    # - le prix correspond à à la dernière série de chiffres.
                    #
                    # pour repérer une série de chiffres, on utilise la regex "^\d+$":
                    # - "\d" = un chiffre
                    # - "+": plusieurs fois le symbole précédent, soit "\d" dans notre cas.
                    # - "^" et "$" correspondent respectivement au début et à la fin d'une ligne
                    number = next((i for i in text if re.search(r"^\d+$", i)), None)
                    price = next((i for i in reversed(text) if re.search(r"^\d+$", i)), None)

                    # on récupère ensuite l'auteur.ice, avec la même méthode: l'auteur.ice est le premier élément qui n'est ni
                    # - un saut de lignes ("\n") suivi d'espaces ("\s") ("\n\s*?")
                    # - une suite de chiffres ("\d+")
                    author = next((i for i in text if not re.search(r"^(\n\s*?|\d+)$", i)), None)

                    # on récupère ensuite le <trait>, c'est-à-dire une description de l'auteur.ice. ici, il est
                    # est beaucoup plus facile de passer par lxml
                    # try...except permet d'éviter des erreurs:
                    # - par défaut, le bloc de code dans le try s'exécute en premier: on essaye de récupérer un <trait>
                    # - si il y a une erreur dans la partie "try", le bloc de code qui est dans le except s'exécute:
                    #   dans notre cas, on dit que trait est vide.
                    #
                    # c'est globalement une bonne pratique de faire des try...except plutôt que des if...else
                    # quand la situation s'y prête (si vous faites du développement web et que les utilisateur.ice
                    # ajoutent des données à votre site, le try...except est votre meilleur allié !)
                    try:
                        trait = item.xpath(".//tei:trait//tei:p//text()", namespaces=ns)[0]
                    except:
                       trait = ""

                    # on extrait ensuite le reste du texte, c'est-à-dire la description des items vendus
                    # on procède tout bêtement par élimitation: on itère sur tous les éléments de text.
                    # si ils ne correspondent pas à ce que l'on a déjà récupéré et qu'ils ne sont pas "vides"
                    # (c-a-d qu'ils ne correspondent pas à "^\n\s*$"), alors on les ajoute à la variable desc.
                    desc = ""  # variable permettant de stocker la description d'un item
                    for t in text:
                        if t != number and t != price and t != author and t != trait and not re.search(r"^\n\s*$", t):
                            desc += f"{t} "  # (la syntaxe "f'{variable} ...'" permet de concaténer une
                            #                  variable avec des chaînes de caractères: la variable s'écrit entre {},
                            #                  le reste de la chaîne s'écrit en dehors des {}. dans les faits, on ajoute
                            #                  ici un espace à la fin de la variable t.)

                    # ensuite, on retire les potentiels sauts de lignes et série d'espaces (très fréquents
                    # puisqu'on parse un fichier tei). on supprime aussi les espaces en début et fin
                    # de ligne grâce à ".strip()"
                    if number is not None:
                        number = re.sub(r"\n\s*", r" ", number).strip()
                    if price is not None:
                        price = re.sub(r"\n\s*", r" ", price).strip()
                    if author is not None:
                        author = re.sub(r"\n\s*", r" ", author).strip()
                        author = author.replace("--", "-")
                    if desc is not None:
                        desc = re.sub(r"\n\s*", r" ", desc).strip()
                    if trait is not None:
                        trait = re.sub(r"\n\s*", r" ", trait).strip()

                    # print(etree.tostring(item, pretty_print=True))

                    # maintenant, toutes nos données sont prêtes. pour chaque "item", on
                    # met à jour la variable out avec les nouvelles données. les items
                    # doivent avoir un minimum de structure pour que l'on puisse en faire
                    # quelque chose automatiquement.
                    # la structure attendue est la suivante:
                    # - première ligne: numéro d'item, nom de la personne et description de celle-ci.
                    # - deuxième ligne: description de l'item vendu.
                    # - troisième ligne: prix en francs.

                    # première ligne:
                    # on concatène le numéro de l'item avec "--" puis avec le nom de l'auteur.ice
                    out += f"{number} -- {author} "
                    # si il y a un trait, on l'ajoute à cette première ligne
                    if trait != "":
                        out += f"~ {trait} "  # pour la suite, on choisit "~" comme séparateur: un séparateur rare
                        #                       a peu de chances d'être utilisé ailleurs dans le texte
                    out += r"\n"  # on ajoute un saut de ligne, soit "\n"

                    # deuxième ligne:
                    out += f" {desc} "  # on ajoute le desc
                    out += r"\n"  # on ajoute le saut de ligne

                    # troisième ligne
                    if price != "":
                        out += f" {price} francs. "

                    # enfin, on saute trois lignes pour marquer la fin d'un élément
                    out += r"\n\n\n "
                    n += 1  # on indique qu'on a traité un fichier en plus

    # il ne reste plus qu'à créer un fichier dans lequel on viendra tout stocker. c'est
    # ce fichier qui sera utilisé pour le reste du tutoriel.
    # with open() ouvre un fichier.
    # - le premier argument est le fichier de sortie. il est exprimé en chemin relatif depuis
    #   le dossier dans lequel le script to_text.py est exécuté vers le fichier de sortie
    # - le deuxième argument, "mode=" indique que le fichier est ouvert en écriture ("w")
    # - le troisième argument ("encoding") est l'encodage du fichier en sortie.
    with open("../input/source.txt", mode="w", encoding="utf-8") as fh:
        fh.write(out)  # écrire le contenu de la variable "out" dans le fichier de sortie "fh"

    # le "return" est la valeur qui est retenue par python à la fin de l'exécution d'une fonction.
    # cela permet de réutiliser le résultat d'une fonction ailleurs. ici, on ne retourne rien.
    return None


# cette structure permet de définir une action à exécuter seulement
# si le fichier est directement exécuté par l'utilisateur.ice. quand l'utilisateur.ice
# exécute directement un fichier, python lui donne le doux nom de "__main__".
# en fait, quand on travaille sur un "vrai" projet python, on a souvent sur plusieurs
# fichiers python qui contiennent des scripts différents. un fichier A peut appeler une fonction
# qui est dans un fichier B.
# if __name__ permet d'éviter que des fonctions s'exécutent par erreur lorsque le fichier B est ouvert
# par le fichier A.
# ce n'est pas nécessairement clair maintenant, mais ça rentre très vite avec la pratique.
# pour faire bref, il faut privilégier le if __name__... pour éviter que des choses imprévues se passent.
if __name__ == "__main__":
    makeinput()
