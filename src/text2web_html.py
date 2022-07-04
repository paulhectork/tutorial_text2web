# ------------------------------------------------------------------------
# construire un fichier html à partir de catalogues de vente en texte brut
# disponible sous MIT License. tutoriel par Paul, H. Kervegan
# ------------------------------------------------------------------------



# le script s'appuie sur différentes fonctions. comme en maths, les fonctions
# correspondent à une suite d'opérations. ces opérations peuvent prendre des attributs,
# c'est-à-dire des valeurs spécifiques à utiliser comme input (fpath, ci-dessous).
def read_input(fpath):
    """
    fonction permettant de lire un fichier dont le chemin est donné par fpath
    :param fpath: le chemin du fichier à lire
    :return:
    """
    # la syntaxe "with open()" ouvre un fichier et l'associe à une variable (ici, "fh").
    # open() prend plusieurs arguments; ici, on en utilise 3:
    # - le premier argument est le fichier d'entrée. il est exprimé en chemin relatif depuis
    #   le dossier dans lequel le script to_text.py est exécuté vers le fichier de sortie
    # - le deuxième argument, "mode=" indique ce que l'on va faire avec le fichier:
    #   ici, on indique de l'on lit son contenu avec "r". (on peut aussi écrire un nouveau
    #   fichier avec "w" ou ajouter du contenu à un fichier existant, avec "a").
    # - le troisième argument ("encoding") est l'encodage du fichier en entrée.
    with open(fpath, mode="r", encoding="utf-8") as fh:
        text = fh.read()  # on lit le contenu de fh

    # le "return" est la valeur qui est retenue par python à la fin de l'exécution d'une fonction.
    # cela permet de réutiliser le résultat d'une fonction ailleurs. ici, on retourne input, ce qui veut
    # dire qu'on pourra utiliser le contenu du fichier ailleurs dans notre script.
    return text


def parse_input(input_string):
    """
    fonction permettant de parser une chaîne de caractère, c'est à dire de la séparer en sous-unités
    en fonction de la syntaxe: on repère des catactères spéciaux (des séparateurs) et on en déduit une structure.
    on stocke le résultat de façon plus structurée sous la forme d'une liste imbriquée.
    :param input_string: chaîne à transformer en liste: le texte retourné par read_input()
    :return: source_tolist, une représentation du fichier d'entrée en liste imbriquée:
             [
                [titre1, description1, prix1],
                [titre2, description2, prix2],
                [titreN, descriptionN, prixN]
             ]
    """
    source_tolist = []  # liste de sortie, pour accueillir l'entrée parsée

    # on construit items, soit une liste des différentes entrées de catalogues. ces entrées
    # sont séparées par un triple saut de ligne ("\n\n\n"). on utilise donc "source.split('\n\n\n')"
    # pour faire une liste où chaque item correspond à une entrée de catalogue. cette entrée est sous la
    # forme d'une chaîne de caractère.
    items = input_string.split(r"\n\n\n")

    # on boucle sur toutes les entrées pour définir une structure à chaque entrée. boucler sur un
    # "itérable" (liste, dictionnaire...) permet de travailler uniquement sur un sous ensemble: ici,
    # une entrée parmi toutes les entrées.
    for item in items:
        # au sein de chaque entrée, les différentes parties (titre, description, prix)
        # est séparée par un saut de ligne ("\n", comme on le sait maintenant). on redéfinit
        # donc item comme une liste contenant ces différents éléments.
        item = item.split(r"\n")

        source_tolist.append(item)  # on ajoute la liste item à source_tolist

    # au final, on a parsé notre texte source en une liste d'entrées de catalogues: [entrée1, entrée2, entrée3...]
    # chaque entrée contient elle même une liste: [titre, description, prix].
    # en définitive, on a donc: [[titre1, description1, prix1], [titre2, description2, prix2], ...]
    return source_tolist


def input_to_html():
    """
    écrire un fichier HTML en sortie à partir du fichier source représenté sous
    la forme d'une liste imbriquée.
    :return:
    """
    source = "../input/source.txt"  # chemin vers le fichier à traiter
    html = ""  # variable pour stocker l'html produit à partir de source
    source = read_input(source)  # read_input() retourne une variable contenant du texte.
    #                          on stocke donc le texte produit par read_input() dans une variable nommée source.
    #                          le "source" écrit entre parenthèses est un attribut
    #                          ou un paramètre de parse_input: une valeur avec laquelle travaillera parse_input()
    source = parse_input(source)  # on traduit la source en liste.

    # on itère sur chaque item, puis sur chaque partie de l'item (titre, description, prix: voir parse_input)
    for item in source:
        item_html = "<div>"  # chaîne de caractère qui contiendra le html de l'item
        list_html = "<ul>"  # pour stocker le prix et la description dans une liste
        # price = ""
        # desc = ""
        for part in item:

            part = part.strip()  # on supprime les espaces au début et à la fin de i

            # ici, ce qu'on doit faire, c'est:
            # - identifier à quel type de partie on a à faire: est-ce un titre, une description, un prix ?
            # - en fonction de ce type, intégrer part au html de sortie
            # pour ce faire, on se réfère à la structure de chaque partie:
            # - un titre a la forme suivante:
            #   "{numéro de l'item} -- {nom de la personne} : {description de la personne}"
            # - un prix a la forme suivante:
            #   "{nombre} francs."
            # on est donc à la recherche de motifs. pour identifier un motif, la meilleure
            # chose à faire est de s'appuyer sur des expressions régulières, qui sont une manière
            # codifiée de représenter des motifs.

            # pour rester sur des choses simples, on va éviter de s'appuyer sur des regex lorsque c'est possible.
            # si c'est un titre, c'est le plus difficile
            if "--" in part:
                # on fait une liste séparant le numéro de l'entrée du nom et de la description
                part = part.split("--")
                numero = part[0]  # le numéro est le premier item de la liste
                title = part[1]  # le nom et la description sont le 2e item de la liste

                # on sépare title entre le nom de la personne et sa description
                title = title.split(" ~ ")
                name = title[0]  # le nom est en première partie du title; si il y a un trait, il
                #                  est en deuxième partie
                if len(title) > 1:
                    trait = title[1]
                else:
                    trait = ""

                # on remplit un squelette de html avec les variables extraites de part.
                # f"{variable} ..." est une fonction très pratique en python qui permet de
                # concaténer des chaînes de caractère avec des variables: les variables s'écrivent
                # entre crochets, le reste de la chaîne de caractère s'écrit normalement.
                # ce qui est en dessous est un équivalent de :
                # item_html = "<dt>" + numero + "</dt><dd>" + name ": <emph>" + trait + "</emph></dd>"
                # avec f"", on peut même faire des opérations entre accolates: f"{4 * 2}" retournera "8" !
                item_html += f"<dt>Item n°{numero}</dt><dd>{name}: <i>{trait}</i></dd>"

            # si c'est un prix, c'est quand même nettement plus simple:
            # on extrait le prix et on le stocke dans la list, dans un <li> (list item, élément de liste)
            elif "francs." in part:
                price = part
                list_html += f"<li>{price}</li>"

            # sinon, c'est une description. là encore, c'est assez facile:
            else:
                desc = part
                list_html += f"<li>{desc}</li>"

        list_html += "</ul>"  # on ferme la liste
        item_html += list_html  # on ajoute la liste avec le desc et le price à l'html
        item_html += "</div>"  # on ferme l'élément html
        html += item_html  # on ajoute l'html créé pour l'item au reste de l'html

    # on ouvre un squelette html a été créé dans utils. on l'ouvre et remplace '{PLACEHOLDER}'
    # par le html qu'on vient de produire
    with open("../utils/catalog_web_skeleton.html", mode="r", encoding="utf-8") as fh:
        skelly = fh.read()
    output = skelly.replace("{PLACEHOLDER_BASE}", html)  # on remplace {PLACEHOLDER} par notre html

    # on écrit le contenu de output dans un fichier en sortie
    with open("../output/catalog_web.html", mode="w", encoding="utf-8") as fh:
        fh.write(output)

    return None


if __name__ == "__main__":
    input_to_html()
